import time
#from ronniedAmp.display import Display
from ronniedAmp.scrollingText import ScrollingText

s = ScrollingText.Worker()
s.start()

#s.startBlink()

while True:
  print s.getText() 
  time.sleep(0.05)
    



