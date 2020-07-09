from formula.Predicate     import Predicate
from formula.And           import And
from formula.Justification import Justification
from utils                 import add_to_base

# base is a list of Formula
# If the base contains two Reasonableness predicates with the same left sub-formula
# and different right sub-formulas (which are not conjunctions -- in order to prevent,
# infinite application of this rule), this deduces the a Reasonableness predicate which
# states that the left sub-formula is more reasonable than the conjunction of the two
# right sub-formulae
# Returns True if base was modified (i.e. rule was applied to a pair of formulae)
def r_conj_intro(base):

  modifiedBase = False

  for formula in base:
    if(isinstance(formula, Predicate) and formula.name == "R"):
      for f in base:

        # If we find two Reasonableness predicates with the
        # same agent, time, and left sub-formula, and *different*
        # right sub-formulae (which are both not conjunctions)...
        if(isinstance(f, Predicate) and f.name == "R" and \
           formula.args[0] == f.args[0]               and \
           formula.args[1] == f.args[1]               and \
           formula.args[2] == f.args[2]               and \
           not isinstance(formula.args[3], And)       and \
           not isinstance(f.args[3], And)             and \
           not formula.args[3] == f.args[3]):

          # Deduce a Reasonablenes predicate where the right sub-formula is the conjunction of the two inputs
          jus = Justification(isgiven=False, formula=[formula, f], schema="Reasonableness Conjunction Intro")
          formula = Predicate.from_args("R", [f.args[0], f.args[1], f.args[2], And.from_args([formula.args[3], f.args[3]])], jus)

          if(add_to_base(base, formula)): modifiedBase = True

  return modifiedBase

