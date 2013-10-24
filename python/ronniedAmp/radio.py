import smbus
import time

######################################
#
# Class for controlling si470x via i2c 
# FM Tuner evaluation board w/ preamp 
#
# Ronald Diaz ronald@ronalddiaz.net
#
class Radio:
  def __init__(self):
    try:
      # open Linux device /dev/i2c-1
      self.i2c = smbus.SMBus(1)
    except:
      pass
    self.i2cAddress = 0x10 # address of SI4703
    #self.volume = 0x20   # volume = minimum
    #self.attenuationL = 0# (-x -> x ? )
    #self.attenuationR = 0# (-x -> x ? )
    #self.mute = False    # mute on
    #self.loudness = True # loudness on
    self.channel = 1053   # default ch
    #self.bass = 0x0F     # bass = 0
    #self.treble = 0x0F   # treble = 0    
    #self._reset()         # Reset device

  # High Level Commands

  def setVolume(self, volume):
    self.volume = volume
    self._updateVolume()

  def setStation(self, station):
    self.station = station
    self._updateStation()
    
  def muteOn(self):
    self.mute = True
    self._updateAttenuation()    

  def muteOff(self):
    self.mute = False
    self._updateAttenuation()

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
    self.bass = self._lookupTone(int(bass))
    self._updateBass()
    return self._lookupToneReverse(self.bass)

  def setTreble(self, treble):
    self.treble = self._lookupTone(int(treble))
    self._updateTreble()
    return self._lookupToneReverse(self.treble)

  # Low Level Commands

  def _updateVolume(self):
    self._sendByte(self.volume)

  def _updateChannel(self):
    print "Tuning: ", self.channel
    nc = int(self.channel)
    nc *= 10
    nc -= 8750 
    nc /= 20  
    print "Param: ", nc
    list1 = [1,128, nc] 
    # set tune bit and set channel 
    w6 = i2c.write_i2c_block_data(address, 64, list1) 
    time.sleep(.1) # allow tuner to tune 
    # clear channel tune bit 
    list1 = [1,0,nc] 
    w6 = i2c.write_i2c_block_data(address, 64, list1) 
    reg2 = i2c.read_i2c_block_data(address,64, 32) 
    print reg2  
    
  def _updateAttenuation(self):
    if self.mute == True:
      self._sendByte(0xDF)      
      self._sendByte(0xFF)
    else:
      self._sendByte(0xC0 | self.attenuationL)
      self._sendByte(0xE0 | self.attenuationR)
    
  def _updateAudioSwitch(self):           
    audioByte = 0x58          # Audio Switch Byte 
    if self.loudness == True: # Loudness
      audioByte |= 0x00
    else:
      audioByte |= 0x04    
    audioByte |= self.channel # Select Channel
    self._sendByte(audioByte) # Send Byte

  def _updateBass(self):
    self._sendByte(0x60 | self.bass)

  def _updateTreble(self):
    self._sendByte(0x70 | self.treble)

  def _lookupTone(self, value):
    try:
        return next(x for x in self.toneValues if x[0] == value)[1]
    except StopIteration:
      return 0x0F
  
  def _lookupToneReverse(self, value):
    try:
        return next(x for x in self.toneValues if x[1] == value)[0]
    except StopIteration:
      return 0

  def _updateAll(self):    
    self._updateVolume()
    self._updateAttenuation()
    self._updateAudioSwitch()
    self._updateBass()
    self._updateTreble()
    
  def _sendByte(self, b):
    print "data: %x" % b
    try:
      self.i2c.write_byte(self.i2cAddress, b) # send data via i2c    
    except:
      #print "exception"
      pass  

  def reset(self):
    GPIO.setmode(GPIO.BCM) #board numbering
    GPIO.setup(23, GPIO.OUT) 
    GPIO.setup(0, GPIO.OUT)  #SDA or SDIO 

    #put SI4703 into 2 wire mode (I2C) 
    GPIO.output(0,GPIO.LOW) 
    time.sleep(.1) 
    GPIO.output(23, GPIO.LOW) 
    time.sleep(.1) 
    GPIO.output(23, GPIO.HIGH) 
    time.sleep(.1) 

    address = 0x10 #address of SI4703 from I2CDetect utility

    print "Initial Register Readings" 
    reg = i2c.read_i2c_block_data(address, 0, 32) 
    print reg 

    #write x8100 to reg 7 to activate oscillator
    list1 = [0,0,0,0,0,0,0,0,0,129,0] 
    w6 = i2c.write_i2c_block_data(address, 0, list1) 
    time.sleep(1) 

    #write x4001 to reg 2 to turn off mute and activate IC
    list1 = [1] 
    #print list1 
    w6 = i2c.write_i2c_block_data(address, 64, list1) 
    time.sleep(.1) 

    #write volume 
    print "Doing Volume lowest setting" 
    list1 = [1,0,0,0,0,0,1] 
    w6 = i2c.write_i2c_block_data(address, 64, list1) 

    #write channel 
    print "Setting Channel, pick a strong one" 

    nc = 1011 #this is 101.1 The Fox In Kansas City Classic Rock!! 
    nc *= 10  #this math is for USA FM only 
    nc -= 8750 
    nc /= 20 

    list1 = [1,128, nc] 
    #set tune bit and set channel 
    w6 = i2c.write_i2c_block_data(address, 64, list1) 
    time.sleep(1) #allow tuner to tune 
    # clear channel tune bit 
    list1 = [1,0,nc] 
    w6 = i2c.write_i2c_block_data(address, 64, list1) 

    reg2 = i2c.read_i2c_block_data(address,64, 32) 
    print reg2  #just to show final register settings

    #You should be hearing music now! 
    #Headphone Cord acts as antenna



















