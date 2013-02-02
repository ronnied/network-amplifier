from ronniedAmp.display import Display
from time import sleep

# Amplifier Controller
#
# Accepts messages that affect the state of the system
#
# web server -> incoming
# display server <- outgoing
# i2cAmplifier <- outgoing (todo)
# relay module <- outgoing (todo)
#
# Ronald Diaz 2013
# ronald@ronalddiaz.net
#
# Messages ::
#
# Inputs:
#       -> PowerOn
#       -> PowerOff
#       -> MuteOn
#       -> MuteOff
#       -> MuteToggle
#       -> SelectMedia
#       -> SelectMp3
#       -> SelectToggle
#       -> VolumeUp
#       -> VolumeDown
#       -> VolumeSet(0 -> 100)
#       -> VolumeDelta(-x -> x)
#
# Status Messages (todo)
#
# getVolume
# getMuteState
# getSelectedInput
#
# MPD Commands (todo)
# isPlaying
# getSong
# getSongTimeRemain
# getSongTimeTotal
# 
class Controller():
  def __init__(self):
    #
    # Amplifier States
    #
    self.muteState = False    
    self.powerState = False
    self.selectState = False
    
    # Volume 0->100
    self.volume = 0

    # Display Client Resource Threaded
    self.display = Display.Worker()
    self.display.start()
    sleep(0.5)
    
    # Relay Resource
    self.relay = None
    
    # i2c Resource
    self.i2c = None
  
  # Power On
  #
  def powerOn(self):
    if self.powerState == True:            
      return "ok. Power already on."   
    self.powerState = True
    #self.i2c.powerOn()
    self.display.powerOn()
    return "ok"

  # Power Off
  #
  def powerOff(self):
    if self.powerState == False:            
      return "ok. Power already off."      
    self.powerState = False
    #self.i2c.powerOff()
    self.display.powerOff()
    return "ok"

  # Select Audio Input [ Media | MP3 ]
  #
  def selectMedia(self):
    if self.selectState == False:
      return "ok. Media already selected."
    #self.i2c.selectMedia()
    self.display.showMedia()
    self.selectState = False
    return "ok"    

  def selectMp3(self):
    if self.selectState == True:              
      return "ok. Mp3 already selected."
    self.display.showMp3()
    #self.i2c.selectMp3()
    self.selectState = True
    return "ok"    

  def selectToggle(self):
    #print "select toggle: currently: " + str(self.selectState)
    if self.selectState == False:
      #self.i2c.selectMp3()
      self.selectMp3()
    else:
      #self.i2c.selectMedia()
      self.selectMedia()    
    return "ok"        

  def muteOn(self):
    if self.muteState == True:
      return "ok. Already muted."
    #self.relay.muteOn()
    self.display.muteOn()    
    self.muteState = True
    return "ok"    

  def muteOff(self):
    if self.muteState == False:
      return "ok. Mute already off."      
    #self.relay.muteOff()
    self.display.muteOff()    
    self.muteState = False
    return "ok"    

  def muteToggle(self):
    #print "mute toggle: currently: " + str(self.muteState)
    if self.muteState == False:
      self.muteOn()
    else:
      self.muteOff()
    return "ok"

  # Volume Methods
  #
  def volumeUp(self):
    self.volume = self.volumeValidate(self.volume + 1)
    #self.i2c.volumeSet(self.volume)
    self.display.volumeSetLcd(self.volume)
    return "ok"    

  def volumeDown(self):
    self.volume = self.volumeValidate(self.volume - 1)
    #self.i2c.volumeSet(self.volume)
    self.display.setVolume(self.volume)
    return "ok"    

  def volumeDelta(self, delta=0):
    if delta == 0:
      return "ok. no change"
    delta = int(delta)
    self.volume = int(self.volumeValidate(int(self.volume) + (delta / 2)))    
    #self.i2c.volumeSet(self.volume)
    self.display.setVolume(self.volume)
    return "ok"

  def volumeSet(self, volume):
    self.volume = self.volumeValidate(volume)
    #print "controller:volume:" + str(self.volume)
    self.display.setVolume(self.volume)
    return "ok"    
      
  def volumeValidate(self, vol):
    #print "controller:volumeValidate:" + str(vol)
    if vol == '':
     vol = 0
    vol = int(vol)
    if vol<0:
      vol=0
    if vol>100:
      vol=100
    #print "controller:volumeValidate:post:" + str(vol)
    return vol

  # Getters    
  #    
  def volumeGet(self):
    return self.volume
