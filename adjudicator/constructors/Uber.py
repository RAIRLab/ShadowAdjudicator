# Level definitions for the modeling the Uber case study as
# presented in the paper ``A Framework for Dynamic Argument
# Adjudication in Autonomous-Driving AI'', submitted to a
# special issue of the Journal of Logic & Computation

# NOTE
# The functions in this file
# don't require the "expanders" and "constructors" arguments
# They must be provided here so that they conform to the general
# signature of constructors when called in the construct_argument
# function. They have a default value so that the functions don't
# require the parameters. Either way, they do nothing with them.

from formula.SFBelief      import SFBelief
from formula.Belief        import Belief
from formula.Withhold      import Withhold
from formula.Perception    import Perception
from formula.Predicate     import Predicate
from formula.Not           import Not
from formula.Justification import Justification
from argument_constructor  import level_arg_constructor

# base -- List(Formula)
# goal -- Formula
# 
# If goal is an instance of the level-1 definition,
# calls ShadowProver to attempt to prove its definition
# 
# If goal is ill-formed, the definition cannot be proved,
# or the goal is already in the base, returns False
# Otherwise, returns True and the goal is added to the base
#
def level1_arg_constructor(base, goal, expanders=None, constructors=None):

  # If goal is of the form: (Believes!1 a t phi) ...
  if(isinstance(goal, SFBelief) and goal.strength == 1):

    a = goal.agent
    t = goal.time
    p = goal.formula

    # Attempt to prove its definition: (not (R a t (Withholds! a t phi) (Believes! a t phi)))
    definition = Not.from_args(Predicate.from_args("R", [a, t, Withhold.from_args(a, t, p), Belief.from_args(a, t, p)]))
    return level_arg_constructor(base, goal, definition, "Level-1 Definition")

  return False



# Same as level1_arg_constructor, for level-2.
#
def level2_arg_constructor(base, goal, expanders=None, constructors=None):

  # If goal is of the form: (Believes!2 a t phi)
  if(isinstance(goal, SFBelief) and goal.strength == 2):

    a = goal.agent
    t = goal.time
    p = goal.formula

    # Attempt to prove its definition: (R a t (Believes! a t phi) (Believes! a t (not phi)))
    definition = Predicate.from_args("R", [a, t, Belief.from_args(a, t, p), Belief.from_args(a, t, Not.from_args(p))])
    return level_arg_constructor(base, goal, definition, "Level-2 Definition")

  return False



def level3_arg_constructor(base, goal, expanders=None, constructors=None):

  # If goal is of the form: (Believes!3 a t phi)
  if(isinstance(goal, SFBelief) and goal.strength == 3):

    a = goal.agent
    t = goal.time
    p = goal.formula

    # Attempt to prove its definition: (R a t (Believes! a t phi) (Withholds! a t (not phi)))
    definition = Predicate.from_args("R", [a, t, Belief.from_args(a, t, p), Withhold.from_args(a, t, p)])
    return level_arg_constructor(base, goal, definition, "Level-3 Definition")

  return False

