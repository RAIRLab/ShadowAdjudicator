# ShadowAdjudicator
A system for adjudicating arguments amongst two or more AI agents reasoning in a quantified modal logic.

This proposed system (which is in the very early stages of development) will adjudicate arguments using a nascent system for measuring uncertainty in modal logics called [Strength Factors](https://arxiv.org/pdf/1705.10726.pdf). ShadowAdjudicator will implement methods for determining the strength of an argument (specifically, arguments crafted using the syntax and inference rules of a modal logic) and adjudicating arguments between agents. This will all be supported by the use of [ShadowProver](https://github.com/naveensundarg/prover) as the backend reasoner.
