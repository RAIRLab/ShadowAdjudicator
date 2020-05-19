from .Belief import Belief

# fstring -- String        -- Original input string (e.g. (Believes!4 alice now phi))
# args    -- List(Formula) -- Sub-formulae (arguments to proposition)
class SFBelief(Belief):

  def __init__(self, fstring):

    super().__init__(fstring)

    try:
      self.strength = int(fstring[10])

    except ValueError:
      print("Improperly formatted SF belief (invalid strength factor)")
      exit()



  def __str__(self):
    return super().__str__()



  def __eq__(self, other):
    return super().__eq__(other)


### END CLASS DEFINITION ###

# Returns a new SFBelief object from arguments
# agent & time are strings
# formula is of type Formula (NOT a string)
def makeSFBelief(strength, agent, time, formula):
  return SFBelief("(Believes!" + str(strength) + " " + agent + " " + time + " " + str(formula) + ")")