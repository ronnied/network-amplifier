from ronniedAmp.lcd import HD44780
from ronniedAmp.led import Led
from ronniedAmp.volume import Volume
from ronniedAmp.timer import Timer
from ronniedAmp.scrollingText import ScrollingText
#import logging
import threading
import wiringpi
import time

######################################
#
# Display Class for controlling LCD
# and LEDs connected to Amplifier
#
# Ronald Diaz ronald@ronalddiaz.net
# 
class Display:
  def __init__(self, gpio = None):

    # If no gpio is given, create resource now
    if gpio == None:
      gpio = wiringpi.GPIO(wiringpi.GPIO.WPI_MODE_PINS)

    # Create resource to control HD44780 16x2 LCD
    self.lcd = HD44780(gpio)    
   
    # Create resources to control leds
    self.sLed = Led(3, 0, gpio)
    self.mLed = Led(0, 0, gpio) 

    # Volume
    self.vol = Volume()
    
    # Selected Input
    self.selectedInput = True # media = True, mp3 = False
      
  # Threaded Worker    
  class Worker(threading.Thread):
    
    # Realtime clock (every second)
    # Flashing text (for mute state)
    # Scrolling text (for now playing)    
      
    def __init__(self, gpio = None):
      threading.Thread.__init__(self)
      self.lock = threading.Lock()
      
      # Display resource
      self.disp = Display(gpio)
      
      # Create text buffers but don't scroll or blink just yet
      self.sTextLine1 = ScrollingText.Worker("", 16, True, False, 0.5, False, 0.5)
      self.sTextLine2 = ScrollingText.Worker("", 16, True, False, 0.5)
      self.sTextLine1.start()
      self.sTextLine2.start()
                  
      self.daemon = True
   
      # Clock Setup
      self.clockOn = False              
      self.clockShowSeconds = True
      
      #################################
      # DISPLAY STATES
      #
      # Welcome State (with 2 second timeout)
      # Media State (with clock)
      # MP3 State (with scrolling text)
      #
      # Volume change state
      # --> Volume Lingering state
      #    --> Back to current state
      self.STATE_WELCOME    = 0 #
      self.STATE_MEDIA      = 1 #
      self.STATE_MP3        = 2 #
      self.STATE_MUTED      = 3 #
      self.STATE_VOLUME     = 4 #
      #self.STATE_MANUAL     = 5
            
      # Timers
      #
      self.volumeTimer = Timer(1, False)
      self.selectLedTimer = Timer(0.25, False)
      self.welcomeTimer = Timer(3, False)
      self.MAIN_THREAD_DELAY = 0.05
      
      self.state = self.STATE_WELCOME
      self.prevState = self.STATE_WELCOME
      self.lastMenu = self.STATE_MEDIA
      self.powerOn()

    ################################################
    # Respond according to the current machine state
    #
    def run(self):
        
      line1PrevBuffer = ""
      line2PrevBuffer = ""
      
      while True:         
        #########################
        # DETERMINE MACHINE STATE
        #
        # Muted Blinking state on?
        if self.state == self.STATE_MUTED:          
          # update the (blinking) line buffers
          self.updateMuteStateBuffers()          
          
        elif self.state == self.STATE_VOLUME:
          # update the volume line buffers
          self.updateVolumeStateBuffers()
          
          # is the volume display lingering timer on and has it expired?
          if self.volumeTimer.isOn() == True and self.volumeTimer.elapsed() == True:
            #print "Volume Lingering timer elapsed!"
            self.volumeTimer.stop()
            self.restorePreviousState()            
          
        elif self.state == self.STATE_MEDIA:
          self.updateMediaStateBuffers()
          
        elif self.state == self.STATE_MP3:
          self.updateMp3StateBuffers()
          
        elif self.state == self.STATE_WELCOME:
          self.updateWelcomeStateBuffers()
          
          # is the welcome timer on and has it expired?
          if self.welcomeTimer.isOn() == True and self.welcomeTimer.elapsed() == True:
            #print "Welcome timer elapsed!"
            self.welcomeTimer.stop()
            # show media state (default)
            self.showMedia()

        ##########################################################
        # are the current buffers different from previous buffers?        
        if line1PrevBuffer != self.sTextLine1.getText() or line2PrevBuffer != self.sTextLine2.getText():
          #print "Display Updating..."
          self._updateLcdDisplay()          
          # cache current buffers
          line1PrevBuffer = self.sTextLine1.getText()
          line2PrevBuffer = self.sTextLine2.getText()
                  
        # Has the select led timer elapsed?
        if self.selectLedTimer.elapsed() == True:
          self.selectLedTimer.stop()
          # switch the led off
          self.disp.sLed.off()
                              
        ###########################
        # main display thread delay
        time.sleep(self.MAIN_THREAD_DELAY)
     
    #################################################
    # HIGH LEVEL COMMANDS (that alter machine states)
    #
    def powerOn(self):
      #print "power on"
      self.state = self.STATE_WELCOME
      self.prevState = self.STATE_WELCOME
      self.disp.lcd.on()
      self.disp.sLed.off()
      self.disp.mLed.off()
      self.welcomeTimer.start()
      
    def powerOff(self):
      self.disp.lcd.off()
      self.disp.sLed.off()
      self.disp.mLed.off()      
        
    def muteOn(self):
      #print "muteOn: " + str(self.state)      
      # mute led on
      self.disp.mLed.on()
      # Setup for blinking mute lcd
      self.stopAllTimers()      
      self.sTextLine1.startBlink()    
      # Save the last menu to restore
      self.prevState = self.lastMenu
      # Set the state (refreshed next cycle) only if not volume
      #if self.state != self.STATE_VOLUME or self.state != self.STATE_MUTED:
      #  self.prevState = self.state
      self.state = self.STATE_MUTED
      
    def muteOff(self):
      #print "muteOff: " + str(self.state)
      self.disp.mLed.off()
      # set the state to the last menu prior to muting
      self.state = self.lastMenu
      self.showVolume()
     
    def showVolume(self):
      #print "showVolume"
      self.stopAllTimers()
      self.volumeTimer.start()
      # Set the state (as long as it's not the volume state)
      if self.state != self.STATE_VOLUME:
        self.prevState = self.state
      # now set the current state to volume
      self.state = self.STATE_VOLUME 
      
    def setVolume(self, vol):
      self.disp.vol.set(vol)
      self.showVolume()

    def showMedia(self):
      self.stopAllTimers()
      self.disp.sLed.on()
      self.selectLedTimer.start()
      self.startClock()
      self.prevState = self.state
      self.state = self.STATE_MEDIA
      self.lastMenu = self.state      

    def showMp3(self):
      self.stopAllTimers()
      self.disp.sLed.on()
      self.selectLedTimer.start()
      self.sTextLine2.startScroll()
      self.sTextLine2.startBlink()
      #self.startClock()
      self.prevState = self.state
      self.state = self.STATE_MP3
      self.lastMenu = self.state
        
    def showWelcome(self):
      #print "showWelcome"
      self.stopAllTimers()
      self.welcomeTimer.start()
      self.prevState = self.state
      self.state = self.STATE_WELCOME
      
    #########################
    # UPDATE LCD LINE BUFFERS
    #          
    def updateMuteStateBuffers(self):
      self.sTextLine1.setText("Volume Muted")      
      self.sTextLine2.setText("")
        
    def updateVolumeStateBuffers(self):
      db = "%ddB" % self.disp.vol.dB()
      db = db.rjust(10, " ")
      line1 = "Volume%s" % db
      line2 = self.disp.vol.hash()          
      self.sTextLine1.setText(line1)
      self.sTextLine2.setText(line2)
    
    def updateMediaStateBuffers(self):
      # Showing static text on Line 1
      self.sTextLine1.setText("     Media")          
      # Showing the Clock on line 2
      self.sTextLine2.setText(self.getClock())

    def updateMp3StateBuffers(self):
      # scroll song playing in line 1
      # show time remaining in line 2
      self.sTextLine1.setText("      Mp3")      
      self.sTextLine2.setText("Total time remaining: 3m 08s")
    
    def updateWelcomeStateBuffers(self):
      self.sTextLine1.setText("Master " + chr(246) + " Control")
      self.sTextLine2.setText("v0.1 Ronald Diaz")         
                
    ####################
    # UPDATE LCD DISPLAY        
    def _updateLcdDisplay(self):
      line1 = self.sTextLine1.getText()
      line2 = self.sTextLine2.getText()
      self.disp.lcd.message(line1 + "\n" + line2)
      #self.disp.lcd.message(line1 + "\n" + "this is line 2")
            
    ##################
    # INTERNAL METHODS
    #
    # stopAll(scrolling / blinking / clock / time remain / lingering)
    def stopAllTimers(self):
      self.sTextLine1.stopAll()
      self.sTextLine2.stopAll()
      self.volumeTimer.stop()
      self.stopClock()             
             
    def startClock(self):
      self.clockOn = True
      self.sTextLine2.stopScroll()
      self.sTextLine2.setText(self.getClock())      
      
    def stopClock(self):
      self.clockOn = False
      
    def getClock(self):
      if self.clockShowSeconds == True:
        return str(time.strftime(" %2d %b %H:%M:%S"))
      else:
        return str(time.stftime("%a %b %H:%M"))
      
    # restore prev state ( welcome | media | mp3 | muted)      
    def restorePreviousState(self):      
      self.state = self.prevState
      if self.state == self.STATE_WELCOME:
        #print "restoring: welcome"
        self.showWelcome()
      elif self.state == self.STATE_MEDIA:
        #print "restoring: media"          
        self.showMedia()
      elif self.state == self.STATE_MP3:
        #print "restoring: mp3"
        self.showMp3()
      elif self.state == self.STATE_MUTED:
        #print "restoring: muted"
        self.muteOn()
   
#    def updateSongPlaying(self, text):
#      self.lcdLine1.setText(text)
#      self.lcdLine1.startScroll()
#      #self.scrollingLine1 = True                            
