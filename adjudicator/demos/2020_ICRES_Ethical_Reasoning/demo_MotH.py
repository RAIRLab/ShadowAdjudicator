# Demo for running the "Miracle on the Hudson" scenario
# presented in the paper "ETHICAL REASONING FOR AUTONOMOUS
# AGENTS UNDER UNCERTAINTY" by Giancola, Bringsjord,
# Govindarajulu, and Varela

from time import time

try:
  from constructors.MotH    import level1_arg_constructor, level2_arg_constructor, reasonableness_expander
  from formula.Parser       import parse_list, parse_fstring
  from argument_constructor import solve
  from demos.demo_sp        import sp_warmup
  from adjudicator          import adjudicate, uncertain_belief_ethical_principle_moth
  from utils                import sp_time_test
except ModuleNotFoundError:
  print("Demos must be run from the base directory, NOT the 'demos' directory.")
  exit(1)


constructors = [level1_arg_constructor, level2_arg_constructor]
expanders    = [reasonableness_expander]



def solve_sub_argument_1():
  print("Generating a solution to Sub-Argument 1...")

  assumptions = [

    # Due to details of the current ShadowProver implementation,
    # the formula in the paper S(atc, capt, t1, Land(lga13))
    # had to be converted to this form
    "(Perceives! capt t1 (Says! atc t1 (Land capt t1 lga13)))"
  ]

  goal = "(Believes!1 capt t1 (Land capt t1 lga13))"

  base         = parse_list(assumptions) # Parse into Python objects
  goal_formula = parse_fstring(goal)

  start = time()
  out   = solve(base, goal_formula, expanders=expanders, constructors=constructors)
  stop  = time()

  print("Argument found in " + str(stop - start) + " seconds.")
  print(out + "\n")



def solve_sub_argument_2():
  print("Generating a solution to Sub-Argument 2...")

  assumptions = [

    "(Perceives! capt t2 emergency)",

    "(Believes!1 capt t2 (Land capt t2 lga13))",

    "(Perceives! capt t2 (Reachable capt t2 teb))",
    "(Perceives! capt t2 (not (Reachable capt t2 lga13)))"
    
  ]

  goal = "(Believes!2 capt t2 (Land capt t2 teb))"

  base         = parse_list(assumptions)
  goal_formula = parse_fstring(goal)

  start = time()
  out   = solve(base, goal_formula, expanders=expanders, constructors=constructors)
  stop  = time()

  print("Argument found in " + str(stop - start) + " seconds.")
  print(out + "\n")



def solve_sub_argument_3():
  print("Generating a solution to Sub-Argument 3...")

  assumptions = [

    "(Perceives! capt t3 emergency)",

    "(Perceives! capt t3 (Says! atc t3 (Land capt t3 teb1)))",

    "(Perceives! capt t3 (not (Reachable capt t3 lga13)))",
    "(Perceives! capt t3 (not (Reachable capt t3 teb1)))",
    "(Perceives! capt t3 (Reachable capt t3 hud))"
  ]

  goal1 = "(Believes!1 capt t3 (Land capt t3 teb1))"
  goal2 = "(Believes!2 capt t3 (Land capt t3 hud))"

  base          = parse_list(assumptions)
  goal_formula1 = parse_fstring(goal1)
  goal_formula2 = parse_fstring(goal2)

  start = time()
  out   = solve(base, goal_formula1, expanders=expanders, constructors=constructors)
  stop  = time()

  print("Argument found in " + str(stop - start) + " seconds.")
  print(out)

  start = time()
  out   = solve(base, goal_formula2, expanders=expanders, constructors=constructors)
  stop  = time()

  print("Argument found in " + str(stop - start) + " seconds.")
  print(out)

  goal1_found = base[base.index(goal_formula1)]
  goal2_found = base[base.index(goal_formula2)]

  print("Calling Adjudicator...")
  beliefs = [goal1_found, goal2_found]
  print("Final Belief: " + str(adjudicate(beliefs)))
  print("Hence: "        + str(uncertain_belief_ethical_principle_moth(beliefs)) + "\n")


def solve_sub_argument_4():
  print("Generating a solution to Sub-Argument 4...")

  assumptions = [

  "(Knows! capt t3 (Ought! capt t3 emergency (happens (action capt (land hud)) t4)))",
  "(Perceives! capt t3 emergency)"
  ]

  goal = "(happens (action capt (land hud)) t4)"

  sp_time_test(assumptions, goal)



if __name__ == "__main__":

  print("Running ShadowProver warmup...")
  sp_warmup()
  print("Done.\n")

  solve_sub_argument_1()
  solve_sub_argument_2()
  solve_sub_argument_3()
  solve_sub_argument_4()

