# Demo for running the a proof of the "Fuel low" scenario.
# The scenario was invented by the following authors, and presented in the following paper:
#   L. Dennis, M. Fisher, M. Slavkovik and M. Webster,
#   Formal Verification of Ethical Choices in Autonomous Systems,
#   Robotics and Autonomous Systems 77, 1 (2016)
#   http://dx.doi.org/ 10.1016/j.robot.2015.11.012
#
# The proof herein corresponds to a translation of the scenario into
# the Deontic Cognitive Event Calculus (DCEC), presented in Appendix B of 
# "ETHICAL REASONING FOR AUTONOMOUS AGENTS UNDER UNCERTAINTY" by Giancola,
# Bringsjord, Govindarajulu, and Varela

from utils import sp_time_test


if __name__ == "__main__":
  assumptions = [

    # UA knows ethicality of options
    "(Knows! ua now (LessUnethical emptyroad fieldwithpowerlines))",
    "(Knows! ua now (LessUnethical emptyroad fieldwithpeople))",

    # UA knows landing in the empty road is the best choice
    # if it is LessUnethical than the other two options
    #
    # NOTE: We would really like
    #       BestOption to be defined using quantification i.e.
    #       (BestOption x) <==> forall y . (LessUnethical x y)
    #       However, this would require quantifying over a fixed domain
    #       which is not currently possible in ShadowProver, but could
    #       be implemented in practice.
    "(Knows! ua now (if (and (LessUnethical emptyroad fieldwithpowerlines) \
                             (LessUnethical emptyroad fieldwithpeople)) \
                        (BestOption emptyroad)))",

    # UA knows they are obligated to select the best option
    "(forall [?option] (Knows! ua now (if (BestOption ?option) \
                                          (Ought! ua now crisis (happens (action ua (Land ?option)) now)))))",

    # UA is aware of the situation
    "(Believes! ua now crisis)"

  ]

  # Prove sub-goal, which requires new "Smart Instantiation" feature of ShadowProver
  goal = "(Knows! ua now (Ought! ua now crisis (happens (action ua (Land emptyroad)) now)))"

  # Then prove rest of the way
  if(sp_time_test(assumptions, goal)):
    assumptions.append(goal)
    goal = "(happens (action ua (Land emptyroad)) now)"

    sp_time_test(assumptions, goal)

