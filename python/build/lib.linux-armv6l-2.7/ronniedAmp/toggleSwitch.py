from gaugette.switch import Switch
import time

class ToggleSwitch(Switch):
  def __init__(self, pin):
    Switch.__init__(self, pin)
    self.toggleOn = False 
    self.lastState = self.get_state()
    #print "init state: " + str(self.lastState)

  def hasChanged(self):
    # compare cached state to now
    if self.lastState != self.get_state():
      # debounce
      time.sleep(0.01)
      if self.lastState != self.get_state():
        #print "Toggle Switch Changed: " + str(self.get_state())
        # pushed down? or let go?
        if self.get_state() == True:
          # significant, flip the buffer
          self.toggleOn = not self.toggleOn
        else:
          # meh, we don't toggle when button is let go
          pass
      # either way, there was a change so
      self.lastState = self.get_state()
      return True
    else:
      return False
  
  def hasToggled(self):
    lastToggle = self.toggleOn
    self.hasChanged()
    if lastToggle != self.toggleOn:
      #print "hasToggled"
      return True
    return False