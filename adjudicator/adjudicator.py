from formula.Knowledge     import Knowledge
from formula.Obligation    import Obligation
from formula.Atom          import Atom
from formula.Justification import Justification

# beliefs -- List(SFBelief)
# This function serves as the adjudicator agent
# Currently, it simply selects the belief with the highest strength factor
# Later, more adjudication methods will be implemented here
def adjudicate(beliefs):
  strengths = list(map(lambda x : x.strength, beliefs))
  return beliefs[strengths.index(max(strengths))]


# beliefs -- List(SFBelief)
# Implements the ethical principle for the Miracle on the Hudson (MotH) scenario
# presented in the paper ``ETHICAL REASONING FOR AUTONOMOUS AGENTS UNDER UNCERTAINTY'',
# submitted to ICRES 2020

def uncertain_belief_ethical_principle(beliefs):
  strongest = adjudicate(beliefs)

  agent        = strongest.agent
  time         = strongest.time
  precondition = Atom.from_string("emergency")
  land         = strongest.formula.args[2]
  formula      = Atom.from_string("(happens (action " + str(agent) + " land(" + str(land) + ")) " + str(time) + "'")

  jus = Justification(isgiven=False, formula=beliefs, schema="Ethical Principle for Scenarios with Uncertain Ethical Outcomes")

  return Knowledge.from_args(agent, time, Obligation.from_args(agent, time, precondition, formula), jus)
