import time
#
# Basic Timer class
# Holds it's on state
#
# Ronald Diaz <ronald@ronalddiaz.net>
# http://github.com/ronnied
#
class Timer():
  def __init__(self, timeout=1, state=True):
    self.state = state
    self.timeout = timeout
    self.timer = time.time()
  def elapsed(self):
    if time.time() - self.timer > self.timeout:
      return True
    else:
      return False
  def start(self):
    self.reset()
    self.state = True
  def stop(self):
    self.state = False
  def isOn(self):
    return self.state
  def reset(self):
      self.timer = time.time()