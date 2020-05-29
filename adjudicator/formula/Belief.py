from .Modal import Modal

# fstring       -- String        -- Original input string
# justification -- Justification -- Links the formula to its justification
# args          -- List(Formula) -- Sub-formulae (arguments to proposition)
class Belief(Modal):

  def __init__(self, fstring, justification):
    super().__init__(fstring, justification)



  def __str__(self):
    return super().__str__()



  def __eq__(self, other):
    return super().__eq__(other)



  def __hash__(self):
    return super().__hash__()



### END CLASS DEFINITION ###



# Returns a new Belief object from arguments
# agent & time are strings
# formula is of type Formula (NOT a string)
# justification is a Justification object
def makeBelief(agent, time, formula, justification):
  return Belief("(Believes! " + agent + " " + time + " " + str(formula) + ")", justification)
