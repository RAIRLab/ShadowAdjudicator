from formula.SFBelief      import SFBelief
from formula.And           import And
from formula.Justification import Justification
from utils                 import add_to_base

# base is a list of Formula
# If the base contains a SFBelief with a conjunction as the sub-formulae,
#   this deduces each conjunct at the same strength
# Returns True if base was modified (i.e. rule was applied to a pair of formulae)
def sf_conj_elim(base):

  modifiedBase = False

  for formula in base:

    if(isinstance(formula, SFBelief)):
      sub = formula.formula

      if(isinstance(sub, And)):
        strength = formula.strength
        jus      = Justification(isgiven=False, formula=formula, schema="Conjunction elim through annotated belief")

        for conjunct in sub.args:
          belief = SFBelief.from_args(formula.agent, formula.time, conjunct, strength, jus)
          if(add_to_base(base, belief)): modifiedBase = True

  return modifiedBase

