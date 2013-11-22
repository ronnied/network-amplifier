import mpd
import time

######################################
#
# Class for controlling MPDaemon
#
# Ronald Diaz ronald@ronalddiaz.net
#
# Todo
# sets: no delay, send request to mpd daemon
# gets: run worker to cache mpd daemon data
# at a regular timely rate, return cache
#
class Mp3:
  def __init__(self):
    self.currentsong = False
    self.mpd = False    
    self.connect()
          
  # High Level Commands
  def connect(self):
    try:
      self.mpd = mpd.MPDClient()
      self.mpd.connect("localhost", 6600)
      # Check response from port is correct: OK MPD 0.17.0
    except:
      self.mpd = False

  def getStatus(self):  
    if self.mpd == False:
      return self.currentsong
    try:
      self.currentsong = self.mpd.currentsong()
    except:      
      return False
    return self.currentsong      