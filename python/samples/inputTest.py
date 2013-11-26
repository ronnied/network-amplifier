#
# Test the input threaded worker
#
from amplifier.input import Input
import time
i = Input.Worker() # no controller passed in will use the web server instead
i.start()
print i

while True:
  time.sleep(5)
  print "."
