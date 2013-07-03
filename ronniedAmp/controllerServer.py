from twisted.web.resource import Resource
from ronniedAmp.controller import Controller
from ronniedAmp.input import Input

# Control Server just delegates
# messages interpreted to the
# Controller Resource
#
class ControllerServer(Resource):

  print "amplifier controller server started"            
  isLeaf = True
  
  # Controller Resource
  controller = Controller()
  #controller.powerOn()
  
  # Input Resource - direct connection to Controller object
  input = Input.Worker(controller)
  input.start()
  
  def render_GET(self, request):      
    request.setHeader("content-type", "application/json")
    return self.translateGET(request)

  def translateGET(self, get):
    path = (get.__dict__)["path"]
    seg = path.split("/")
    print seg #print seg[1]
    if seg[1] == "set":
      return self.routeSet(seg) 
    elif seg[1] == "get":
      return self.routeGet(seg)
    else:
      return "Error"

  ########################################################  
  # Delegate incoming set  
  def routeSet(self, seg):
      
    # command to switch
    sw = seg[2]
    #print sw
    
    # High level commands
    #
    if sw == "muteToggle":
      return self.controller.muteToggle() 
    if sw == "muteOn":      
      return self.controller.muteOn()
    elif sw == "muteOff":
      return self.controller.muteOff()
    elif sw == "selectToggle":
      return self.controller.selectToggle()            
    elif sw == "selectMedia" or sw == "select0": 
      return self.controller.selectMedia()
    elif sw == "selectMp3" or sw == "select1":
      return self.controller.selectMp3()
    elif sw == "volume":
      volume = 0
      try:
        volume = seg[3]
      except ValueError:
        volume = 0
      return self.controller.volumeSet(volume)
    elif sw == "volumeDelta":
      delta = 0
      try:
        delta = seg[3]
      except ValueError:
        delta = 0
      return self.controller.volumeDelta(delta)
    elif sw == "powerOn":
      return self.controller.powerOn()
    elif sw == "powerOff":
      return self.controller.powerOff()
    elif sw == "bass":
      bass = 0
      try:
        bass = seg[3]
      except ValueError:
        bass = 0
      return self.controller.bassSet(bass)
    elif sw == "treble":
      treble = 0
      try:
        treble = seg[3]
      except ValueError:
        treble = 0
      return self.controller.trebleSet(treble)

    # Granular commands
    #            
    else:
      error = "Unknown command: " + str(sw)
      #print error
      return error

  ########################################################  
  # Delegate incoming get    
  def routeGet(self, seg):
    # command to switch
    sw = seg[2]
    #print sw
    
    # High level commands
    #
    if sw == "all":
      return self.controller.getAll()       
    else:
      msg = "not implemented"
      #print msg
      return msg


