# Demo for running the pilot dilemma case study
# presented in the paper "Toward Defeasible Multi-Operator
# Argumentation Systems" by Bringsjord, Giancola, & Govindarajulu

from time import time

try:
  from expanders.PerceptiontoEvidentBelief import perception_to_evident_belief
  from expanders.SFModusPonens             import sf_modus_ponens
  from expanders.SFConjElim                import sf_conj_elim
  from constructors.ProvableFromBeliefs    import argue_via_beliefs
  from formula.Parser                      import parse_list, parse_fstring
  from argument_constructor                import solve
  from demos.demo_sp                       import sp_warmup
  from adjudicator                         import adjudicate, uncertain_belief_ethical_principle_pilot
  from utils                               import sp_time_test
except ModuleNotFoundError:
  print("Demos must be run from the base directory, NOT the 'demos' directory.")
  exit(1)


expanders    = [perception_to_evident_belief, sf_modus_ponens, sf_conj_elim]
constructors = [argue_via_beliefs]


def solve_argument_3():
  print("Generating a solution to Argument 3...")

  assumptions = [

    "(Perceives! r1 t0 iru1)",

    "(Perceives! r1 t1 celestial_bodies)",
    "(Perceives! r1 t1 (and (not (Perceives! p1 t1 celestial_bodies)) \
                            (not (Perceives! p2 t1 celestial_bodies))))",

    "(Believes!4 r1 t1 (implies (and (not (Perceives! p1 t1 celestial_bodies)) \
                                     (Perceives! p1 t1 (Says! r1 t1 iru1))) \
                                (Believes! p1 t2 (GoingToStall plane t3))))",

    "(Believes!4 r1 t1 (implies (Believes! p1 t2 (GoingToStall plane t3)) \
                                (Intends! p1 t3 (LowerPitch plane t4))))",

    "(Believes!4 r1 t1 (implies (LowerPitch plane t4) (Crash plane t5)))",

    # Counterfactual assumption
    # (That is, r1 shows that this assumption leads to a crash. Hence,
    #  r1 should not pass the iru1 data along to the pilot)
    "(Believes!4 r1 t1 (Perceives! p1 t1 (Says! r1 t1 iru1)))"

  ]

  goal = "(Believes!4 r1 t1 (Crash plane t5))"

  base         = parse_list(assumptions) # Parse into Python objects
  goal_formula = parse_fstring(goal)

  start = time()
  out   = solve(base, goal_formula, expanders=expanders, constructors=constructors)
  stop  = time()

  print("Argument found in " + str(stop - start) + " seconds.")
  print(out + "\n")

  return goal_formula



def solve_argument_4():
  print("Generating a solution to Argument 4...")

  assumptions = [

    "(Perceives! r2 t0 iru1)",

    "(Believes!3 r2 t1 (IsReliable iru1))",

    "(Believes!4 r2 t1 (implies (IsReliable iru1) \
                                (implies (Perceives! p1 t1 (Says! r2 t1 iru1)) \
                                         (not (Crash plane t5)))))",

    # Counterfactual assumption
    # (That is, r2 shows that this assumption won't lead to a crash. Hence,
    #  r2 should pass the iru1 data along to the pilot)
    "(Believes!4 r2 t1 (Perceives! p1 t1 (Says! r2 t1 iru1)))"

  ]

  goal = "(Believes!3 r2 t1 (not (Crash plane t5)))"

  base         = parse_list(assumptions) # Parse into Python objects
  goal_formula = parse_fstring(goal)

  start = time()
  out   = solve(base, goal_formula, expanders=expanders, constructors=constructors)
  stop  = time()

  print("Argument found in " + str(stop - start) + " seconds.")
  print(out + "\n")

  return goal_formula



if __name__ == "__main__":

  print("Running ShadowProver warmup...")
  sp_warmup()
  print("Done.\n")

  b1 = solve_argument_3()
  b2 = solve_argument_4()

  beliefs = [b1, b2]
  print("Calling Adjudicator...")
  print("Final Belief: " + str(adjudicate(beliefs)))
  print("Hence: " + str(uncertain_belief_ethical_principle_pilot(beliefs)))

