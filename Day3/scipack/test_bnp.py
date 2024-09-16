from bnp import extended_binpacking
from generator import random_bin_packing_instance

def test_bnp():
    capacity = 100
    sizes = random_bin_packing_instance(100, capacity)

    model, *_ = extended_binpacking(sizes, capacity)
    model.optimize()

    assert abs(model.getObjVal() - 52) < 1e-6


if __name__ == "__main__":
    test_bnp()
    print("bnp test passed!")