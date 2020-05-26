from .Justification import Justification

def parse_list(fstrings):

  flist = []
  for f in fstrings:
    flist.append(parse(f))
  return flist



def parse(fstring):

  if(fstring.startswith("(Believes!")):
    if(fstring[10] == ' '):
      from .Belief import Belief
      return Belief(fstring, Justification(isgiven=True))
    else:
      from .SFBelief import SFBelief
      return SFBelief(fstring, Justification(isgiven=True))

  #elif(fstring.startswith("Perceives!"):
  #  return Perceives(fstring)

  #elif(fstring.startswith("(Knows!"):
  #  return Knowledge(fstring)

  #elif(fstring.startswith("(Common!"):
  #  return Common(fstring)

  #elif(fstring.startswith("(Ought!"):
  #  return Ought(fstring)

  #elif(fstring.startswith("(Intends!"):
  #  return Intends(fstring)

  #elif(fstring.startswith("(Desires!"):
  #  return Desires(fstring)

  elif(fstring.startswith("(not")):
    from .Not import Not
    return Not(fstring, Justification(isgiven=True))

  elif(fstring.startswith("(and")):
    from .And import And
    return And(fstring, Justification(isgiven=True))

  elif(fstring.startswith("(or")):
    from .Or import Or
    return Or(fstring, Justification(isgiven=True))

  elif(fstring.startswith("(implies")):
    from .Implication import Implication
    return Implication(fstring, Justification(isgiven=True))

  elif(fstring.startswith("(iff")):
    from .BiConditional import BiConditional
    return BiConditional(fstring, Justification(isgiven=True))

  # A propositional atom (or unimplemented formula types)
  else:
    from .Formula import Formula
    return Formula(fstring, Justification(isgiven=True))


# formula -- String
# Given a s-expression, returns a list of the top-level elements
# e.g. given (and (and a b) (implies (and c d) e))
# returns    ['and', '(and a b)', '(implies (and c d) e)']
def parse_sexpr(formula):
  out = []
  begin_atom = 1
  begin_search = 1
  depth = 0
  N = len(formula)

  while begin_search < N:
    end = find_next_of_interest(formula, begin_search)
    c = formula[end]
    begin_search = end + 1

    if(c == ' ' and depth == 0):
        out.append(formula[begin_atom:end])
        begin_atom = end + 1

    elif(c == '('):
      depth += 1
      begin_search = end + 1

    elif(c == ')'):
      depth -= 1
      if(depth == 0):
        out.append(formula[begin_atom:end+1])
        begin_atom = end + 2
        begin_search = begin_atom

      # Done! (Hit last right paren)
      elif(depth == -1):
        out.append(formula[begin_atom:end])

  return out

# NOT INTENDED TO BE CALLED OUTSIDE THIS FILE
# Helper for parse_sexpr
# Finds the next character of interest in the formula
def find_next_of_interest(formula, begin):
  val = float("inf")

  idx = formula.find(' ', begin)
  if(not idx == -1 and idx < val): val = idx

  idx = formula.find('(', begin)
  if(not idx == -1 and idx < val): val = idx

  idx = formula.find(')', begin)
  if(not idx == -1 and idx < val): val = idx

  return val
