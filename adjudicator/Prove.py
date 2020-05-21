# Functions for printing proof of goal formula

from formula.Formula import Formula
from expanders.SFModusPonens import sf_modus_ponens

def prove(base, goal):
  expanders = [sf_modus_ponens]

  progress = True
  while(progress):

    # Goal has been proved -- return proof
    if(goal in base):
      goal_proved = base[base.index(goal)] # Find goal_formula in base
      return generate_proof(goal_proved)

    progress = False

    # Try all expanders
    # If none of them are able to expand the base,
    # we're done
    for expand in expanders:
      if(expand(base)): progress = True

  return "FAILED"



def generate_proof(formula):
  return generate_proof_helper(formula, "")



def generate_proof_helper(formula, sep):

  if(formula.justification.isgiven):
    return sep + "GIVEN: " + str(formula) + "\n"

  else:
    out =  sep + "PROOF OF: " + str(formula) + "\n"
    out += sep + formula.get_justification() + "\n"

    sep += "  "                               # Increase indent
    justifier = formula.justification.formula # Formula(e) which justify formula

    if(isinstance(justifier, Formula)):             # If justification is a single formula
      out += generate_proof_helper(justifier, sep)  # Recursively output its justification

    else:                                      # If it's a list of formulae
      for f in formula.justification.formula: # Recursively output justifications of each formula       
        out += generate_proof_helper(f, sep)

    return out

