import smbus
import time

######################################
#
# Class for controlling PT2314 via i2c 
# 4-channel input audo processor
#
# Ronald Diaz ronald@ronalddiaz.net
#
class PT2314:
  def __init__(self):
    try:
      # open Linux device /dev/i2c-0
      self.i2c = smbus.SMBus(0)
    except:
      pass
    self.i2cAddress = 0x88    
    self.volume = 0      # volume = minimum
    self.attenuationL = 0# (-x -> x ? )
    self.attenuationR = 0# (-x -> x ? )
    self.mute = True     # mute on
    self.loudness = True # loudness on
    self.channel = 0     # channel 0 selected [ 0 > 3 ]
    self.bass = 0xF      # bass = 0
    self.treble = 0XF    # treble = 0    
    self._updateAll()    # Initialise all 
    
  # High Level Commands
  #
  def setVolume(self, volume):
    self.volume = volume
    self._updateVolume()
    
  def muteOn(self):
    self.mute = True
    self._updateAttenuation()    

  def muteOff(self):
    self.mute = False
    self._updateAttenuation()

  def selectChannel(self, ch):
    self.channel = ch
    self._updateAudioSwitch()
  
  def loudnessOn(self):
    self.loudness = True
    self._updateAudioSwitch()
    
  def loudnessOff(self):
    self.loudness = False
    self._updateAudioSwitch()
    
  def setAttenuation(self, l, r):
    self.attenuationL = l
    self.attenuationR = r
    self._updateAttenuation()
    
  def setBass(self, bass):
    self.bass = bass
    self._updateBass()

  def setTreble(self, treble):
    self.treble = treble
    self._updateTreble()

  # Low Level Commands
  #
  def _updateVolume(self):
    _sendByte(self.volume)
    
  def _updateAttenuation(self):
    if self.mute == True:
      _sendByte(0xDF)      
      _sendByte(0xFF)
    else:
      _sendByte(0xC0 | self.attenuationL)
      _sendByte(0xE0 | self.attenuationR)
    
  def _updateAudioSwitch(self):           
    audioByte = 0x58          # Audio Switch Byte 
    if self.loudness == True: # Loudness
      audioByte |= 0x00
    else:
      audioByte |= 0x04    
    audioByte |= self.channel # Select Channel
    self._sendbyte(audioByte) # Send Byte

  def _updateBass(self):
    self._sendByte(0x60 | self.bass)

  def _updateTreble(self):
    self._sendByte(0x70 | self.bass)
    
  def _updateAll(self):    
    self._updateVolume()
    self._updateAttenuation()
    self._updateAudioSwitch()
    self._updateBass()
    self._updateTreble()
    
  def _sendByte(self, b):
    # send data via i2c
    self.i2c.write_byte(self. address, b)    
    time.sleep(0.1)

#code BYTE _bVolImageTable[] = {
##ifdef AV_CENTER
#0x3f,0x2b,0x26,0x20,0x1e,0x1a,0x18,0x16,0x14,0x12,0x10,0xf,0xe,0xd,0xc,0x0a,0x08,0x06,0x03,0x01,0x00
##else
#0x3f,0x2e,0x2b,0x29,0x26,0x23,0x20,0x1e,0x1c,0x1a,0x18,0x16,0x14,0x12,0x10,0xf,0xe,0xd,0xc,0xb,0x0a,0x09,0x08,0x07,0x06,0x05,0x04,0x03,0x02,0x01,0x00

#     Function : vMainVolCtrltemp
#  Description : Main vol control by control PT2314
#    Parameter : 
#    Return    : 
#************************************************************************/
#void vMainVolCtrltemp(BYTE main_Vol) large
#{
#
#     if(main_Vol > 20)
#         main_Vol = 20;
#     #ifdef YXT_LOST_PATCH
#          _rewrite5 = main_Vol;
#     #endif
#     vPT2314Write(COMMAND_VOL_CTRL | _bVolImageTable[main_Vol]);
#}
#  def _blanketUpdate(self):
#    data = [0,0,0,0,0,0]
#          
#    # VOLUME
#    data[0]=self.volume
#
#    # ATTL (Attenuators)    
#    if self.mute == True:    
#      data[1]=0xdf #l
#      data[2]=0xff #r
#    else:
#      # Set attenuators to 0
#      data[2]=0xdf-0x1f #l #dat[1]=0xdf-0x1f #l
#      data[1]=0xff-0x1f #r #dat[2]=0xff-0x1f #r
#
#      if self.attenuation != 0:
#        if self.attenuation > 0:
#          data[1] |= self.attenuation
#        else:
#          data[2] |= self.attenuation * -1
#          
#    #  LOUDNESS
#    data[3]=self.loudness | 0x40
#    
#    # Bass Control
#    if self.bass > 0:
#      data[4] = 15 - self.bass
#    else:
#      data[4] = self.bass + 7
#    
#    # Treble Control
#    if self.treble > 0:
#      data[5] = 15 - self.treble
#    else
#      data[5] = self.treble + 7
#            
#    data[4] |= 0x60
#    data[5] |= 0x70
#        
#  def _sendData(self):
#    for i in range(0, 5):
#      _sendByte(self.data[i])
#    
#  def _sendByte(self):
#    # send data via i2c
#    #I2CWriteStream(self.i2cAddress, dat, sizeof(dat))
#    pass