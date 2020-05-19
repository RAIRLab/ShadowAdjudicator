

def parse_list(fstrings):

  flist = []
  for f in fstrings:
    flist.append(parse(f))
  return flist



def parse(fstring):

  if(fstring.startswith("(Believes!")):
    if(fstring[10] == ' '):
      from .Belief import Belief
      return Belief(fstring)
    else:
      from .SFBelief import SFBelief
      return SFBelief(fstring)

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
    return Not(fstring)

  elif(fstring.startswith("(and")):
    from .And import And
    return And(fstring)

  elif(fstring.startswith("(or")):
    from .Or import Or
    return Or(fstring)

  elif(fstring.startswith("(implies")):
    from .Implication import Implication
    return Implication(fstring)

  elif(fstring.startswith("(iff")):
    from .BiConditional import BiConditional
    return BiConditional(fstring)

  # A propositional atom (or unimplemented formula types)
  else:
    from .Formula import Formula
    return Formula(fstring)
