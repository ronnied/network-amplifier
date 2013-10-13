import wiringpi2
from lcd import HD44780
from time import sleep

######################################
#
# 3 Wire LCD Shift Register
# 
# extends HD44780 - 16x2 LCD
#
# Ronald Diaz ronald@ronalddiaz.net
# http://github.com/ronnied/
#
class HD44780_595(HD44780) :
  # Overriden to provide shift reg intercept
  def initGpio(self, gpio, a, b, c, d, e, f):
    if gpio == None:
      self.gpio = wiringpi2.GPIO(wiringpi2.GPIO.WPI_MODE_PINS)
    else:
      self.gpio = gpio

    # Setup ShiftReg
    self.pin_s_clock = 5
    self.pin_s_data = 0
    self.pin_s_latch = 3
    self.sRegBase = 100
    self.sRegPins = 6
    self.sReg = wiringpi2.sr595Setup(self.sRegBase, self.sRegPins, self.pin_s_data, self.pin_s_clock, self.pin_s_latch)

    # ShiftReg 3 wire
    self.gpio.pinMode(self.pin_s_clock, self.gpio.OUTPUT)
    self.gpio.pinMode(self.pin_s_data,  self.gpio.OUTPUT)
    self.gpio.pinMode(self.pin_s_latch, self.gpio.OUTPUT) 

    # LCD Pins (on the 595 end)
    self.pin_rs = self.sRegBase + 0 # rs
    self.pin_e =  self.sRegBase + 5 # e
    self.pin_d4 = self.sRegBase + 1 # d4
    self.pin_d5 = self.sRegBase + 2 # d5
    self.pin_d6 = self.sRegBase + 3 # d6
    self.pin_d7 = self.sRegBase + 4 # d7
    
# if __name__ == '__main__':
#     lcd = HD44780_595()
#     print lcd
#     sleep(1)
#     lcd.message("Raspberry Pi\n16x2 LCD 44780!")