from ronniedAmp.timer import Timer
import collections
import logging
import threading
import time
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

######################################
#
# Scrolling Text Buffer Class
#
# Ronald Diaz <ronald@ronalddiaz.net>
# http://github.com/ronnied
#
# Added Timer class reference
# Added Blinking state
#
class ScrollingText():
  def __init__(self, text, width, direction = True):
    self.width = width
    self.direction = direction # Left = True, Right = False            
    self.renderedBuffer = ""        
    self.setText(text)
    
  def setText(self, text, direction = True):
    self.direction = direction    
    # fill the text to at least the width size
    if len(text) < self.width:      
      text = text.ljust(self.width, " ")            
    self.textBuffer = collections.deque(text)
    # fill the renderedBuffer
    self._updateBuffer()
        
  def getText(self):
    return self.renderedBuffer              
  
  def scroll(self):
    if self.direction == True:        
      self.textBuffer.rotate(-1)            
    else:
      self.textBuffer.rotate(1)      
    self._updateBuffer()    
          
  # cut [ 0 -> width-1 ] chars out of the textBUffer
  # and put them into the renderedBuffer
  def _updateBuffer(self):
    #print self.renderedBuffer
    self.renderedBuffer = ""
    # fill the widthBuffer with [ 0 -> width-1 ]
    for i in range(0, self.width):
     self.renderedBuffer = self.renderedBuffer + self.textBuffer[i] 
                 
  # Threaded Worker    
  class Worker(threading.Thread):
    def __init__(self, text = "This is a test scrolling text class.", width = 16, direction = True, scrolling = True, speed = 0.2, blinking = False, blinkSpeed = 0.25):
      threading.Thread.__init__(self)
      self.lock = threading.Lock()
      self.sText = ScrollingText(text, width, direction)
      #print self.sText
      self.daemon = True
   
      # Timers
      self.scrollTimer = Timer(speed, scrolling)      
      self.blinkTimer = Timer(blinkSpeed, blinking)
      self.blinkState = False
      
    def run(self):
      while True:        
        # are we currently scrolling?
        if self.scrollTimer.isOn() == True:
          #print "scrolling!"
          # have we elapsed the scroll scrollTimer?
          if self.scrollTimer.elapsed() == True:                                
            #print "scroll scrollTimer elapsed!"
            self.sText.scroll()                         
            # reset the scrollTimer
            self.scrollTimer.reset()            
            
        # are we currently blinking?
        if self.blinkTimer.isOn() == True:
          # have we elapsed the blinking scrollTimer?
          if self.blinkTimer.elapsed() == True:
            #print "BLINK"
            # switch blink states
            self.blinkState = not self.blinkState
            #print str(self.blinkState)
            # restart the blinking scrollTimer
            self.blinkTimer.reset()
                        
        time.sleep(0.01)

    def setText(self, text, direction = True):
      self.sText.setText(text, direction)

    def getText(self):
      #with self.lock:
      # if currently blinking
      if self.blinkState == True:                               
       return " " * self.sText.width
      else:  
        return self.sText.getText()
  
    def startScroll(self):
      self.scrollTimer.start()
      
    def stopScroll(self):
      self.scrollTimer.stop()
  
    def startBlink(self):
      self.blinkTimer.start()
      self.blinkState = True
      
    def stopBlink(self):
      self.blinkTimer.stop()
      self.blinkState = False
      
    def stopAll(self):        
      self.stopScroll()
      self.stopBlink()
  