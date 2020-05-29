# Demo for running ShadowProver within JuypterLab/Docker environment

import sys
sys.path.insert(1, '/pylibs/interface')
import interface



def sp_warmup():
  assumptions = [
    "(Believes! john happy)",
    "(Believes! john smiling)"]

  goal = "(Believes! john (and happy smiling))"

  return interface.prove(assumptions, goal)



if __name__ == "__main__":
  print(sp_warmup())
