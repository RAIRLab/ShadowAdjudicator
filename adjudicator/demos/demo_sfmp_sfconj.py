# Demo of a proof requiring both SF Modus Ponens and SF Conj Elim schemas

try:
  from formula.Parser import parse_list, parse_fstring
  from argument_constructor    import construct_argument
except ModuleNotFoundError:
  print("Demos must be run from the base directory, NOT the 'demos' directory.")
  exit(1)

if __name__ == "__main__":

  assumptions = [
    "(Believes!5 john now smiling)",
    "(Believes!4 john now (and (implies smiling happy) (implies happy (and jubilant thrilled))))",
  ]

  goal = "(Believes!4 john now thrilled)"

  base         = parse_list(assumptions) # Parse into Python objects
  goal_formula = parse_fstring(goal)

  print(prove(base,goal_formula))

