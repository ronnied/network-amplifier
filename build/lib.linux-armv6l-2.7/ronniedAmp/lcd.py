import gaugette.lcd
import time

class Lcd:
  def __init__(self):
    self.LCD = gaugette.lcd.Lcd()
    self.welcome()
    time.sleep(1)
    self.home()
     
    # Volume Setup
    self.volume_level = 0
    self.vol_63 = -63
    self.vol_15 = 0

  def mute(self):
    self.LCD.lcd_lines("Volume Muted","")

  def welcome(self):
    self.LCD.lcd_lines("Master " + chr(246) + " Control", "v0.1 Ronald Diaz")

  def volume_delta(self, delta=0):
    self.volume_level = self.volume_level + (delta / 2)
    self.volume_calculate()
    self.volume_update_display()

  def volume_down(self, delta=1):
    self.volume_level = self.volume_level - (delta / 2)
    #self.volume_level = self.volume_level - 1
    self.volume_calculate()
    self.volume_update_display()

  def volume_up(self, delta=1):
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
  def home(self):
    self.LCD.lcd_lines("     Media      ", "Mon 02 May 22:22")
