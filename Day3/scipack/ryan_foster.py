from typing import List
from pyscipopt import Branchrule, SCIP_RESULT

class RyanFoster(Branchrule):
    def __init__(self, *args, **kwargs):
        """ 
        Branching decisions are stored in a dictionary, where the key is the node number
        and the value is a dictionary with the keys "together" and "apart"
        the value of "together" is a set of pairs of items that must be in the same bin
        the value of "apart" is a set of pairs of items that must be in different bins. 
        """
        super().__init__(*args, **kwargs)
        self.branching_decisions = {
            1: { # root node
                "together": set(),
                "apart": set(),
            }
        }
    
    def branchexeclp(self, allowaddcons):
        # get the fractional variables from the LP solution
        lpcands, lpcandssol, *_ = self.model.getLPBranchCands()
        
        patterns_with_vals = [
            (eval(var.name.replace("t_", "")), val) for var, val in zip(lpcands, lpcandssol)
        ]
        
        # TODO (Exercise 2: choose a fractional pair to branch on)
        chosen_pair = choose_fractional_pair(patterns_with_vals)
        
        parent_together = set()
        parent_apart = set()
        
        # get the branching decisions of the parent node
        parent = self.model.getCurrentNode().getParent()
        if parent:
            parent_together = set(self.branching_decisions[parent.getNumber()]["together"])
            parent_apart = set(self.branching_decisions[parent.getNumber()]["apart"])
        
                                
        # Left subproblem: enforce that pair is in the same bin
        left_node = self.model.createChild(0, 0)
        
        raise NotImplementedError("Complete the following: what should be the value of together and apart?")
        # self.branching_decisions[left_node.getNumber()] = {
        #     "together": ?,
        #     "apart": ?
        # }

        # Right subproblem: enforce that pair is in different bins
        right_node = self.model.createChild(0, 0)

        raise NotImplementedError("Complete the following: what should be the value of together and apart?")
        # self.branching_decisions[right_node.getNumber()] = {
            # "together": ?,
            # "apart": ?
        # }
        
        return {"result": SCIP_RESULT.BRANCHED}


def all_fractional_pairs(patterns_with_vals: List[tuple[List[int], float]]) -> List[tuple[int, int]]:
    """
    Find all pairs of items that are fractional in the LP solution

    Parameters:
    patterns_with_vals: List[tuple[List[int], float]] - a list of packings and the value of the variable in the LP solution

    Returns:
    List[tuple[int, int]] - a list of pairs of items that are fractional in the LP solution
    """

    raise NotImplementedError("Implement this function")


def choose_fractional_pair(patterns_with_vals: List[tuple[List[int], float]]) -> tuple[int, int]:
    """
    Choose a fractional pair to branch on
    
    Parameters:
    fractional_vars: List[tuple[List[int], float]] - a list of packings and the value of the variable in the LP solution
    
    Returns:
    tuple[int, int] - the pair of items to branch on
    """
    
    first_pair = all_fractional_pairs(patterns_with_vals)[0]
    return first_pair