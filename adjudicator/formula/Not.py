from .Proposition import Proposition

# fstring -- String        -- Original input string
# justification -- Justification -- Links the formula to its justification
# args    -- List(Formula) -- Sub-formulae (arguments to proposition)
class Not(Proposition):

  def __init__(self, fstring, justification):
    super().__init__(fstring, justification)



  def __str__(self):
    return super().__str__()



  def __eq__(self, other):
    return super().__eq__(other)



  def __hash__(self):
    return super().__hash__()
