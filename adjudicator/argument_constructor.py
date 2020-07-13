# Functions for generating arguments
# (Both finding arguments and constructing String forms of them)

from formula.Formula         import Formula
from formula.SFBelief        import SFBelief
from formula.Justification   import Justification
from expanders.SFModusPonens import sf_modus_ponens
from expanders.SFConjElim    import sf_conj_elim
from utils                   import add_to_base, remove_annotations, remove_sf_beliefs, inconsistent

# ShadowProver interface
import sys
sys.path.insert(1, '/pylibs/interface')
import interface

INDENT   = "  "  # Amount of indent for sub-parts of arguments
SPINDENT = "-->" # Indent to indicate ShadowProver portion of argument

# base                   -- List(Formula)
# goal                   -- Formula
# expanders              -- List(Function Handle)
# level_arg_constructors -- List(Function Handle) || None
#
# Attempts to construct an argument for the goal given the list of assumptions in base.
#
# The functions in expanders attempt to apply annotated modal inference schemata to the formulae in base
# The functions in level_arg_constructors attempt to apply the definition of a Strength Factors level to
# the goal. The specific definitions depends on the specification of Strength Factors that are used.
# Several have been specified in various papers, and a subset of those have been implemented.
#
def construct_argument(base, goal, expanders=[sf_modus_ponens, sf_conj_elim], level_arg_constructors=None):

  progress = True

  while(progress):

    # An argument for the goal has been constructed -- return argument
    if(goal in base):
      goal_found = base[base.index(goal)] # Find goal_formula in base
      return generate_argument_string(goal_found, base)

    progress = False

    # Try all level definitions, if given
    if(not level_arg_constructors == None):
      for level in level_arg_constructors:
        if(level(base, goal)): progress = True

    # Try all expanders
    for expand in expanders:
      if(expand(base)): progress = True


  # If all level definitions & expanders
  # failed to return any new formulae, we're done
  return "FAILED"



# base       -- List(Formula)
# goal       -- SFBelief 
# definition -- Formula
# def_name   -- String                -- e.g. "Level-1 Definition"
# full_def   -- Formula || None
# subs       -- List(Formula) || None
# 
# Function calls ShadowProver, attempting to prove the definition of the level of the belief of the goal
# If the definition is successfully proved by ShadowProver, this function adds
# the goal and definition to the assumption base
#
# full_def is specified when the definition includes annotated beliefs which cannot be passed to ShadowProver
# It is assumed by this function that definition contains the non-annotated subset of full_def, and that an
# argument has already been constructed for the annotated sub-formulae of full_def by calls to ShadowAdjudicator functions
#
# subs is a list of Formula containing those sub-formulae with annotations
#
def level_arg_constructor(base, goal, definition, def_name, full_def=None, subs=None):

  # remove_annotations has no effect on base if no SFBeliefs; but it does
  # still perform the conversion to strings for input to ShadowProver
  sp_base = remove_annotations(base)
  sp_def  = str(definition)

  print("Calling ShadowProver...", flush=True)
  out = interface.prove(sp_base, sp_def)
  print("ShadowProver Done.", flush=True)

  if(not out=="FAILED"):

    # Only need to check for inconsistency if there are SFBeliefs in the base
    need_consist_check = any(isinstance(f, SFBelief) for f in base)

    # If the assumption base contains inconsistent beliefs...
    if(need_consist_check and inconsistent(base)):
      sp_base = remove_sf_beliefs(base)       # Remove all SFBeliefs
      print("Calling ShadowProver...", flush=True)
      out = interface.prove(sp_base, sp_def)  # And try again
      print("ShadowProver Done.", flush=True)
      if(out == "FAILED"): return False       # And if SP can't find a proof, return False

    # If it reaches here, either SP found a proof and the assumption base was consistent,
    # or it was inconsistent but SP was able to find a proof without contradictory SFBeliefs

    if(full_def == None):
      definition.justification = Justification(isgiven=False, sp_output=out)
      goal.justification       = Justification(isgiven=False, formula=definition, schema=def_name)
      res1 = add_to_base(base, definition)

    else:
      full_def.justification = Justification(isgiven=False, formula=subs, sp_output=out)
      goal.justification     = Justification(isgiven=False, formula=full_def, schema=def_name)
      res1 = add_to_base(base, full_def)

    # Attempt to add both to base, return True if either succeeds (i.e. if either was not previously in the base)
    res2 = add_to_base(base, goal)
    return res1 or res2

  return False



# formula -- Formula
# base    -- List(Formula)
#
# Returns a string containing an argument justifying "formula"
# The helper function recursively traces justifications of supporting
# formulae in "base"
#
def generate_argument_string(formula, base):
  return generate_argument_string_helper(formula, base, "", [])



# sep           -- String        -- Spaces, e.g. "  ", to indent recursive argument steps further in
# already_added -- List(Formula) -- Any formula which have already been justified (or are being justified in calls to the helper up the stack)
#
def generate_argument_string_helper(formula, base, sep, already_added):

  if(formula in already_added): return ""

  # Ensures that any subsequent recursive calls to the helper function won't
  # attemmpt to justify the formula we're currently justifying (causing an infinite
  # loop)
  already_added.append(formula) 

  out  = sep + "PROOF OF: " + str(formula) + "\n"
  out += formula.justification.string_with_indent(sep)

  # If formula is given, we're done
  if(formula.justification.isgiven): return out

  justifier = formula.justification.formula # Formula(e) which justify formula
  sep      += INDENT                        # Increase indent

  # If justified (in part or in whole) using ShadowProver, it won't be obvious which formulae in the
  # base ShadowProver needed to construct its proof
  # While not perfect, this is a "hacky" (but currently, the most easily implemented) way to trace
  # which assumptions ShadowProver used. That is, we see which formulae are contained in SP's output
  if not formula.justification.sp_output == None:
    sp_out_sanitized = " ".join(formula.justification.sp_output.split()) # Squish any extra spaces

    for f in base:                                                          # If a formula in the base (which is not
      if(str(f) in sp_out_sanitized and not f == formula):                  # the one currently being justified -- think
        out += generate_argument_string_helper(f, base, sep, already_added) # infinite loop) appears in the ShadowProver
        already_added.append(f)                                             # output, include it's justification

  # If no justifying formula(e), we're done
  # (Possible reasons -- used ShadowProver (and hence can't track which formuale were used)
  #                   -- used a schema which requires no formulae to invoke)
  if justifier == None: return out

  if(isinstance(justifier, Formula)):                                           # If justification is a single formula
    out += generate_argument_string_helper(justifier, base, sep, already_added) # Recursively output its justification

  else:                                                                # If it's a list of formulae
    for f in justifier:                                                # Recursively output justifications of each formula       
      out += generate_argument_string_helper(f, base, sep, already_added)
      already_added.append(justifier)

  return out


