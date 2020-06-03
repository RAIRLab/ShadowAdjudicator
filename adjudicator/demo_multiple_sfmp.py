# Demo of multiple applications of SF Modus Ponens inference rule

from formula.Parser import parse_list, parse_fstring
from Prove          import prove

if __name__ == "__main__":

  assumptions = [
    "(Believes!5 john now smiling)",
    "(Believes!4 john now (implies smiling happy))",
    "(Believes!3 john now (implies happy excited))"
  ]

  goal = "(Believes!3 john now excited)"

  base         = parse_list(assumptions) # Parse into Python objects
  goal_formula = parse_fstring(goal)

  print(prove(base,goal_formula))

