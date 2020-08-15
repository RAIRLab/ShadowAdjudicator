# This file runs ShadowAdjudicator based on input from AirSim
# and returns to AirSim its decision

from time     import time, sleep
from os.path  import exists
from filelock import SoftFileLock

try:
  from expanders.PerceptiontoEvidentBelief import perception_to_evident_belief
  from constructors.Uber                   import level1_arg_constructor, level2_arg_constructor, level3_arg_constructor
  from constructors.ProvableFromBeliefs    import argue_via_beliefs
  from formula.Parser                      import parse_list, parse_fstring
  from argument_constructor                import solve
  from demos.demo_sp                       import sp_warmup
  from adjudicator                         import adjudicate
except ModuleNotFoundError:
  print("Demos must be run from the base directory, NOT the 'demos' directory.")
  exit(1)


constructors = [level1_arg_constructor, level2_arg_constructor, level3_arg_constructor, argue_via_beliefs]
expanders    = [perception_to_evident_belief]



def construct_agent1_argument():
  print("Constructing Agent 1's Argument...")

  assumptions = [

    "(Believes!5 a1 t1 (forall [?x] (iff (Moving ?x) \
                                         (and (At ?x t0 l0) (At ?x t1 l1) (not (= t0 t1)) (not (= l0 l1))))))",

    "(Believes!5 a1 t1 (forall [?c] (iff (NeedToBrake ?c) \
                                         (or (and (Moving o) (TrajectoriesCross ?c o)) \
                                             (InPath o ?c)))))",

    "(Perceives! a1 t1 (not (InPath o c)))",

    "(R a1 t1 (Believes! a1 t1 (not (Moving o))) \
              (Believes! a1 t1 (not (not (Moving o)))))"

  ]

  goal1 = "(Believes!2 a1 t1 (not (Moving o)))"
  goal2 = "(Believes!2 a1 t1 (not (NeedToBrake c)))"

  base          = parse_list(assumptions) # Parse into Python objects
  goal_formula1 = parse_fstring(goal1)
  goal_formula2 = parse_fstring(goal2)

  start = time()
  out   = solve(base, goal_formula1, expanders=expanders, constructors=constructors)
  stop  = time()

  print("Argument found in " + str(stop - start) + " seconds.")
  print(out + "\n")

  start = time()
  out   = solve(base, goal_formula2, expanders=expanders, constructors=constructors)
  stop  = time()

  print("Argument found in " + str(stop - start) + " seconds.")
  print(out)

  return goal_formula2



def construct_agent2_argument():
  print("Constructing Agent 2's Argument...")

  assumptions = [

    "(Believes!5 a2 t1 (forall [?x] (iff (Moving ?x) \
                                         (and (At ?x t0 l0) (At ?x t1 l1) (not (= t0 t1)) (not (= l0 l1))))))",

    "(Believes!5 a2 t1 (forall [?c] (iff (NeedToBrake ?c) \
                                         (or (and (Moving o) (TrajectoriesCross ?c o)) \
                                             (InPath o ?c)))))",

    "(Perceives! a2 t0 (not (InPath o c)))",
    "(Perceives! a2 t0 (At o t0 l0))",
    "(Perceives! a2 t1 (At o t1 l1))",
    "(Perceives! a2 t1 (not (= l0 l1)))",
    "(Perceives! a2 t1 (not (= t0 t1)))",
    "(Perceives! a2 t1 (TrajectoriesCross c o))"

  ]

  goal = "(Believes!4 a2 t1 (NeedToBrake c))"

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

  demo_path = "demos/2020_GCAI_Driving/"

  out_file   = demo_path + "reasoner_output.txt"
  lock_file2 = out_file + ".lock"
  lock2      = SoftFileLock(lock_file2)

  # Make sure ShadowAdjudicator gets lock for its output file
  with lock2:
    in_file    = demo_path + "reasoner_input.txt"
    lock_file1 = in_file + ".lock"

    print("Wating for input from AirSim...")
    while(not exists(in_file)):
      sleep(0.1)

    lock1 = SoftFileLock(lock_file1)
    with lock1:
      in_text = open(in_file, "r").read()

    if in_text == "Single agent":
      print("Single agent simulation requested.")
      b1      = construct_agent1_argument()
      beliefs = [b1]

    elif in_text == "Both agents":
      print("Both agent simulation requested.")
      b1      = construct_agent1_argument()
      b2      = construct_agent2_argument()
      beliefs = [b1, b2]

    else:
      print("ERROR: Invalid input.")
      exit(1)

    final    = adjudicate(beliefs)
    out_text = str(final.formula)

    open(out_file, "w").write(out_text)

  print("Sent output of reasoning to AirSim.")

