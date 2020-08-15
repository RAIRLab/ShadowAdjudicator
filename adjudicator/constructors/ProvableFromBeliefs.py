from formula.SFBelief      import SFBelief
from formula.Justification import Justification
from utils                 import add_to_base

# base -- List(Formula)
# goal -- Formula
#
# Attempts to apply inference schema I^s_B to prove goal
# That is, if the sub-formula of goal is provable from the sub-formulae of some
# annotated beliefs, we can induce a belief in the sub-goal at the weakest strength
# of any of the beliefs whose sub-formulae were used in the argument.
#
# Returns True if base was modified (i.e. rule was applied to at least one formula)
#
def argue_via_beliefs(base, goal, expanders, constructors):

  modifiedBase = False

  a = goal.agent
  s = goal.strength

  # We filter here for beliefs that are no weaker than the goal (since if weaker beliefs are
  # used, we can't derive a belief in the goal at the level we desire)
  beliefs = list(filter(lambda x : isinstance(x, SFBelief) and x.agent == a and x.strength >= s, base))

  sub_base = list(map(lambda x : x.formula, beliefs))
  sub_goal = goal.formula

  # If the subgoal is an annotated formula, try to construct an argument using ShadowAdjudicator
  if(sub_goal.is_annotated()):
    from argument_constructor import construct_argument
    found = construct_argument(sub_base, sub_goal, expanders, constructors)

    if(not found == None and add_to_base(base, found)):
      modifiedBase = True

  # Otherwise, try to prove it using ShadowProver
  else:
    from argument_constructor import prove_via_shadowprover
    out = prove_via_shadowprover(sub_base, sub_goal)

    if(not out == "FAILED" and add_to_base(base, goal)):
      goal.justification = Justification(isgiven=False, formula=beliefs, schema="Arguable from Belief Set")
      modifiedBase = True

  return modifiedBase

