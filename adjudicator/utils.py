from formula.SFBelief import SFBelief
from formula.Belief   import Belief

from time import time

# ShadowProver interface
import sys
sys.path.insert(1, '/pylibs/interface')
import interface

# base    -- List(Formula)
# formula -- Formula
# Add a formula to the base
# Checks if formula is already there first
def add_to_base(base, formula):
  if(not formula in base):
    base.append(formula)
    return True
  return False



# Returns a list of String representations of
# the formulae in base in which any SFBeliefs
# have had their annotations removed
# TODO This function doesn't handle SFBeliefs as sub-formulae
def remove_annotations(base):
  out = []
  for f in base:
    if isinstance(f, SFBelief): out.append(f.fstring_no_ann)
    else:                       out.append(f.fstring)

  return out



# Returns a list of String representations of
# the formulae in base in which any SFBeliefs
# have been removed
# TODO This function doesn't handle SFBeliefs as sub-formulae
def remove_sf_beliefs(base):
  return [str(f) for f in list(filter(lambda x : not isinstance(x, SFBelief), base))]



# Returns true if the assumption base contains inconsistent beliefs
# by casting Beliefs & SFBeliefs down their sub-formulae & attempting
# to prove zeta, a reserved symbol (hence, only provable if the base
# is inconsistent)
def inconsistent(base):
  new_base = []
  for f in base:
    if isinstance(f, SFBelief): new_base.append(str(f.formula))
    elif isinstance(f, Belief): new_base.append(str(f.formula))
    else:                       new_base.append(f.fstring)

  print("Calling ShadowProver...")
  consistency_check = interface.prove(new_base, "zeta")
  print("ShadowProver Done.")

  if(consistency_check == "FAILED"): return False
  else:                              return True



# assumptions -- List(String)
# goal        -- String
#
# Runs ShadowProver on the input and prints a String containing the output as well as timing
# Returns True if ShadowProver found a proof
#
def sp_time_test(assumptions, goal):
  start = time()
  out   = interface.prove(assumptions, goal)
  stop  = time()
  elapsed = stop - start

  if(out != "FAILED"):
    print("Proof found in " + str(elapsed) + " seconds.")
    print("PROOF OF: " + goal)
    print(out)
    return True

  print("Failed to find a proof in " + str(elapsed) + " seconds.")
  return False

