import wiringpi
from amplifier.toggleSwitch import ToggleSwitch
from amplifier.lircInput import LircInput
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

    # LIRC Input
    self.lirc = LircInput.Worker()
    self.lirc.start()

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

  def networkRequest(self, cmd):
    try:
      response, content = self.input.http.request(self.ControllerServerUrl + cmd)
    except:
      print "couldn't connect to server :: ", sys.exc_info()[0]
    return content
      
  def powerOff(self):
    if self.client == self.CONTROLLER:
      return self.controller.powerOff()
    return self.networkRequest("set/powerOff")

  def selectToggle(self):
    if self.client == self.CONTROLLER:
      return self.controller.selectToggle()
    return self.networkRequest("set/selectToggle")
        
  def muteToggle(self):
    if self.client == self.CONTROLLER:
      return self.controller.muteToggle()
    return self.networkRequest("set/muteToggle")
        
  def volumeDelta(self, delta):
    if self.client == self.CONTROLLER:
      return self.controller.volumeDelta(delta)
    return self.networkRequest("set/volumeDelta/" + str(delta))

  def volumeUp(self):
    if self.client == self.CONTROLLER:
      return self.controller.volumeUp()
    return self.networkRequest("set/volumeUp")
  
  def volumeDown(self):
    if self.client == self.CONTROLLER:
      return self.controller.volumeDown()
    return self.networkRequest("set/volumeDown")

  def selectAux(self):
    if self.client == self.CONTROLLER:
      return self.controller.selectAux()
    return self.networkRequest("set/selectAux")
  
  def selectMp3(self):
    if self.client == self.CONTROLLER:
      return self.controller.selectMp3()
    return self.networkRequest("set/selectMp3")

  def selectRadio(self):
    if self.client == self.CONTROLLER:
      return self.controller.selectRadio()
    return self.networkRequest("set/selectRadio")

  def selectMedia(self):
    if self.client == self.CONTROLLER:
      return self.controller.selectMedia()
    return self.networkRequest("set/selectMedia")

  def getStateString(self):
    if self.client == self.CONTROLLER:
      return self.controller.getStateString()
    return self.networkRequest("get/stateString")

  def radioStationNext(self):
    if self.client == self.CONTROLLER:
      return self.controller.radioStationNext()
    return self.networkRequest("set/radioStationNext")
 
  def radioStationPrevious(self):
    if self.client == self.CONTROLLER:
      return self.controller.radioStationPrevious()
    return self.networkRequest("set/radioStationPrevious")
 
  def mp3Previous(self):
    if self.client == self.CONTROLLER:
      return self.controller.mp3Previous()
    return self.networkRequest("set/mp3Previous")
 
  def mp3Next(self):
    if self.client == self.CONTROLLER:
      return self.controller.mp3Next()
    return self.networkRequest("set/mp3Next")
 
  def mp3Stop(self):
    if self.client == self.CONTROLLER:
      return self.controller.mp3Stop()
    return self.networkRequest("set/mp3Stop")
 
  def mp3Play(self):
    if self.client == self.CONTROLLER:
      return self.controller.mp3Play()
    return self.networkRequest("set/mp3Play")
  
  def mp3Pause(self):
    if self.client == self.CONTROLLER:
      return self.controller.mp3Pause()
    return self.networkRequest("set/mp3Pause")
 
  def handleLircCode(self, code):
    print "got code: " + str(code)
    if code[0] == 'mute':
      return self.muteToggle()
    if code[0] == 'up':
      return self.volumeUp()
    if code[0] == 'down':
      return self.volumeDown()
    if code[0] == 'red':
      return self.selectAux()
    if code[0] == 'green':
      return self.selectMp3()
    if code[0] == 'yellow':
      return self.selectRadio()
    if code[0] == 'blue':
      return self.selectMedia()
    if code[0] == 'stop' and self.getStateString() == "mp3":
      return self.mp3Stop()
    if code[0] == 'play' and self.getStateString() == "mp3":
      return self.mp3Play()
    if code[0] == 'pause' and self.getStateString() == "mp3":
      return self.mp3Pause()
    if code[0] == 'power':
      pass
    if code[0] == 'back':
      selected = self.getStateString()
      if selected == "radio":
        return self.radioStationPrevious()
      if selected == "mp3":
        return self.mp3Previous()
    if code[0] == 'forward':
      selected = self.getStateString()
      if selected == "radio":
        return self.radioStationNext()
      if selected == "mp3":
        return self.mp3Next()
        
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
        # have both buttons being pushed at the same time?
        if self.input.sButton.get_state() == True and self.input.mButton.get_state() == True:
          # print "Shutting down..."
          self.input.powerOff()

        # has the state of the select button toggled?
        if self.input.sButton.hasToggled() == True:
          # print "Select Toggle..."
          self.input.selectToggle()
          
        # has the state of the mute button toggled?
        if self.input.mButton.hasToggled() == True:
          # print "Mute Toggled..."
          self.input.muteToggle()

        # monitor the Volume for changes
        delta = self.input.volume.get_delta()
        if delta != self.input.delta and delta != 0:
          #print "volume: " + str(delta)
          self.input.volumeDelta(delta)

        # monitor lirc for changes
        lircCode = self.input.lirc.getCode()
        if lircCode != None or lircCode == "None":
          self.input.handleLircCode(lircCode)

        # save all current states        
        sleep(self.MAIN_THREAD_DELAY)
