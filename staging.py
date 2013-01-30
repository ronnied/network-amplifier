#!/usr/bin/python
#
# CURRENT WORKING CONTROL Test Script for
# Raspberry Pi
#
# Author : Ronald Diaz
# Site   : http://www.ronalddiaz,net
# 
# Date   : 27/01/2013
#
from gaugette import rotary_encoder
from ronniedAmp import display, input#, controller
from time import sleep
import time
import wiringpi

class amplifier:
  def __init__(self):
    self.main_sleep = 0.05
    self.gpio = wiringpi.GPIO(wiringpi.GPIO.WPI_MODE_PINS)
    self.display = display.Display(self.gpio)
    self.input = input.Input(self.gpio)

    self.home_display_timer = 0
    self.home_display_threshold = 2
    self.start_home_display_timer = False

    self.mute_state = False
    self.select_state = True

    # Display init + Welcome
    sleep(0.25)
    self.display.welcome()
    sleep(0.5)
    self.display.home()

    self.do_main()

  def do_main(self):
    while True:

      # Check for home display timer trigger
      if self.start_home_display_timer == True:
        self.home_display_timer = time.time()
        self.start_home_display_timer = False
        #print "#"

      # Check for home display timeout
      if time.time() - self.home_display_timer > self.home_display_threshold:
        self.home_display_timer = 0
        self.display.home(self.select_state)

      self.check_volume_changes()
      self.check_select_state()
      self.check_mute_state()
      sleep(self.main_sleep)

  def check_select_state(self):
    if self.input.select_button.get_state() == True:
      self.select_media()
    else:
      self.input.select_led_off()

  def check_volume_changes(self):
    delta = self.input.volume.get_delta()
    if delta!=0:
      self.display.volume_delta(delta)
      self.start_home_display_timer = True

  def check_mute_state(self):
    if self.mute_state == True:
      self.start_home_display_timer = True
    if self.input.mute_button.get_state() == True:
      sleep(0.05)
      if self.input.mute_button.get_state() == True:
        self.mute_state = not self.mute_state
        if self.mute_state == True:
          self.mute_on()
        else:
          self.mute_off()
        while self.input.mute_button.get_state() == True:
          pass
        self.home_display_timer = time.time()

  def select_media(self):
    self.select_state = not self.select_state
    if self.select_state == True:
      self.display.home(1)
    else:
      self.display.home(0)
    self.input.select_led_on()
    while self.input.select_button.get_state() == True:
      pass
    self.home_display_timer = time.time()

  def mute_on(self):
    self.input.mute_led_on()
    self.display.mute()

  def mute_off(self):
    self.input.mute_led_off()
    self.display.volume_update_display()
    self.start_home_display_timer = False

if __name__ == '__main__':
  amp = amplifier()
  amp.do_main()

