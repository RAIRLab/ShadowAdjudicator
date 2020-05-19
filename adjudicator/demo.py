# Demo for running Strength Factor inference rules

from formula.Parser          import parse_list, parse
from expanders.SFModusPonens import sf_modus_ponens

if __name__ == "__main__":

  assumptions = [
    "(Believes!5 john now smiling)",
    "(Believes!4 john now (implies smiling happy))"]

  goal = "(Believes!4 john now happy)"

  base         = parse_list(assumptions) # Parse into Python objects
  goal_formula = parse(goal)

  sf_modus_ponens(base)          # Run SF Modus Ponens expander

  print("Goal in Assumption Base?: " + str(goal_formula in base))

