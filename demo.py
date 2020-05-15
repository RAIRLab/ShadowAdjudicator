from prover20200407unk.interface import prove


if __name__ == "__main__":
  assumptions = [
    "(Believes! john happy)",
    "(Believes! john smiling)"]

  goal = "(Believes! john (and happy smiling))"

  print(prove(assumptions, goal))
