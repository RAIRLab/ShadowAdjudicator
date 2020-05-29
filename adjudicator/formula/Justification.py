
# isgiven       -- Boolean                          -- True if formula is assumed, false otherwise
# proved_via_sp -- Booelan                          -- True if formula was proved using ShadowProver
# formula       -- List(Formula) || Formula || None -- Formula(e) used in proof (i.e. input to rule)
# rule          -- String                   || None -- Inference rule used. If proved_via_sp=True, this contains the ShadowProver output
class Justification:

  # Last two parameters are None if (isgiven == True)
  def __init__(self, isgiven, proved_via_sp=False, formula=None, rule=None):
    self.isgiven       = isgiven
    self.proved_via_sp = proved_via_sp
    self.formula       = formula
    self.rule          = rule



  def __str__(self):
    from .Formula import Formula

    if self.isgiven: return "GIVEN"

    elif isinstance(self.formula, Formula):

      if self.proved_via_sp:
        out = "Proved via ShadowProver:\n"
        out += self.rule
        out += "\n using " + str(self.formula)
        return out

      else: return "Applied " + self.rule + " to: " + str(self.formula)

    else:

      if self.proved_via_sp:
        out = "Proved via ShadowProver:\n"
        out += self.rule
        out += "\n using "

      else: out = "Applied '" + self.rule + "' to: "
      
      for f in self.formula:
        out += str(f) + "; "
      out = out[:len(out)-2] # Remove trailing separator
      return out


