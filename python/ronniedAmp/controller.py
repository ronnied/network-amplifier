from ronniedAmp.display import Display
from ronniedAmp.pt2314 import PT2314
from ronniedAmp.i2c import I2cInit
from ronniedAmp.radio import Radio
from time import sleep
import json

# Amplifier Controller
#
# Accepts messages that affect the state of the system
#
# web server -> incoming
# display server <- outgoing
# i2cAmplifier <- outgoing
# i2cRadio <- outgoing
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
#       -> SelectRadio
#       -> SelectToggle
#       -> VolumeUp
#       -> VolumeDown
#       -> VolumeSet(0 -> 100)
#       -> VolumeDelta(-x -> x)
#
# Status Message
#  # describe status message here
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
# Radio Commands (todo)
# switch station
# get rdbs
#
class Controller():
  def __init__(self):
    #
    # Amplifier States
    #
    self.muteState = False    
    self.powerState = False
    self.selectState = 0 # 0 -> 2    
    
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

    # reset i2c ports
    self.i = I2cInit()
    
    # i2c PT2314 Resource
    self.audio = PT2314()

    # i2c Radio Resource
    self.radio = Radio()
  
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
    #self.audio.powerOn()    
    self.volumeSet(50)
    #self.audio.setVolume(0x10)
    self.audio.loudnessOn()
    self.muteOff()
    #self.audio.muteOff()
    self.selectMedia()
    #self.audio.selectChannel(0)   
    self.audio.setAttenuation(0,0) 
    self.audio.setBass(0)
    self.audio.setTreble(0)
    self.display.powerOn()
    return self.ok()

  # Power Off
  #
  def powerOff(self):
    if self.powerState == False:            
      return self.ok("Power already off.")      
    self.powerState = False
    #self.audio.powerOff()
    self.display.powerOff()
    return self.ok()

  # Select Audio Input [ Media | MP3 ]
  #
  def selectMedia(self):
    #if self.selectState == False:
    #  return self.ok("ok. Media already selected.")
    self.audio.selectChannel(0)
    self.display.showMedia()
    self.selectState = 0
    return self.ok()

  def selectMp3(self):
    if self.selectState == 1:
      return self.ok("ok. Mp3 already selected.")
    self.audio.selectChannel(1)
    self.display.showMp3()
    self.selectState = 1
    return self.ok()

  def selectRadio(self):
    if self.selectState == 2:
      return self.ok("ok. Radio already selected.")
    self.audio.selectChannel(2) # route audio input
    #self.display.showRadio()    
    self.selectState = 2
    return self.ok()

  def selectAux(self):
    if self.selectState == 3:              
      return self.ok("ok. Aux already selected.")
    self.audio.selectChannel(3) # route audio input
    #self.display.showAux()
    self.selectState = 3
    return self.ok()

  def selectToggle(self):
    # toggle through states
    self.selectState = self.selectState + 1
    # upper limit
    if self.selectState > 3:
      self.selectState = 0
    # switch states
    if self.selectState == 0:
      self.audio.selectChannel(0)
      self.selectMedia()
    elif self.selectState == 1:
      self.audio.selectChannel(1)
      self.selectMp3()
    elif self.selectState == 2:
      self.audio.selectChannel(2)
      self.selectRadio()
    elif self.selectState == 3:
      self.audio.selectChannel(3)
      self.selectAux()
    return self.ok()

  def muteOn(self):
    if self.muteState == True:
      return "ok. Already muted."
    #self.relay.muteOn()
    self.audio.muteOn()
    self.display.muteOn()    
    self.muteState = True
    return self.ok()

  def muteOff(self):
    if self.muteState == False:
      return self.ok("ok. Mute already off.")      
    #self.relay.muteOff()
    self.audio.muteOff()
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
    self.audio.setVolume(self.volumei2c)
    self.display.volumeSetLcd(self.volume)
    return self.ok()

  def volumeDown(self):
    self.volume = self.volumeValidate(self.volume - 1)
    self.audio.setVolume(self.volumei2c)
    self.display.setVolume(self.volume)
    return self.ok() 

  def volumeDelta(self, delta=0):
    if delta == 0:
      return self.ok("ok. no change")
    delta = int(delta)
    self.volume = int(self.volumeValidate(int(self.volume) + (delta / 2)))    
    self.audio.setVolume(self.volumei2c)
    self.display.setVolume(self.volume)
    return self.ok()

  def volumeSet(self, volume):
    self.volume = self.volumeValidate(volume)
    #print "controller:volume:" + str(self.volume)
    self.audio.setVolume(self.volumei2c)
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
    # calculate audio i2c volume
    self.volumei2c = int(0x3F - float((float(63)/float(100) * float(vol))))
    return vol

  # Tone Methods
  #
  def bassSet(self, bass):
    self.bass = self.audio.setBass(bass)
    self.display.setTone(self.bass, self.treble)
    return self.ok()

  def trebleSet(self, treble):
    self.treble = self.audio.setTreble(treble)
    self.display.setTone(self.bass, self.treble)
    return self.ok()

  def radioStationSet(self, station):
    self.radio.setStation(station)
    return self.getAll()

  # Getters
  def volumeGet(self):
    return self.volume

  def getAll(self):
    data = {'power' : self.powerState,
             'volume' : self.volume,
             'mute' : self.muteState,
             'select' : self.selectState,
             'bass': self.bass,
             'treble': self.treble,
             'radio': {
                'station' : self.radio.station
              }
            }
    return json.dumps(data)