from amplifier.displayHelper import DisplayHelper

######################################
#
# MP3 Display Class for LCD methods
#
# Ronald Diaz ronald@ronalddiaz.net
# 
class Mp3Display():
  def __init__(self):
    self.album = "Album Name"
    self.title = "Song Title Goes Here"
    self.artist = "Artist Name"
    self.helper = DisplayHelper()
    
  def getLine1(self):
    return self.helper.centerText(self.title)

  def getLine2(self):
    return self.artist + " - " + self.album + " . "

  def set(self, mp3):
    #print mp3
    try:
      self.album = mp3['album']
    except Exception, e:
      self.album = "album"

    try:
      self.title = mp3['title']
    except Exception, e:
      self.title = 'title'
    
    try:      
      self.artist = mp3['artist']
    except Exception, e:
      self.artist = 'artist'      