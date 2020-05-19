from formula.SFBelief import SFBelief, makeSFBelief
from formula.Implication import Implication

# base is a list of Formula
# If the base contains a SFBelief with an implication as the sub-formula
#   and a SFBelief with the antecedent of that implication, this deduces
#   the consequent at the weaker strength (for-each)
def sf_modus_ponens(base):

  for formula in base:

    if(isinstance(formula, SFBelief)):
      subformula = formula.formula

      if(isinstance(subformula, Implication)):
        antecedent = subformula.args[0]
        consequent = subformula.args[1]

        for f in base:
          if(isinstance(f, SFBelief)):                                   # If we find another SFBelief
            if(f.agent == formula.agent):                                # belonging to the same agent
              if(f.time == formula.time):                                # at the same time
                if(f.formula == antecedent):                             # with the antecedent of the implication
                  strength = min(formula.strength, f.strength)           # take the minimum strength
                  base.append(makeSFBelief(strength, f.agent, f.time, consequent)) # and generate an SFBelief in the consequent

