import mpd
import time

######################################
#
# Class for controlling MPDaemon
#
# Ronald Diaz ronald@ronalddiaz.net
#
class Mp3:
  def __init__(self):      
    try:
      self.mpd = mpd.MPDClient()
      self.mpd.connect("localhost", 6600)
    except:
      self.mpd = False
              
  # High Level Commands
  def getStatus(self):
    if self.mpd != False:
      return self.mpd.currentsong()
    return False

  def getSongPlaying(self):
    if self.mpd != False:
      return self.mpd.currentsong()
    return False