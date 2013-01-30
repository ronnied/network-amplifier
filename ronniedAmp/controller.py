from ronniedAmp.display import Display
from ronniedAmp.input import Input
from time import sleep

# Amplifier Controller
#
# Accepts messages that affect the state of the system
#
# input server -> incoming
# web server -> incoming
# display server <- outgoing
# i2cAmplifier <- outgoing
# relay module <- outgoing
#
# Ronald Diaz 2013
# ronald@ronalddiaz.net
#
# Messages ::
#
# Input -> MuteOn
#       -> MuteOff
#       -> VolumeUp
#       -> VolumeDown
#       -> VolumeSet(0 -> 100)
#       -> VolumeDelta(-10 -> 10)
#
# Status Messages
#
# getVolume
# getMuteState
# getSelectedInput
#
# MPD Commands
# isPlaying
# getSong
# getSongTimeRemain
# getSongTimeTotal
# 
class Controller:
  def __init__(self):
    # Amplifier States
    #
    self.muteState = False
    self.powerState = False
    
    # Volume 0->100
    self.volume = 0

    self.display = Display()

  #
  # Power On
  #
  def powerOn(self):
    self.powerState = True
    self.display.on()
    sleep(0.5)
    self.display.welcome()

  #
  # Power Off
  #
  def powerOff(self):
    self.powerState = False
    self.display.off()

  #
  # Select Audio Input
  #
  # 0 = Media
  # 1 = MP3
  #
  def selectInput(self, i):
    if i<0:
      i=0
    if i>1:
      i=1
    self.inputSelected = i
    self.display.select(i)

  # Set Mute LED On         :/led/muteOn
  # Set Mute Relay Low      :/relay/muteOn
  # Set Display LCD muteOn  :/display/muteOn
  def muteOn(self):
    self.relay.muteOn
    self.display.muteLedOn()
    self.display.muteLcd()
    self.muteState = True

  # Set Mute LED Off        :/led/muteOff
  # Set Mute Relay Low      :/relay/muteOff
  # Set Display LCD muteOn  :/display/muteOff
  def muteOff(self):
    self.relay.muteOff
    self.display.muteLedOff()
    self.display.muteLcd()
    self.muteState = False

  #
  # Volume Methods
  #
  def volumeUp(self):
    self.volume = self.volumeValidate(self.volume + 1)
    self.display.volumeSet(self.volume)

  def volumeDown(self):
    self.volume = self.volumeValidate(self.volume - 1)
    self.display.volumeSet(self.volume)

  def volumeDelta(self, delta=0):
    self.volume = self.volumeValidate(self.volume + (delta / 2))
    self.display.volumeSet(self.volume)

  def volumeSet(self, volume):
    self.volume = self.volumeValidate(volume)
    self.display.volumeSet(self.volume)
  
  def volumeValidate(self, vol):
    if vol<0:
      vol=0
    if vol>100:
      vol=100
    return int(vol)
