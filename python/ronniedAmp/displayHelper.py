######################################
#
# Display Helper Class for commonly
# used LCD methods.
#
# Ronald Diaz ronald@ronalddiaz.net
# 
class DisplayHelper:
  def __init__(self):
    return

  # x column text center
  def centerText(self, text, length=16):
    # get text length
    txtLen = len(text)
    #print "text length: ", txtLen

    # get length offset
    offset = (length - txtLen) / 2
    #print "text offset: ", offset

    # add offset
    buf = " " * offset + text
    #print "buf: ", buf
    
    # return buffer
    return buf