from knapsack import solve_knapsack, solve_knapsack_with_constraints

def test_solve_knapsack():
    sizes = [2, 3, 4, 5]
    values = [1, 2, 5, 6]
    capacity = 8
    result = solve_knapsack(sizes, values, capacity)
    print("Got result:", result)

    expected_value = 8
    assert abs(result[0] - expected_value) < 1e-6
    assert set(result[1]) == {1, 3}

    capacity = 0
    result = solve_knapsack(sizes, values, capacity)
    assert abs(result[0] - 0) < 1e-6


if __name__ == "__main__":
    test_solve_knapsack()
    print("knapsack test passed!")
