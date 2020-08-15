# Level definitions for the Miracle on the Hudson (MotH) scenario
# presented in the paper ``ETHICAL REASONING FOR AUTONOMOUS AGENTS
# UNDER UNCERTAINTY'', submitted to ICRES 2020

# NOTE
# level1_arg_constructor (& the corresponding func for level 2)
# don't require the "expanders" and "constructors" arguments
# They must be provided here so that they conform to the general
# signature of constructors when called in the construct_argument
# function. They have a default value so that the functions don't
# require the parameters. Either way, they do nothing with them.

from formula.SFBelief      import SFBelief
from formula.Belief        import Belief
from formula.Perception    import Perception
from formula.Predicate     import Predicate
from formula.And           import And
from formula.Or            import Or
from formula.Not           import Not
from formula.Atom          import Atom
from formula.Greater       import Greater
from formula.Function      import Function
from formula.Justification import Justification
from utils                 import add_to_base 
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

  # If goal is of the form: (Believes!1 a t (Land a t phi)) ...
  if(isinstance(goal, SFBelief)          and \
     goal.strength == 1                  and \
     isinstance(goal.formula, Predicate) and \
     goal.formula.name == "Land"):

    # Attempt to prove its definition: (Believes! a t (Believes! atc t (Land a t phi)))
    definition = Belief.from_args(goal.agent, goal.time, Belief.from_args("atc", goal.time, goal.formula))
    return level_arg_constructor(base, goal, definition, "Level-1 Definition")

  return False



# base -- List(Formula)
#
# If the base contains formulae of the following forms:
#   (Perceives! a t (Reachable a t phi))
#   (Perceives! a t (not (Reachable a t psi))
# this function infers a Reasonableness relation of the following form:
#   (R a t (Land a t phi) (Land a t psi))A
#
def reasonableness_expander(base):

  modifiedBase = False

  # Filtering for formulae of the forms: (Perceives! a t (Reachable a t phi))
  #                                      (Perceives! a t (not (Reachable a t psi)))
  reachable     = filter(lambda x : isinstance(x, Perception) and isinstance(x.formula, Predicate) and x.formula.name == "Reachable", base)
  not_reachable = filter(lambda x : isinstance(x, Perception) and isinstance(x.formula, Not) and isinstance(x.formula.args[0], Predicate) and x.formula.args[0].name == "Reachable", base)

  for f1 in reachable:
    for f2 in not_reachable:
      subf1 = f1.formula
      subf2 = f2.formula.args[0]

      if(f1.agent == f2.agent and \
         f1.time  == f2.time  and \
         subf1.args[0] == subf2.args[0] and \
         subf1.args[1] == subf2.args[1] and \
         not subf1.args[2] == subf2.args[2]):

        # Generate a formula of the form: (R a t (Land a t phi) (Land a t psi))
        jus     = Justification(isgiven=False, formula=[f1, f2], schema="Reasonableness Definition")
        result  = Predicate.from_args("R", [f1.agent, f1.time, Predicate.from_args("Land", [subf1.args[0], subf1.args[1], subf1.args[2]]), \
                                                               Predicate.from_args("Land", [subf1.args[0], subf1.args[1], subf2.args[2]])], jus)

        if(add_to_base(base, result)): modifiedBase = True

  return modifiedBase


# Same as level1_arg_constructor, for level-2.
#
def level2_arg_constructor(base, goal, expanders=None, constructors=None):

  # If goal is of the form: (Believes!2 a t (Land a t phi))
  if(isinstance(goal, SFBelief)          and \
     goal.strength == 2                  and \
     isinstance(goal.formula, Predicate) and \
     goal.formula.name == "Land"):

    # Attempt to construct an argument for the full level-2 definition:
    # (and (Perceives a t emergency) (Believes!1 a t (Land a t psi)) (R a t (Land a t phi) (Land a t psi)))

    # First step: Run reasonableness expander, then find any reasonableness predicates which match the third conjunct of the definition 
    reasonableness_expander(base)
    matching_r = list(filter(lambda x : isinstance(x, Predicate) \
                               and x.name == "R"                 \
                               and x.args[0] == goal.agent       \
                               and x.args[1] == goal.time        \
                               and x.args[2] == goal.formula,    \
                        base))

    # Then collect a list of psi's, which are the less reasonable landing locations in the reasonableness predicates found above
    valid_psi = map(lambda x : x.args[3].args[2], matching_r)

    i = -1
    for psi in valid_psi:

      i += 1

      # For those psi's, we need to see if we can construct an argument for a level-1 belief (this is the second conjunct in the level-2 definition)
      level_1_sub = SFBelief.from_args(goal.agent, goal.time, Predicate.from_args("Land", [goal.agent, goal.time, psi]), 1)
      if(level_1_sub in base or level1_arg_constructor(base, level_1_sub)):

        # Find conjunct 2 and 3 in the base
        level_1_found  = base[base.index(level_1_sub)]
        r_found        = matching_r[i]

        # Now we just need to prove the first conjunct and we're done
        definition = Perception.from_args(goal.agent, goal.time, Atom.from_string("emergency"))

        full       = And.from_args([Perception.from_args(goal.agent, goal.time, Atom.from_string("emergency")), \
                                    level_1_found, \
                                    r_found])

        return level_arg_constructor(base, goal, definition, "Level-2 Definition", full_def=full, subs=[level_1_found, r_found])

  return False

