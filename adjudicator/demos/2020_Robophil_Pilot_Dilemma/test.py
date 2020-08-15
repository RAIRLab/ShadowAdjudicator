# Demo for running ShadowProver within JuypterLab/Docker environment

#import sys
#sys.path.insert(1, '/pylibs/interface')
#import interface

from argument_constructor import prove_via_shadowprover
from formula.Parser import parse_list, parse_fstring

def test():
  assumptions = [

  "(implies (and (not (Perceives! p1 t1 celestial_bodies)) (Perceives! p1 t1 (Says! r1 t1 iru1))) (Believes! p1 t2 (GoingToStall plane t3)))",
  "(implies (Believes! p1 t2 (GoingToStall plane t3)) (Intends! p1 t3 (LowerPitch plane t4)))",
  "(implies (LowerPitch plane t4) (Crash plane t5))",
  "(Perceives! p1 t1 (Says! r1 t1 iru1))",
  "iru1",
  "celestial_bodies",
  "(and (not (Perceives! p1 t1 celestial_bodies)) (not (Perceives! p2 t1 celestial_bodies)))",
  "(not (Perceives! p1 t1 celestial_bodies))",
  "(not (Perceives! p2 t1 celestial_bodies))"

  ]

  goal = "(Crash plane t5)"

  base         = parse_list(assumptions) # Parse into Python objects
  goal_formula = parse_fstring(goal)

  return prove_via_shadowprover(base, goal_formula)



if __name__ == "__main__":
  print(test())
