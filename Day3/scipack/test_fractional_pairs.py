from ryan_foster import all_fractional_pairs

def test_fractional_pairs():
    patterns_with_vals = [
        ([0, 1, 2], 0.5),
        ([0], 0.5),
        ([1, 2], 0.5),
    ]

    pairs = all_fractional_pairs(patterns_with_vals)
    print("Got pairs:", pairs)

    assert len(pairs) == 2

    pairs = [set(pair) for pair in pairs]
    assert {0, 1} in pairs
    assert {0, 2} in pairs


def test_fractional_pairs2():
    patterns_with_vals = [
        ([0, 1, 2, 3], 0.5),
        ([0, 1], 0.5),
        ([2, 3], 0.5),
    ]

    pairs = all_fractional_pairs(patterns_with_vals)
    print("Got pairs:", pairs)

    assert len(pairs) == 4

    pairs = [set(pair) for pair in pairs]
    assert {0, 2} in pairs
    assert {0, 3} in pairs
    assert {1, 2} in pairs
    assert {1, 3} in pairs


if __name__ == "__main__":
    test_fractional_pairs()
    test_fractional_pairs2()
    print("Fractional pairs test passed!")