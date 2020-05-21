from .Parser  import parse
from .Formula import Formula

# fstring       -- String        -- Original input string
# justification -- Justification -- Links the formula to its justification
# args          -- List(Formula) -- Sub-formulae (arguments to proposition)
class Modal(Formula):

  def __init__(self, fstring, justification):

    super().__init__(fstring, justification)

    # Split off the agent and time, leaving the sub-formula intact
    args = fstring.split(maxsplit=3)

    self.agent = args[1]
    self.time  = args[2]
    self.formula = parse(args[3][:-1]) # Pass sub-formulae to parse



  def __str__(self):
    return super().__str__()



  def __eq__(self, other):
    return super().__eq__(other)
