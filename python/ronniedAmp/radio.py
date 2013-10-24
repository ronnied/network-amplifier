import smbus
import time
import RPi.GPIO as GPIO 

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
    self.station = 1053    # default station
    self.volume = 0        # volume    
    self._reset()          # Reset device

  # High Level Commands

  def setVolume(self, volume):
    self.volume = volume
    self._updateVolume()

  def setStation(self, station):
    self.station = station
    self._updateStation()

  def getStation(self):
    return self.station

  # Low Level Commands

  def _updateVolume(self):
    self._sendByte(self.volume)

  def _updateStation(self):
    print "Set Station: ", self.station
    nc = int(self.station)
    nc *= 10
    nc -= 8750 
    nc /= 20  
    print "Param: ", nc
    list1 = [1,128, nc] 
    # set tune bit and set channel 
    w6 = self.i2c.write_i2c_block_data(self.i2cAddress, 64, list1) 
    time.sleep(.1) # allow tuner to tune 
    # clear channel tune bit 
    list1 = [1,0,nc] 
    w6 = self.i2c.write_i2c_block_data(self.i2cAddress, 64, list1) 
    reg2 = self.i2c.read_i2c_block_data(self.i2cAddress,64, 32) 
    print reg2  

  def _reset(self):
    GPIO.setmode(GPIO.BCM) 
    GPIO.setup(23, GPIO.OUT) 
    GPIO.setup(0, GPIO.OUT)

    # Put SI4703 into 2 wire mode (I2C) 
    GPIO.output(0,GPIO.LOW) 
    time.sleep(.1) 
    GPIO.output(23, GPIO.LOW) 
    time.sleep(.1) 
    GPIO.output(23, GPIO.HIGH) 
    time.sleep(.1) 

    print "Initial Register Readings" 
    reg = self.i2c.read_i2c_block_data(self.i2cAddress, 0, 32) 
    print reg 

    #write x8100 to reg 7 to activate oscillator
    list1 = [0,0,0,0,0,0,0,0,0,129,0] 
    w6 = self.i2c.write_i2c_block_data(self.i2cAddress, 0, list1) 
    time.sleep(1) 

    #write x4001 to reg 2 to turn off mute and activate IC
    list1 = [1] 
    w6 = self.i2c.write_i2c_block_data(self.i2cAddress, 64, list1) 
    time.sleep(.1) 

    list1 = [1,0,0,0,0,0,1] 
    w6 = self.i2c.write_i2c_block_data(self.i2cAddress, 64, list1) 

    # Set default station
    self._updateStation()



















