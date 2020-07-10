# Demo for running Strength Factor inference schemata

try:
  from formula.Parser          import parse_list, parse_fstring
  from Prove                   import prove
except ModuleNotFoundError:
  print("Demos must be run from the base directory, NOT the 'demos' directory.")
  exit(1)

if __name__ == "__main__":

  assumptions = [
    "(Believes!5 john now smiling)",
    "(Believes!4 john now (implies smiling happy))"]

  goal = "(Believes!4 john now happy)"

  base         = parse_list(assumptions) # Parse into Python objects
  goal_formula = parse_fstring(goal)

  print(prove(base,goal_formula))
