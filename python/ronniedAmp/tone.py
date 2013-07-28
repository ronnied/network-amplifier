# Calucates the tone chars
# for the lcd display
#
# B-------I-------
# T#######I-------
#
# B-------I######-
# T-------I###---- 
#
# (-14 -> 14) -> + 14 / 2 = (0->14)
# 
class Tone():
  def __init__(self):
    self.bass = 0
    self.treble = 0
  
  def set(self, bass, treble):
    self.bass = bass
    self.treble = treble
    self._convert()

  def hashBass(self):
    return "B" + self.hash(self.bass)

  def hashTreble(self):
    return "T" + self.hash(self.treble)

  def hash(self, x):
    #print x
    if int(x) > 7:
      #print "> 7"
      return ("-" * 7) + "I" + ("#" * (int(x) - 7)) + ("-" * (14 - int(x)))
    else:
      #print "< 7"
      return ("-" * int(x)) + ("#" * (7 - int(x))) + "I" + ("-" * 7)
      
  # Convert [-14 -> 14] :: [0 -> 14]    
  def _convert(self):
    #print "convert"
    #print "bass: " + str(self.bass)
    #print "treble: " + str(self.treble)
    # is numeric
    try:
      float(self.bass)
      float(self.treble)
    except ValueError:
      print "error!"
      self.bass = 0
      self.treble = 0
    self.bass = int(self.bass)
    self.treble = int(self.treble)
    # safe boundaries
    if self.bass < -14:
      self.bass = 0
    if self.bass > 14:
      self.bass = 0
    if self.treble < -14:
      self.treble = 0
    if self.treble > 14:
      self.treble = 0
    # convert to positive int
    self.bass =  int((float(self.bass) / 2) + 7) 
    self.treble =  int((float(self.treble) / 2) + 7) 
