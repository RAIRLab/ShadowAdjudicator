
# isgiven -- Boolean                          -- True if formula is assumed, false otherwise
# formula -- List(Formula) || Formula || None -- Formula(e) used in proof (i.e. input to rule)
# rule    -- String                           -- Inference rule used
class Justification:

  # Last two parameters are None if (isgiven == True)
  def __init__(self, isgiven, formula=None, rule=None):
    self.isgiven = isgiven
    self.formula = formula
    self.rule    = rule



  def __str__(self):
    from .Formula import Formula
    if   self.isgiven:                      return "GIVEN"
    elif isinstance(self.formula, Formula): return "Applied " + self.rule + " to: " + str(self.formula)
    else:
      out = "Applied '" + self.rule + "' to: "
      for f in self.formula:
        out += str(f) + "; "
      out = out[:len(out)-2] # Remove trailing separator
      return out


