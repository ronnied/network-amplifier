import pylirc
import threading
import time

class LircInput():

  # Threaded Worker    
  class Worker(threading.Thread):
    def __init__(self):
      threading.Thread.__init__(self)
      self.lock = threading.Lock()
      self.daemon = True
      self.MAIN_THREAD_DELAY = 0.01
      self.lircConnected = True
      try:
        self.sockid = pylirc.init("myamp", "/root/.lircrc")
        pylirc.blocking(0)
      except:
        print "error connecting to lircd!"
        self.lircConnected = False
      self.code = None
      
    def run(self):
      while True:
        if self.lircConnected == True:
          self.code = pylirc.nextcode(0)
        #print self.code
        time.sleep(self.MAIN_THREAD_DELAY)

    def getCode(self):
      return self.code
