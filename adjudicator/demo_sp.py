# Demo for running ShadowProver within JuypterLab/Docker environment

import sys
sys.path.insert(1, '/pylibs/interface')
import interface

if __name__ == "__main__":
  assumptions = [
    "(Believes! john happy)",
    "(Believes! john smiling)"]

  goal = "(Believes! john (and happy smiling))"

  print(interface.prove(assumptions, goal))
