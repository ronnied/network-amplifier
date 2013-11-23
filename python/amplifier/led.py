####################################
#
# Class for controlling a single LED
#
# Ronald Diaz ronald@ronalddiaz.net
# 
import wiringpi
import sys

class Led:
  def __init__(self, pin, defaultState = False, gpio = None):
            
    self.state = self._setState(defaultState)
    self.pin = pin
    
    # If no gpio is given, create resource now
    if gpio == None:
      gpio = wiringpi.GPIO(wiringpi.GPIO.WPI_MODE_PINS)
    self.gpio = gpio
      
    # attempt to gain resource to GPIO pin
    try:
      self.sLed = self.gpio.pinMode(self.pin, self.gpio.OUTPUT)
    except:
      print "Error! Couldn't assign pin " + str(pin) + " of the GPIO in WPI MODE."
      print "Unexpected error:", sys.exc_info()[0]
      raise
      
    # Set default state
    self.out(self.state)
  
  def getPin(self):
    return self.pin
      
  def getState(self):
    return self.state

  # internal
  def _setState(self, s):
    if s == False or s == None or s == "0" or int(s) <= 0:
      self.state = 0
    else:
      self.state = 1

  def out(self, s):
    self._setState(s)   
    self.gpio.digitalWrite(self.pin, self.state)
    
  def on(self):
    self.out(1)
    
  def off(self):
    self.out(0)
    
    