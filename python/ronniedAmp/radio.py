import smbus
import time
import RPi.GPIO as GPIO
from configobj import ConfigObj

#          B105.3FM        <- centered text
# freq + description scrolling    

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
    self.stationIdx = 0    # 
    self.station = {}      # current station    
    self.stations = {}     # all stations  
    self._readConfig()     # read config
    self._reset()          # Reset device

  # High Level Methods

  def addStation(self, station):
    self._addStation(station)

  def prevStation(self):
    if(self.stationIdx == 0):
      self.stationIdx = (len(self.stations) - 1)
    else:
      self.stationIdx = self.stationIdx - 1
    self.setStationIndex(self.stationIdx)

  def nextStation(self):
    if(self.stationIdx == (len(self.stations) - 1)):
      self.stationIdx = 0
    else:
      self.stationIdx = self.stationIdx + 1
    self.setStationIndex(self.stationIdx)

  def setStationIndex(self, index):
    self.station = self.stations[str(index)]
    #print "setStationIndex: ", index, str(index)
    self._updateStation()  

  def getStation(self):
    return self.station

  # Low Level Methods

  def _addStation(self, station):    
    # get station count (to gain last idx)
    newIdx = 'undef'
    # validate?
    # save station -> config
    self.config['stations'][newIdx] = station
    self.config.write()

  def _readConfig(self):
    # open config file
    self.config = ConfigObj("config-radio")
    
    # read all the stations
    self.stations = self.config['stations']

    # read default station
    defaultIdx = self.config['default']

    # set default station
    self.station = self.config['stations'][defaultIdx]

  def _updateVolume(self):
    self._sendByte(self.volume)

  def _updateStation(self):
    #print "Set Station: ", self.station
    nc = int(self.station['frequency'])
    nc *= 10
    nc -= 8750 
    nc /= 20 
    #print "Param: ", nc
    list1 = [1,128, nc] 
    # set tune bit and set channel 
    w6 = self.i2c.write_i2c_block_data(self.i2cAddress, 64, list1) 
    time.sleep(.1) # allow tuner to tune 
    # clear channel tune bit 
    list1 = [1,0,nc] 
    w6 = self.i2c.write_i2c_block_data(self.i2cAddress, 64, list1) 
    reg2 = self.i2c.read_i2c_block_data(self.i2cAddress,64, 32) 
    #print reg2  

  def _reset(self):
    GPIO.setmode(GPIO.BCM) 
    GPIO.setwarnings(False)
    GPIO.setup(23, GPIO.OUT) 
    GPIO.setup(0, GPIO.OUT)

    # Put SI4703 into 2 wire mode (I2C) 
    GPIO.output(0,GPIO.LOW) 
    time.sleep(.1) 
    GPIO.output(23, GPIO.LOW) 
    time.sleep(.1) 
    GPIO.output(23, GPIO.HIGH) 
    time.sleep(.1) 

    #print "Initial Register Readings" 
    reg = self.i2c.read_i2c_block_data(self.i2cAddress, 0, 32) 
    #print reg 

    #write x8100 to reg 7 to activate oscillator
    list1 = [0,0,0,0,0,0,0,0,0,129,0] 
    w6 = self.i2c.write_i2c_block_data(self.i2cAddress, 0, list1) 
    time.sleep(1) 

    #write x4001 to reg 2 to turn off mute and activate IC
    list1 = [1]
    w6 = self.i2c.write_i2c_block_data(self.i2cAddress, 64, list1) 
    time.sleep(.1)

    #write volume 0 dBFS = b1111
    list1 = [1,0,0,0,0,0,15]
    #print list1
    w6 = self.i2c.write_i2c_block_data(self.i2cAddress, 64, list1) 

    # Set default station
    self._updateStation()

# [
# {"name":"Vision FM",// Mhz/87.8 Mhz/88.0 Mhz (Various suburbs) Vision FM
#  "freq":"876"}, //"88.0 Mhz (Brisbane CBD and Moreton Island)                 
# {"name":"SBS Radio",
#  "freq":"933"}, // Mhz SBS Radio (international languages)
# {"name":"River",
#  "freq":"949"},// Mhz River 94.9
# {"name":"Family FM",
#  "freq":"965"}, // Mhz 96five Family FM
# {"name":"FM Mix",
#  "freq":"973"}, // Mhz 97.3 FM MIX
# {"name":"Ethnic",
#  "freq":"981"}, // Mhz 4EB (ethnic community radio)
# {"name":"Indigenous",
#  "freq":"989"}, // Mhz 98.9 FM (indigenous community radio)
# {"name":"Bay FM",
#  "freq":"1003"}, // Mhz Bay FM
# {"name":"101.1 FM",
#  "freq":"1011"}, // Mhz 101.1 FM
# {"name":"4ZZZ",
#  "freq":"1021"}, // Mhz 4ZZZ
# {"name":"4MBS",
#  "freq":"1037"}, // Mhz 4MBS
# {"name": "Triple M",
#  "freq":"1045"}, // Mhz Triple M
# {"name":"B105 FM",
#  "freq":"1053"}, // Mhz B105 FM
# {"name":"Classic FM",
#  "freq":"1061"}, // Mhz ABC Classic FM
# {"name":"Nova FM",
#  "freq":"1069"}, // Mhz Nova 106.9
# {"name":"Triple J",
#  "freq":"1077"} // Mhz Triple J
# ],