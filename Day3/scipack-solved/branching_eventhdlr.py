import pyscipopt as scip

class RyanFosterBranchingEventhdlr(scip.Eventhdlr):
    def __init__(self, branching_decisions):
        self.branching_decisions = branching_decisions

    def eventinit(self):
        self.model.catchEvent(scip.SCIP_EVENTTYPE.NODEFOCUSED, self)

    def eventexec(self, event):
        apart = self.branching_decisions[self.model.getCurrentNode().getNumber()]["apart"]
        together = self.branching_decisions[self.model.getCurrentNode().getNumber()]["together"]
        
        
        for var in self.model.getVars(transformed=True):
            pattern = set(eval(var.name.replace("t_", "")))
            
            for pair in apart:
                intersection = pattern.intersection(set(pair))
                if len(intersection) == 2:
                    self.model.chgVarUb(var, 0)
            
            for pair in together:
                intersection = pattern.intersection(set(pair))
                if len(intersection) == 1:
                    self.model.chgVarUb(var, 0)
                    
