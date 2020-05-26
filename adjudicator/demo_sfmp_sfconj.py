# Demo of a proof requiring both SF Modus Ponens and SF Conj Elim rules

from formula.Parser import parse_list, parse
from Prove          import prove

if __name__ == "__main__":

  assumptions = [
    "(Believes!5 john now smiling)",
    "(Believes!4 john now (and (implies smiling happy) (implies happy (and jubilant thrilled))))",
  ]

  goal = "(Believes!4 john now thrilled)"

  base         = parse_list(assumptions) # Parse into Python objects
  goal_formula = parse(goal)

  print(prove(base,goal_formula))

