# Functions for generating proofs
# (Both finding a proof and printing it)

from formula.Formula         import Formula
from expanders.SFModusPonens import sf_modus_ponens
from expanders.SFConjElim    import sf_conj_elim

INDENT   = "  "  # Amount of indent for sub-parts of proofs
SPINDENT = "-->" # Indent to indicate ShadowProver portion of proof

# Attempts to prove a Formula goal given a list of
# assumptions base.
# expanders is a list of function callers which (attempt to)
# apply annotated modal inference schemeata to the formulae
# in the assumption base
# If levels=None, only expanders are used.
# Otherwise, level_provers is a list of functions which use SP to prove level definitions
#            level_exp     is a list of functions which check the assumption base for the definition
# functions
def prove(base, goal, expanders=[sf_modus_ponens, sf_conj_elim], level_provers=None, level_exp=None):

  progress = True

  while(progress):

    # Goal has been proved -- return proof
    if(goal in base):
      goal_proved = base[base.index(goal)] # Find goal_formula in base
      return generate_proof(goal_proved, base)

    progress = False

    # Try all level definitions, if given
    if(not level_provers == None):
      for level in level_provers:
        if(level(base, goal)): progress = True

    # Try all level expanders, if given
    if(not level_exp == None):
      for level in level_exp:
        if(level(base)): progress = True

    # Try all expanders
    for expand in expanders:
      if(expand(base)): progress = True


  # If all level definitions & expanders
  # failed to return any new formulae, we're done
  return "FAILED"



def generate_proof(formula, base):
  return generate_proof_helper(formula, base, "")



def generate_proof_helper(formula, base, sep):

  if(formula.justification.isgiven):
    return sep + "GIVEN: " + str(formula) + "\n"

  else:
    out = sep + "PROOF OF: " + str(formula) + "\n"

    justifier = formula.justification.formula # Formula(e) which justify formula

    # If proved using ShadowProver...
    if(formula.justification.proved_via_sp):
      out += sep + "Proved via ShadowProver:\n"
      out += sep + SPINDENT + formula.justification.rule.replace("\n", "\n"+sep+SPINDENT) + "\n" # Format SP output

      # "Hacky" way to trace which assumptions ShadowProver used which may not
      # have been givens (i.e. they were proved by a combination of ShadowAdjudicator
      # rules and previous calls to ShadowProver)
      sep += INDENT
      sp_out_sanitized = " ".join(formula.justification.rule.split())
      for f in base:
        if(str(f) in sp_out_sanitized):              # If a formula in the base appears in the ShadowProver output
          out += generate_proof_helper(f, base, sep) # generate a proof of it
      return out

    # If proved using ShadowAdjudicator...
    else: out += sep + formula.get_justification() + "\n"

    sep += INDENT                                   # Increase indent

    if(isinstance(justifier, Formula)):                   # If justification is a single formula
      out += generate_proof_helper(justifier, base, sep)  # Recursively output its justification

    else:                                     # If it's a list of formulae
      for f in formula.justification.formula: # Recursively output justifications of each formula       
        out += generate_proof_helper(f, base, sep)

    return out


