from twisted.web import server, resource
from twisted.internet import reactor
from pprint import pprint
import ronniedAmp.display

class DisplayResource(resource.Resource):
  isLeaf = True
  numberRequests = 0
  display = ronniedAmp.display.Display()
  print "amplifier display server started"

  def render_GET(self, request):
    self.numberRequests +=  1

    # translate get
    self.translateGet(request)

    # output result
    request.setHeader("content-type", "text/plain")
    return "I am request #" + str(self.numberRequests) + "\n"

  def translateGet(self, get):
    path = (get.__dict__)["path"]
    seg = path.split("/")
    #print seg
    #print seg[1]
   
    if seg[1] == "lcd":
      self.route_lcd_command(seg) 
    elif seg[1] == "led":
      self.route_led_command(seg)

  def route_led_command(self, seg):
    # command to switch
    sw = seg[2]
    print sw
    if sw == "mute_on":
      self.display.mute_on()
    elif sw == "mute_off":
      self.display.mute_off()
    elif sw == "select_on":
      self.display.select_on()
    elif sw == "select_off":
      self.display.select_off()
    else:
      print "LED command unknown: " + str(sw)
 
  def route_lcd_command(self, seg):
    # command to switch
    sw = seg[2]
    print sw
    if sw == "welcome":
      self.display.welcome()
    elif sw == "select_mp3":
      self.display.home(0)
    elif sw == "select_media":
      self.display.home(1)
    elif sw == "lines":
      self.display.lcd_lines(seg[3], seg[4])
    elif sw == "vol_set":
      self.display.volume_set(int(seg[3]))
    elif sw == "volume_update":
      self.display.volume_update_display()
    else:
      print "LCD command unknown: " + str(sw)


reactor.listenTCP(8080, server.Site(DisplayResource()))
reactor.run()

