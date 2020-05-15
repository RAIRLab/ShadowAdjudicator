# ShadowAdjudicator
A system for adjudicating arguments amongst two or more AI agents reasoning in a quantified modal logic.

## Description

This proposed system (which is in the very early stages of development) will adjudicate arguments using a nascent system for measuring uncertainty in modal logics called [Strength Factors](https://arxiv.org/pdf/1705.10726.pdf). ShadowAdjudicator will implement methods for determining the strength of an argument (specifically, arguments crafted using the syntax and inference rules of a modal logic) and adjudicating arguments between agents. This will all be supported by the use of [ShadowProver](https://github.com/naveensundarg/prover) as the backend reasoner.

## Installation and Use

ShadowProver is integrated in this project as a Git submodule. Hence, to make sure you get everything, clone the project using the following command:

```git clone --recurse-submodules https://github.com/RAIRLab/ShadowAdjudicator```

For more information about Git submodules, see [here](https://git-scm.com/book/en/v2/Git-Tools-Submodules).
