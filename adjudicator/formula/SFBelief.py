from .Belief import Belief

# fstring        -- String        -- Original input string (e.g. (Believes!4 alice now phi))
# fstring_no_ann -- String        -- String form with no strength factor 
# justification  -- Justification -- Links the formula to its justification
# agent         -- String
# time          -- String
# formula       -- Formula       -- Sub-formula (object of modal operator)
class SFBelief(Belief):

  def __init__(self, fstring, justification):
    super().__init__(fstring, justification)

    try:
      self.strength = int(fstring[10])

    except ValueError:
      print("Improperly formatted SF belief (invalid strength factor)")
      exit()

    self.fstring_no_ann = fstring[:10] + fstring[11:]



  def __str__(self):
    return super().__str__()



  def __eq__(self, other):
    return super().__eq__(other)



  def __hash__(self):
    return super().__hash__()



### END CLASS DEFINITION ###

# Returns a new SFBelief object from arguments
# agent & time are strings
# formula is of type Formula (NOT a string)
# justification is a Justification object
def makeSFBelief(strength, agent, time, formula, justification):
  return SFBelief("(Believes!" + str(strength) + " " + agent + " " + time + " " + str(formula) + ")", justification)
