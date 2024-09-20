from typing import List

from pyscipopt import Model


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
    tuple[float, List[int]] - the minimum reduced cost and the packing of the items
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
    Solve the knapsack problem

    Parameters:
    sizes: List[int] - the sizes of the items
    values: List[float] - the values of the items
    capacity: int - the capacity of the knapsack

    Returns:
    tuple[float, List[int]] - the optimal value and the packing of the items
    """

    m = Model("knapsack")
    m.hideOutput()
    x = {}
    for i in range(len(sizes)):
        x[i] = m.addVar(vtype="B", name=f"x{i}", obj=values[i])

    m.addCons(sum(sizes[i] * x[i] for i in range(len(sizes))) <= capacity)

    m.setMaximize()
    m.optimize()

    packing = [i for i in range(len(sizes)) if m.getVal(x[i]) > 0.5]
    return m.getObjVal(), packing


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
    tuple[float, List[int]] - the optimal value and the packing of the items
    """

    m = Model("knapsack_with_constraints")
    m.hideOutput()

    x = {}
    for i in range(len(sizes)):
        x[i] = m.addVar(vtype="B", name=f"x{i}", obj=values[i])

    m.addCons(sum(sizes[i] * x[i] for i in range(len(sizes))) <= capacity)

    for i, j in together:
        m.addCons(x[i] == x[j])

    for i, j in apart:
        m.addCons(x[i] + x[j] <= 1)

    m.setMaximize()

    m.optimize()

    packing = [i for i in range(len(sizes)) if m.getVal(x[i]) > 0.5]
    return m.getObjVal(), packing