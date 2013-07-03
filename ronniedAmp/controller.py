from ronniedAmp.display import Display
from ronniedAmp.pt2314 import PT2314
from time import sleep
import json

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
    self.volume = 50
    self.volumei2c = 0x20

    # Tone
    self.bass = 0
    self.treble = 0

    # Display Client Resource Threaded
    self.display = Display.Worker()
    self.display.start()
    sleep(0.5)
    
    # Relay Resource
    self.relay = None
    
    # i2c Resource
    self.i2c = PT2314()
  
  # json formatted ok response
  def ok(self, status = "ok"):
    data = {"result" : True, "status" : status}
    return json.dumps(data)
  
  # Power On
  #
  def powerOn(self):
    if self.powerState == True:            
      return self.ok("ok. Power already on.")   
    self.powerState = True
    #self.i2c.powerOn()    
    self.volumeSet(50)
    #self.i2c.setVolume(0x10)
    self.i2c.loudnessOn()
    self.muteOff()
    #self.i2c.muteOff()
    self.selectMedia()
    #self.i2c.selectChannel(0)   
    self.i2c.setAttenuation(0,0) 
    self.i2c.setBass(0)
    self.i2c.setTreble(0)
    self.display.powerOn()
    return self.ok()

  # Power Off
  #
  def powerOff(self):
    if self.powerState == False:            
      return self.ok("Power already off.")      
    self.powerState = False
    #self.i2c.powerOff()
    self.display.powerOff()
    return self.ok()

  # Select Audio Input [ Media | MP3 ]
  #
  def selectMedia(self):
    if self.selectState == False:
      return self.ok("ok. Media already selected.")
    self.i2c.selectChannel(0)
    self.display.showMedia()
    self.selectState = False
    return self.ok()    

  def selectMp3(self):
    if self.selectState == True:              
      return self.ok("ok. Mp3 already selected.")
    self.i2c.selectChannel(1)
    self.display.showMp3()    
    self.selectState = True
    return self.ok()   

  def selectToggle(self):
    #print "select toggle: currently: " + str(self.selectState)
    if self.selectState == False:
      self.i2c.selectChannel(1)
      self.selectMp3()
    else:
      self.i2c.selectChannel(0)
      self.selectMedia()    
    return self.ok()       

  def muteOn(self):
    if self.muteState == True:
      return "ok. Already muted."
    #self.relay.muteOn()
    self.i2c.muteOn()
    self.display.muteOn()    
    self.muteState = True
    return self.ok()

  def muteOff(self):
    if self.muteState == False:
      return self.ok("ok. Mute already off.")      
    #self.relay.muteOff()
    self.i2c.muteOff()
    self.display.muteOff()    
    self.muteState = False
    return self.ok()

  def muteToggle(self):
    #print "mute toggle: currently: " + str(self.muteState)
    if self.muteState == False:
      self.muteOn()
    else:
      self.muteOff()
    return self.ok()

  # Volume Methods
  #
  def volumeUp(self):
    self.volume = self.volumeValidate(self.volume + 1)
    self.i2c.setVolume(self.volumei2c)
    self.display.volumeSetLcd(self.volume)
    return self.ok()

  def volumeDown(self):
    self.volume = self.volumeValidate(self.volume - 1)
    self.i2c.setVolume(self.volumei2c)
    self.display.setVolume(self.volume)
    return self.ok() 

  def volumeDelta(self, delta=0):
    if delta == 0:
      return self.ok("ok. no change")
    delta = int(delta)
    self.volume = int(self.volumeValidate(int(self.volume) + (delta / 2)))    
    self.i2c.setVolume(self.volumei2c)
    self.display.setVolume(self.volume)
    return self.ok()

  def volumeSet(self, volume):
    self.volume = self.volumeValidate(volume)
    #print "controller:volume:" + str(self.volume)
    self.i2c.setVolume(self.volumei2c)
    self.display.setVolume(self.volume)
    return self.ok()   
      
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
    # calculate i2c volume
    self.volumei2c = int(0x3F - float((float(63)/float(100) * float(vol))))
    return vol

  # Tone Methods
  #
  def bassSet(self, bass):
    self.bass = self.i2c.setBass(bass)
    #self.display.bassSetLcd(self.bass)
    return self.ok()

  def trebleSet(self, treble):
    self.treble = self.i2c.setTreble(treble)
    #self.display.trebleSetLcd(self.treble)
    return self.ok()

  # Getters
  def volumeGet(self):
    return self.volume

  def getAll(self):
    data = {'power' : self.powerState,
             'volume' : self.volume,
             'mute' : self.muteState,
             'select' : self.selectState,
             'bass': self.bass,
             'treble': self.treble}
    return json.dumps(data)    
