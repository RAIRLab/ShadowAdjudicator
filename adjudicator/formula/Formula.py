
# fstring -- String -- Original input string
class Formula:

  def __init__(self, fstring):
    self.fstring = fstring



  def __str__(self):
    return self.fstring



  def __eq__(self, other):
    return isinstance(other, Formula) and self.fstring == other.fstring
