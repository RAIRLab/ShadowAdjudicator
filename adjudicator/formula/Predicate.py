from .Parser  import parse, parse_sexpr
from .Formula import Formula

# fstring       -- String        -- Original input string (e.g. (Happy john))
# justification -- Justification -- Links the formula to its justification
# name          -- String        -- Name of predicate (e.g. "Happy")
# args          -- List(Formula) -- Sub-formulae (arguments to proposition) (e.g. ["john"])
class Predicate(Formula):

  def __init__(self, fstring, justification):
    super().__init__(fstring, justification)

    args = parse_sexpr(fstring) # Parse s-expression
    self.name = args[0]
    args = args[1:]             # Remove proposition type (e.g. "and", "implies")

    # Recursively parse sub-formulae
    self.args = []
    for a in args:
      self.args.append(parse(a))



  def __str__(self):
    return super().__str__()



  def __eq__(self, other):
    return super().__eq__(other)



  def __hash__(self):
    return super().__hash__()
