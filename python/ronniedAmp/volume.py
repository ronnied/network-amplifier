# Deals with different
# volume scales required
# input is 0 -> 100
# outputs are dB and # for LCD  
class Volume():
  def __init__(self):
    self.vol15 = 0
    self.vol63 = -63
    self.vol100 = 0
  
  def set(self, vol):
    self.vol100 = vol
    self._convert()

  def get(self):
    return self.vol100

  def hash(self):
    if self.vol100 == 0:
      return " "
    return "#" * self.vol15

  def dB(self):
    return self.vol63
    
  # Convert [0 -> 100] :: [-63 -> 0] ; [0 -> 15]    
  def _convert(self):
    # is numeric
    try:
      float(self.vol100)
    except ValueError:
      self.vol100 = 0
    self.vol100 = int(self.vol100)
    # safe boundaries
    if self.vol100 < 0:
      self.vol100 = 0
    if self.vol100 > 100:
      self.vol100 = 100
    # todo: convert volume to decibal value
    self.vol63 = int(float(self.vol100) * 0.63) - 63
    #print "self.vol63 : " + str(self.vol63)
    self.vol15 = int((float(self.vol63) / 4) + 16)
    #print "self.vol15 : " + str(self.vol15)
  
