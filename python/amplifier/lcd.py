import wiringpi
from time import sleep

######################################
#
# Class for 6 wire / 4 bit control
# of HD44780 based 16x2 LCD
#
# Ronald Diaz ronald@ronalddiaz.net
# http://github.com/ronnied/
#
class HD44780:
  def __init__(self, gpio=None, rs=11, e=10, d4=6, d5=5, d6=4, d7=1, power=1):
    self.initConstants()
    self.initGpio(gpio, rs, e, d4, d5, d6, d7)
    self.initPower(power)

  def initPower(self, power):
    self.power = power
    if self.power == 1:
      self.on()  

  def initGpio(self, gpio, rs=11, e=10, d4=6, d5=5, d6=4, d7=1):
    if gpio == None:
      self.gpio = wiringpi.GPIO(wiringpi.GPIO.WPI_MODE_PINS)
    else:
      self.gpio = gpio      
    # LCD Pins
    self.E  = self.gpio.pinMode(self.pin_e,  self.gpio.OUTPUT)
    self.RS = self.gpio.pinMode(self.pin_rs, self.gpio.OUTPUT)
    self.D4 = self.gpio.pinMode(self.pin_d4, self.gpio.OUTPUT)
    self.D5 = self.gpio.pinMode(self.pin_d5, self.gpio.OUTPUT)
    self.D6 = self.gpio.pinMode(self.pin_d6, self.gpio.OUTPUT)
    self.D7 = self.gpio.pinMode(self.pin_d7, self.gpio.OUTPUT)

  def initConstants(self):
    self.width = 16 # LCD Width
    self.l1 = 0x80 # LCD RAM address for the 1st line
    self.l2 = 0xC0 # LCD RAM address for the 2nd line
    self.E_PULSE = 0.00005 # Timing
    self.E_DELAY = 0.00005 # Timing

  def init(self):
    self.cmd(0x33)
    self.cmd(0x32)
    self.cmd(0x28)
    self.cmd(0x0C) 
    self.cmd(0x06)
    self.cmd(0x01)

  def on(self):
    # power the lcd / backlight
    pass
    # wait...
    self.init()
    # wait...
    sleep(0.5)

  def off(self):
    # clear the screen
    self.clear()
    # power off the lcd / backlight
    pass
    
  def clear(self):
      self.message(" " * 16 + "\n" + " " * 16)

  # abstracted to allow change
  def out(self, pin, data):
    self.gpio.digitalWrite(pin, data)
  
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
  def byte(self, bits, mode):
    self.out(self.pin_rs, mode)
    self.highBits(bits)
    self.toggleEnablePin()
    self.lowBits(bits)
    self.toggleEnablePin()
  
  def toggleEnablePin(self):
    sleep(self.E_DELAY)    
    self.out(self.pin_e, True)  
    sleep(self.E_PULSE)
    self.out(self.pin_e, False)  
    sleep(self.E_DELAY) 
    
  def highBits(self, bits):
    self.out(self.pin_d4, False)
    self.out(self.pin_d5, False)
    self.out(self.pin_d6, False)
    self.out(self.pin_d7, False)
    if bits&0x10==0x10:
      self.out(self.pin_d4, True)
    if bits&0x20==0x20:
      self.out(self.pin_d5, True)
    if bits&0x40==0x40:
      self.out(self.pin_d6, True)
    if bits&0x80==0x80:
      self.out(self.pin_d7, True)
    
  def lowBits(self, bits):
    self.out(self.pin_d4, False)
    self.out(self.pin_d5, False)
    self.out(self.pin_d6, False)
    self.out(self.pin_d7, False)
    if bits&0x01==0x01:
      self.out(self.pin_d4, True)
    if bits&0x02==0x02:
      self.out(self.pin_d5, True)
    if bits&0x04==0x04:
      self.out(self.pin_d6, True)
    if bits&0x08==0x08:
      self.out(self.pin_d7, True)      

  def cmd(self, bits):
      self.byte(bits, False)

  def chr(self, bits):
      self.byte(bits, True)    
    
  def message(self, text):
      #print text
      # Auto left justify both lines      
      msg = text.split("\n")      
      msg[0] = msg[0].ljust(16, " ")
      msg[1] = msg[1].ljust(16, " ")            
      text = msg[0] + "\n" + msg[1]
      #print text              
      self.cmd(self.l1)
      #print text
      for char in text:
          if char == '\n':
              self.cmd(self.l2)
          else:
              self.chr(ord(char))

#  def sendString(self, message):
#    message = message.ljust(self.width," ")  
#    for i in range(self.width):
#      self.byte(ord(message[i]), self.chr)
#
#  def line1(self, message):
#    self.byte(0x80, False)
#    self.sendString(message)
#
#  def line2(self, message):
#    self.byte(0xC0, False)
#    self.sendString(message)
#
#  def lines(self, line1, line2):
#    self.line1(line1)
#    self.line2(line2)

#if __name__ == '__main__':
#
#    lcd = HD44780()
#    print lcd
#    sleep(1)
#    lcd.message("Raspberry Pi\n16x2 LCD 44780!")