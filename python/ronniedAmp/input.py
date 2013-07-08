import wiringpi
from ronniedAmp.toggleSwitch import ToggleSwitch
import gaugette.rotary_encoder
import threading
from time import sleep
import httplib2
import sys

class Input:
  def __init__(self, Controller): 
    
    # Buttons    
    self.sButton = ToggleSwitch(2) # GPIO PIN 2 # Select
    self.mButton = ToggleSwitch(7) # GPIO PIN 7 # Mute

    # Rotary Volume GPIO PINS 13 + 14    
    self.volume = gaugette.rotary_encoder.RotaryEncoder.Worker(13, 14)
    self.volume.start()
    self.delta = 0

    # Constants
    self.CONTROLLER = True
    self.HTTPCLIENT = False
    # Server address
    self.ControllerServerUrl = "http://127.0.0.1:8241/"    
            
    # Do we have a direct connection to the Controller object?
    self.controller = Controller      
    if self.controller != None: # typedef is better here...            
      self.client = self.CONTROLLER
    else:
      # Establish a HTTP Client connection to 
      # send messages to Controller Server
      self.http = httplib2.Http(".cache")
      self.client = self.HTTPCLIENT
      
  def selectToggle(self):
    if self.client == self.CONTROLLER:
      return self.controller.selectToggle()
    else:
      try:
        response, content = self.input.http.request(self.ControllerServerUrl + "set/selectToggle")
      except:
        print "couldn't connect to server :: ", sys.exc_info()[0]
        
  def muteToggle(self):
    if self.client == self.CONTROLLER:
      return self.controller.muteToggle()
    else:
      try:
        response, content = self.input.http.request(self.ControllerServerUrl + "set/muteToggle")
      except:
        print "couldn't connect to server :: ", sys.exc_info()[0]
        
  def volumeDelta(self, delta):
    if self.client == self.CONTROLLER:
      return self.controller.volumeDelta(delta)
    else:
      try:
        response, content = self.input.http.request(self.ControllerServerUrl + "set/volumeDelta/" + str(delta))
      except:
        print "couldn't connect to server :: ", sys.exc_info()[0]  
        
  # Threaded Worker    
  class Worker(threading.Thread):
    # cache prev state
    # signal on change state
    def __init__(self, Controller = None):
      threading.Thread.__init__(self)
      self.lock = threading.Lock()
      self.daemon = True
      
      # Decrease for greater resolution at the cost of cpu cycles
      self.MAIN_THREAD_DELAY = 0.01
      
      # Input resource
      self.input = Input(Controller)
      
    def run(self):        
      while True:
        
        # has the state of the select button toggled?
        if self.input.sButton.hasToggled() == True:
          #print "Select Toggle..."
          self.input.selectToggle()
          
        # has the state of the mute button toggled?
        if self.input.mButton.hasToggled() == True:
          #print "Mute Toggled..."
          self.input.muteToggle()

        # monitor the Volume for changes
        delta = self.input.volume.get_delta()
        if delta != self.input.delta and delta != 0:
          #print "volume: " + str(delta)
          self.input.volumeDelta(delta)

        # save all current states        
        sleep(self.MAIN_THREAD_DELAY)          
        