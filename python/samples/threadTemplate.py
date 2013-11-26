import threading
import time

class SomeClass:
  def __init__(self, something):
    self.something = something

  # Threaded Worker
  class Worker(threading.Thread):
    # cache prev state
    # signal on change state
    def __init__(self, something = None):
      threading.Thread.__init__(self)
      self.lock = threading.Lock()
      self.daemon = True
      self.MAIN_THREAD_DELAY = 0.05

      # Input resource
      self.s = SomeClass()

    def run(self):
      while True:
        # do stuff
        # self.s.someMethod()
        time.sleep(self.MAIN_THREAD_DELAY)
