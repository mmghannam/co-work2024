from typing import List
import pyscipopt as scip


def pricing_solver(sizes: List[int], capacity: int, dual_solution: dict[float], together: set[tuple[int, int]],
                   apart: set[tuple[int, int]]) -> tuple[float, List[int]]:
    """
    Solve the pricing problem for the knapsack problem (with branching constraints)
    
    Parameters:
    sizes: List[int] - the sizes of the items
    capacity: int - the capacity of the knapsack
    dual_solution: dict[float] - the dual solution of the linear relaxation
    together: set[tuple[int]] - the pairs of items that must be together
    apart: set[tuple[int]] - the pairs of items that must be apart
    
    Returns:
    tuple[float, List[int]] - the minimum reduced cost and the pattern of the items    
    """

    profits = [dual_solution[i] for i in range(len(sizes))]
    if len(together) > 0 or len(apart) > 0:
        result = solve_knapsack_with_constraints(sizes, profits, capacity, together, apart)
    else:
        result = solve_knapsack(sizes, profits, capacity)

    min_red_cost = 1 - result[0]

    return min_red_cost, result[1]


def solve_knapsack(sizes: List[int], values: List[float], capacity: int) -> tuple[float, List[int]]:
    """
    Solve the knapsack problem with branching constraints

    Parameters:
    sizes: List[int] - the sizes of the items
    values: List[float] - the values of the items
    capacity: int - the capacity of the knapsack

    Returns:
    tuple[float, List[int]] - the optimal value and the pattern of the items
    """
    n = len(sizes)
    model = scip.Model("knapsack_mip")
    # Create binary variables for each item
    x = [model.addVar(vtype='B', name=f'x{i}') for i in range(n)]

    # Set the objective function (maximize total value)
    model.setObjective(scip.quicksum(values[i] * x[i] for i in range(n)), sense="maximize")

    # Add the knapsack constraint (total weight <= capacity)
    model.addCons(scip.quicksum(sizes[i] * x[i] for i in range(n)) <= capacity, name='knapsack_constraint')

    # Optimize the model
    model.optimize()

     # Get the optimal value and selected items
    opt_value = model.getObjVal()

    selected_items = [i for i in range(n) if model.getVal(x[i]) == 1]

    return tuple([opt_value, selected_items])

def solve_knapsack_with_constraints(
        sizes: List[int], values: List[float], capacity: int, together: set[tuple[int, int]],
        apart: set[tuple[int, int]]
) -> tuple[float, List[int]]:
    """
    Solve the knapsack problem with branching constraints

    Parameters:
    sizes: List[int] - the sizes of the items
    values: List[float] - the values of the items
    capacity: int - the capacity of the knapsack
    together: set[tuple[int]] - the pairs of items that must be together
    apart: set[tuple[int]] - the pairs of items that must be apart

    Returns:
    tuple[float, List[int]] - the optimal value and the pattern of the items
    """

    raise NotImplementedError("The knapsack solver with constraints is not implemented yet")
