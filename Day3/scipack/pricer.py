import math
from pyscipopt import Pricer, SCIP_RESULT
from knapsack import pricing_solver

class KnapsackPricer(Pricer):
    def __init__(self, sizes, capacity, constraints, branching_decisions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sizes = sizes
        self.capacity = capacity
        self.constraints = constraints
        self.branching_decisions = branching_decisions
        self.i = 0
    
    def price(self, farkas):
        branching_decisions = self.branching_decisions[self.model.getCurrentNode().getNumber()]
        
        if self.i % 10 == 0:
            print("--lp obj:", self.model.getLPObjVal())
        
        dual_sol = {}
        for (cons_id, cons) in self.constraints.items():
            cons = self.model.getTransformedCons(cons)
            if farkas:
                dual_sol[cons_id] = self.model.getDualfarkasLinear(cons)
            else:
                dual_sol[cons_id] = self.model.getDualsolLinear(cons)   
                
        
        min_red_cost, pattern = pricing_solver(self.sizes, self.capacity, dual_sol, branching_decisions["together"], branching_decisions["apart"])

        if farkas:
            min_red_cost -= 1 # in farkas' pricing the objective fn. coefficient is 0

        if min_red_cost < 0:
            new_var = self.model.addVar(vtype="B", name=f"{pattern}", obj=1, pricedVar=True)
            for item in pattern:
                item_constraint = self.constraints[item]
                item_constraint = self.model.getTransformedCons(item_constraint)
                self.model.addConsCoeff(item_constraint, new_var, 1)
        
        
        return {
            'result': SCIP_RESULT.SUCCESS,
        }
        
    def pricerredcost(self):
        self.i += 1
        return self.price(farkas=False)
    
    def pricerfarkas(self):
        self.i += 1
        return self.price(farkas=True)
        
        
