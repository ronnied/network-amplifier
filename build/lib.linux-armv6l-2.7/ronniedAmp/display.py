import gaugette.lcd
import time

class Display:
  def __init__(self, gpio):
    self.LCD = gaugette.lcd.Lcd(gpio)
     
    # Volume Setup
    self.volume_level = 0
    self.vol_100 = 0
    self.vol_63 = -63
    self.vol_15 = 0

    # Time Setup
    self.time_mode_seconds = True

  def mute(self):
    self.LCD.lcd_lines("Volume Muted","")

  def welcome(self):
    self.LCD.lcd_lines("Master " + chr(246) + " Control", "v0.1 Ronald Diaz")

  def volume_delta(self, delta=0):
    self.volume_level = self.volume_level + (delta / 2)
    self.volume_calculate()
    self.volume_update_display()

  def volume_down(self, delta=2):
    self.volume_level = self.volume_level - (delta / 2)
    #self.volume_level = self.volume_level - 1
    self.volume_calculate()
    self.volume_update_display()

  def volume_up(self, delta=2):
    self.volume_level = self.volume_level + (delta / 2)
    #self.volume_level = self.volume_level + 1
    self.volume_calculate()
    self.volume_update_display()

  def volume_calculate(self):
    # safe boundaries
    if self.volume_level < 0:
      self.volume_level = 0
    if self.volume_level > 63:
      self.volume_level = 63
    # convert volume to decibal value
    self.vol_63 = self.volume_level - 63
    self.vol_15 = (self.volume_level / 4) + 1
    self.vol_100 = self.volume_level * (100 / 63)

  # Volume 0 < 63
  def volume_set(self, volume):
    self.volume_level = volume
    self.volume_calculate()
    self.volume_update_display()
    
  # Update the LCD with Volume
  #
  def volume_update_display(self):
    db = "%ddB" % self.vol_63
    db = db.rjust(10, " ")
    self.LCD.lcd_line_1("Volume%s" % db)
    if self.volume_level == 0:
      self.LCD.lcd_line_2(" ")
    else:
      self.LCD.lcd_line_2("#" * self.vol_15)

  # Display the Home Screen
  #
  def home(self, selected=True):
    if selected == True:
      self.LCD.lcd_line_1("     Media      ")
    else:
      self.LCD.lcd_line_1("      MP3       ")
    if self.time_mode_seconds == True:
      self.LCD.lcd_line_2(time.strftime(" %2d %b %H:%I:%S"))
    else:
      self.LCD.lcd_line_2(time.stftime("%a %b %H:%I"))

