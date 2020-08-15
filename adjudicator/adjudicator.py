from formula.SFBelief      import SFBelief
from formula.Knowledge     import Knowledge
from formula.Obligation    import Obligation
from formula.Predicate     import Predicate
from formula.Function      import Function
from formula.Not           import Not
from formula.Atom          import Atom
from formula.Justification import Justification

# beliefs -- List(SFBelief)
# This function serves as the adjudicator agent
# Currently, it simply selects the belief with the highest strength factor
# Later, more adjudication methods will be implemented here
def adjudicate(beliefs):
  strengths = list(map(lambda x : x.strength, beliefs))
  b = beliefs[strengths.index(max(strengths))]
  return SFBelief.from_args("adj", b.time, b.formula, b.strength, b.justification)


# beliefs -- List(SFBelief)
# Implements the ethical principle for the Miracle on the Hudson (MotH) scenario
# presented in the paper "ETHICAL REASONING FOR AUTONOMOUS AGENTS UNDER UNCERTAINTY"
# by Giancola, Bringsjord, Govindarajulu, & Varela
def uncertain_belief_ethical_principle_moth(beliefs):
  strongest = adjudicate(beliefs)

  agent        = strongest.agent
  time         = strongest.time
  precondition = Atom.from_string("emergency")
  land         = strongest.formula.args[2]
  # TODO Fix this to match func below if that one works
  formula      = Atom.from_string("(happens (action " + str(agent) + " land(" + str(land) + ")) " + str(time) + "'")

  jus = Justification(isgiven=False, formula=beliefs, schema="Ethical Principle for Scenarios with Uncertain Ethical Outcomes")
  return Knowledge.from_args(agent, time, Obligation.from_args(agent, time, precondition, formula), jus)



# beliefs -- List(SFBelief)
# Implements the ethical principle for the pilot dilemma case study
# presented in the paper "Toward Defeasible Multi-Operator
# Argumentation Systems" by Bringsjord, Giancola, & Govindarajulu
def uncertain_belief_ethical_principle_pilot(beliefs):
  strongest = adjudicate(beliefs)

  agent        = strongest.agent
  time         = strongest.time
  precondition = strongest

  # Adjudicator believes the plane will crash
  if isinstance(strongest.formula, Predicate) and strongest.formula.name == "Crash":
    formula = Function.from_args("happens", [Function.from_args("action", [agent, Atom.from_string("hide_iru_data")]), time + "'"])

  # Adjudicator believes the plane will not crash
  elif isinstance(strongest.formula, Not) and isinstance(strongest.formula.args[0], Predicate) and strongest.formula.args[0].name == "Crash":
    formula = Function.from_args("happens", [Function.from_args("action", [agent, Atom.from_string("show_iru1_data")]), time + "'"])

  jus = Justification(isgiven=False, formula=beliefs, schema="Ethical Principle for Potential IRU Failure")
  return Knowledge.from_args(agent, time, Obligation.from_args(agent, time, precondition, formula), jus)
