from formula.Perception    import Perception
from formula.SFBelief      import SFBelief
from formula.Implication   import Implication
from formula.Justification import Justification
from utils                 import add_to_base

# base is a list of Formula
# Expands any perception formulae into evident beliefs
# Returns True if base was modified (i.e. rule was applied to at least one formula)
def perception_to_evident_belief(base):

  modifiedBase = False

  perceptions = filter(lambda x : isinstance(x, Perception), base)

  for f in perceptions:
    jus      = Justification(isgiven=False, formula=[f], schema="Perception => Evident Belief")
    belief   = SFBelief.from_args(f.agent, f.time, f.formula, 4, jus)                           # Generate an SFBelief in the perceived formula at level-4 "evident"
    if(add_to_base(base, belief)): modifiedBase = True                                          # Then add it if it is not already in the base

  return modifiedBase

