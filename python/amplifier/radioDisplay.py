from amplifier.displayHelper import DisplayHelper

######################################
#
# Radio Display Class for LCD methods
#
# Ronald Diaz ronald@ronalddiaz.net
# 
class RadioDisplay():
  def __init__(self):
    self.index = 0
    self.name = ""
    self.frequency = ""
    self.description = "" 
    self.helper = DisplayHelper()
    
  def getLine1(self):
    return self.helper.centerText(self.name)

  def getLine2(self):
    return self.description + " - "

  def set(self, station):
    #print station
    self.index = station['index']
    self.name = station['name']
    self.frequency = station['frequency']
    self.description = station['description']