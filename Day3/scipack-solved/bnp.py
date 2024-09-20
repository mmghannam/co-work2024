from typing import List
from pyscipopt import Model, SCIP_PARAMSETTING

from branching_eventhdlr import RyanFosterBranchingEventhdlr
from pricer import KnapsackPricer
from ryan_foster import RyanFoster


def extended_binpacking(sizes: List[int], capacity: int):
    model = Model("Extended Binpacking")

    model.setPresolve(SCIP_PARAMSETTING.OFF)
    model.setSeparating(SCIP_PARAMSETTING.OFF)
    model.setParam("display/freq", 1) # show the output log after each node

    x = {}
    # create one item per bin variables
    for i in range(len(sizes)):
        x[i] = model.addVar(vtype="B", name=f"{[i]}", obj=1)

    # add constraints that ensure that each item is packed into exactly one bin
    constraints = {}
    for i in range(len(sizes)):
        constraints[i] = model.addCons(x[i] >= 1, modifiable=True)

    branching_rule = RyanFoster()
    eventhdlr = RyanFosterBranchingEventhdlr(branching_rule.branching_decisions)
    pricer = KnapsackPricer(sizes, capacity, constraints,
                            branching_rule.branching_decisions)

    model.includeEventhdlr(eventhdlr, "Ryan Foster Branching Event Handler", "")
    model.includePricer(pricer, "KnapsackPricer",
                        "Pricer for Knapsack Problem")
    model.includeBranchrule(branching_rule, "RyanFoster", "Branching rule for Ryan Foster", priority=1000000,
                            maxdepth=-1,
                            maxbounddist=1.0)

    return model, x, constraints
