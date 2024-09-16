from knapsack import solve_knapsack_with_constraints


def test_knapsack_with_constraints():
    sizes = [2, 3, 4, 5]
    values = [1, 2, 5, 6]
    capacity = 8
    together = {(0, 1)}
    apart = {(1, 3)}
    result = solve_knapsack_with_constraints(sizes, values, capacity, together, apart)
    print("Got result:", result)

    expected_value = 6
    assert abs(result[0] - expected_value) < 1e-6
    assert set(result[1]) == {3}


def test_knapsack_with_constraints2():
    sizes = [1, 2]
    values = [1, 2]
    capacity = 1
    together = {(0, 1)}
    apart = set()
    result = solve_knapsack_with_constraints(sizes, values, capacity, together, apart)
    print("Got result:", result)

    expected_value = 0
    assert abs(result[0] - expected_value) < 1e-6
    assert set(result[1]) == set()


def test_knapsack_with_constraints3():
    sizes = [1, 2]
    values = [1, 2]
    capacity = 3
    together = set()
    apart = {(0, 1)}
    result = solve_knapsack_with_constraints(sizes, values, capacity, together, apart)
    print("Got result:", result)

    expected_value = 2
    assert abs(result[0] - expected_value) < 1e-6
    assert set(result[1]) == {1}



if __name__ == "__main__":
    test_knapsack_with_constraints()
    test_knapsack_with_constraints2()
    test_knapsack_with_constraints3()
    print("knapsack with constraints test passed!")