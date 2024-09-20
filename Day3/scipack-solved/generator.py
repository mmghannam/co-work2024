def random_bin_packing_instance(
    num_items: int, capacity: int, seed: int = 0,
    ):
    import random
    
    random.seed(seed)
    
    return [random.randint(1, capacity) for _ in range(num_items)]



def test_random_bin_packing_instance():
    from compact import binpacking_compact
    
    capacity = 100
    sizes = random_bin_packing_instance(35, capacity)
    
    model = binpacking_compact(sizes, capacity)
    
    model.optimize()