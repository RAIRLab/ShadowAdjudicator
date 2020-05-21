from .Parser  import parse
from .Formula import Formula

# fstring       -- String        -- Original input string
# justification -- Justification -- Links the formula to its justification
# args          -- List(Formula) -- Sub-formulae (arguments to proposition)
class Proposition(Formula):

  def __init__(self, fstring, justification):
    super().__init__(fstring, justification)

    args = fstring.split()[1:] # Remove proposition type
    args[len(args)-1] = args[len(args)-1][:-1] # Remove trailing paren from last arg

    # Recursively parse sub-formulae
    self.args = []
    for a in args:
      self.args.append(parse(a))



  def __str__(self):
    return super().__str__()



  def __eq__(self, other):
    return super().__eq__(other)
