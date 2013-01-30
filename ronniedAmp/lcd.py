import wiringpi
import time

######################################
#
# LCD Class for 6 wire / 4 bit control
#
# Ronald Diaz ronald@ronalddiaz.net
#
class Lcd:
  def __init__(self, gpio=None, rs=11, e=10, d4=6, d5=5, d6=4, d7=1, power=1):
    self.rs = rs
    self.e = e
    self.d4 = d4
    self.d5 = d5
    self.d6 = d6
    self.d7 = d7
    self.power = power
    
    # Setup GPIO
    if gpio == None:
      self.gpio = wiringpi.GPIO(wiringpi.GPIO.WPI_MODE_PINS)
    else:
      self.gpio = gpio

    # LCD GPIO SETUP
    self.LCD_E  = self.gpio.pinMode(self.e,  self.gpio.OUTPUT)
    self.LCD_RS = self.gpio.pinMode(self.rs, self.gpio.OUTPUT)
    self.LCD_D4 = self.gpio.pinMode(self.d4, self.gpio.OUTPUT)
    self.LCD_D5 = self.gpio.pinMode(self.d5, self.gpio.OUTPUT)
    self.LCD_D6 = self.gpio.pinMode(self.d6, self.gpio.OUTPUT)
    self.LCD_D7 = self.gpio.pinMode(self.d7, self.gpio.OUTPUT)

    # Define some device constants
    self.LCD_WIDTH = 16
    self.LCD_CHR = True
    self.LCD_CMD = False

    self.LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
    self.LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line 

    # Timing constants
    self.E_PULSE = 0.00005
    self.E_DELAY = 0.00005

    if self.power == 1:
      self.on()

  def init(self):
    self.lcd_byte(0x33, self.LCD_CMD)
    self.lcd_byte(0x32, self.LCD_CMD)
    self.lcd_byte(0x28, self.LCD_CMD)
    self.lcd_byte(0x0C, self.LCD_CMD) 
    self.lcd_byte(0x06, self.LCD_CMD)
    self.lcd_byte(0x01, self.LCD_CMD)

  def on(self):
    # power the lcd / backlight
    # wait...
    self.init()
    time.sleep(0.25)

  def off(self):
    # power off the lcd / backlight
    pass

  def home(self):
    self.position(0, 0)

  def position(self, x, y):
    pass
  
  # abstracted to allow change
  def output(self, pin, data):
    self.gpio.digitalWrite(pin, data)

  def lcd_byte(self, bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True  for character
    #        False for command
    self.output(self.rs, mode) # RS

    # High bits
    self.output(self.d4, False)
    self.output(self.d5, False)
    self.output(self.d6, False)
    self.output(self.d7, False)
    if bits&0x10==0x10:
      self.output(self.d4, True)
    if bits&0x20==0x20:
      self.output(self.d5, True)
    if bits&0x40==0x40:
      self.output(self.d6, True)
    if bits&0x80==0x80:
      self.output(self.d7, True)

    # Toggle 'Enable' pin
    time.sleep(self.E_DELAY)    
    self.output(self.e, True)  
    time.sleep(self.E_PULSE)
    self.output(self.e, False)  
    time.sleep(self.E_DELAY)      

    # Low bits
    self.output(self.d4, False)
    self.output(self.d5, False)
    self.output(self.d6, False)
    self.output(self.d7, False)
    if bits&0x01==0x01:
      self.output(self.d4, True)
    if bits&0x02==0x02:
      self.output(self.d5, True)
    if bits&0x04==0x04:
      self.output(self.d6, True)
    if bits&0x08==0x08:
      self.output(self.d7, True)

    # Toggle 'Enable' pin
    time.sleep(self.E_DELAY)    
    self.output(self.e, True)  
    time.sleep(self.E_PULSE)
    self.output(self.e, False)  
    time.sleep(self.E_DELAY)   

  def sendString(self, message):
    message = message.ljust(self.LCD_WIDTH," ")  
    for i in range(self.LCD_WIDTH):
      self.lcd_byte(ord(message[i]), self.LCD_CHR)

  def line1(self, message):
    self.lcd_byte(0x80, False)
    self.sendString(message)

  def line2(self, message):
    self.lcd_byte(0xC0, False)
    self.sendString(message)

  def lines(self, line1, line2):
    self.line1(line1)
    self.line2(line2)
