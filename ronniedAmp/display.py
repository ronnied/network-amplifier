import ronniedAmp.lcd
import wiringpi
import time

######################################
#
# Display Class for controlling LCD
# and LEDs connected to Amplifier
#
# Ronald Diaz ronald@ronalddiaz.net
#
class Display:
  def __init__(self, gpio = None):

    # Volume
    self.vol15 = 0
    self.vol63 = -63
    self.vol100 = 0

    # If no gpio is given, create resource now
    if gpio == None:
      gpio = wiringpi.GPIO(wiringpi.GPIO.WPI_MODE_PINS)

    # Create resource to control HD4470 16x2 LCD
    self.lcd = ronniedAmp.lcd.Lcd(gpio)
   
    # Create resources to control leds 
    self.select_led_pin = 3

    # Time Setup
    self.time_mode_seconds = True

  def on(self):
    self.lcd.init()
    self.lcd.on()

  def off(self):
    self.lcd.init()
    self.lcd.off()
    self.selectLedOff()
    self.muteLedOff()

  def mute(self):
    self.lcd.lines("Volume Muted","")

  def welcome(self):
    self.lcd.lines("Master " + chr(246) + " Control", "v0.1 Ronald Diaz")

  #
  # Convert [0 -> 100] :: [-63 -> 0] ; [0 -> 15]
  #
  def volumeConvert(self):
    # safe boundaries
    if self.vol100 < 0:
      self.vol100 = 0
    if self.vol100 > 100:
      self.vol100 = 100
    # todo: convert volume to decibal value
    self.vol63 = int(63 - float(self.vol100) * 0.63)
    self.vol15 = int((float(self.vol63) / 4) + 1)
    #self.vol100 = int(float(self.volumeLevel) * float(1.5873015873))
  
  #
  # [0 -> 100]
  #
  def volumeSet(self, vol):
    self.vol100 = vol
    self.volumeConvert()
    db = "%ddB" % self.vol_63
    db = db.rjust(10, " ")
    self.lcd.line1("Volume%s" % db)
    if self.vol100 == 0:
      self.lcd.line2(" ")
    else:
      self.lcd.line2("#" * self.vol15)

  #
  # Select 0 || 1
  #
  def select(self, s=True):
    if s == True:
      self.lcd.line1("     Media      ")
    else:
      self.lcd.line1("      MP3       ")
    if self.time_mode_seconds == True:
      self.lcd.line2(time.strftime(" %2d %b %H:%I:%S"))
    else:
      self.lcd.line2(time.stftime("%a %b %H:%I"))

