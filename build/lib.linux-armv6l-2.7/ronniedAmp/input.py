import wiringpi
import gaugette.switch
import gaugette.rotary_encoder

class Input:
  def __init__(self, gpio):
    self.gpio = gpio

    # Select Button and LED
    self.select_button_pin = 2
    self.select_led_pin = 3
    self.select_button = gaugette.switch.Switch(self.select_button_pin)
    self.select_led = self.gpio.pinMode(3, self.gpio.OUTPUT)
    self.select_led_off()    

    # Mute Button and LED
    self.mute_button_pin = 7
    self.mute_led_pin = 0
    self.mute_button = gaugette.switch.Switch(self.mute_button_pin)
    self.mute_led = self.gpio.pinMode(0, self.gpio.OUTPUT)
    self.mute_led_off()

    # Rotary Volume
    self.vol_a = 13
    self.vol_b = 14
    self.volume = gaugette.rotary_encoder.RotaryEncoder.Worker(self.vol_a, self.vol_b)
    self.volume.start()
    
  def mute_led_on(self):
    self.led_mute(1)
  def mute_led_off(self):
    self.led_mute(0)
  def led_mute(self, s):
    self.led(self.mute_led_pin, s)

  def select_led_on(self):
    self.led_select(1)
  def select_led_off(self):
    self.led_select(0)
  def led_select(self, s):
    self.led(self.select_led_pin, s)

  def led(self, p, s):
    self.gpio.digitalWrite(p, s)
