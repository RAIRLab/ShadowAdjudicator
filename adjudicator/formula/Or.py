from .Proposition import Proposition

# fstring -- String        -- Original input string
# args    -- List(Formula) -- Sub-formulae (arguments to proposition)
class Or(Proposition):

  def __init__(self, fstring):
    super().__init__(fstring)



  def __str__(self):
    return super().__str__()



  def __eq__(self, other):
    return super().__eq__(other)
