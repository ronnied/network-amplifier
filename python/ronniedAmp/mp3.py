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
    #self.
    self.volume = 0
    self.mute = False
    self.song = ""
    self.mpd = mpd.MPDClient()
    self.mpd.connect("localhost", 6600)  

  # High Level Commands
  def getStatus(self):
    return self.mpd.currentsong()

  def getSongPlaying(self):    
    return self.mpd.currentsong()

  def setVolume(self, volume):
    self.volume = volume
    self._updateVolume()
    
  def muteOn(self):
    self.mute = True

  def muteOff(self):
    self.mute = False
