from .Justification import Justification

# fstring       -- String        -- Original input string
# justification -- Justification -- Links the formula to its justification
class Formula:

  def __init__(self, fstring, justification):
    self.fstring       = fstring
    self.justification = justification



  def __str__(self):
    return self.fstring



  def __eq__(self, other):
    return isinstance(other, Formula) and self.fstring == other.fstring



  def get_justification(self):
    return str(self.justification)
