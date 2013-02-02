#from ronniedAmp.controller import Controller
#c = Controller()
#print c
#c.powerOn()

#from ronniedAmp.scrollingText import ScrollingText
#from time import sleep
#
#from ronniedAmp.lcd import HD44780
#
#l = HD44780()
#s = ScrollingText.Worker()
#s.start()
#
#s2 = ScrollingText.Worker(text="It's the second line text now scrolling at a theatre near you :)         ", direction = False, speed = 0.2)
#s2.start()
#
#while True:
#  #print s.getText()  
#  l.message(s.getText() + "\n" + s2.getText())  
#  sleep(0.02)


#d.setLine1("Line one for the win :) More text to scroll...    ")
#d.startScrollLine1()

    
from ronniedAmp.display import Display
from time import sleep

d = Display.Worker()
d.start()
print d

vol = 0
#d.disp.lcd.init()

print "about to sleep for 10 seconds"
sleep(10)

d.showMp3()

while True:      
    print "."
    
    #d.showVolume()
    #sleep(5)
                    
    d.muteOn()
    sleep(10)    
    
    d.muteOff()
    sleep(10)
            
    #vol = vol + 10
    #d.setVolume(vol)    
    
    