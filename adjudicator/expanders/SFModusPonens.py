from formula.SFBelief      import SFBelief
from formula.Implication   import Implication
from formula.Justification import Justification
from utils                 import add_to_base

# base is a list of Formula
# If the base contains a SFBelief with an implication as the sub-formula
#   and a SFBelief with the antecedent of that implication, this deduces
#   the consequent at the weaker strength (for-each)
# Returns True if base was modified (i.e. rule was applied to a pair of formulae)
def sf_modus_ponens(base):

  modifiedBase = False

  for formula in base:

    if(isinstance(formula, SFBelief)):
      subformula = formula.formula

      if(isinstance(subformula, Implication)):
        antecedent = subformula.args[0]
        consequent = subformula.args[1]

        for f in base:
          if(isinstance(f, SFBelief)):                                                                                        # If we find another SFBelief
            if(f.agent == formula.agent):                                                                                     # belonging to the same agent
              if(f.time == formula.time):                                                                                     # at the same time
                if(f.formula == antecedent):                                                                                  # with the antecedent of the implication
                  strength = min(formula.strength, f.strength)                                                                # take the minimum strength
                  jus      = Justification(isgiven=False, formula=[formula, f], schema="Modus ponens through annotated belief")
                  belief   = SFBelief.from_args(f.agent, f.time, consequent, strength, jus)                                   # and generate an SFBelief in the consequent
                  if(add_to_base(base, belief)): modifiedBase = True                                                          # Then add it if it is not already in the base

  return modifiedBase

