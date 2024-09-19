from bnp import extended_binpacking
from compact import binpacking_compact
from generator import random_bin_packing_instance

if __name__ == "__main__":
    compact = False
    
    capacity = 100
    sizes = random_bin_packing_instance(20, capacity)


    if compact:
        model = binpacking_compact(sizes, capacity)
    else:
        model, *_ = extended_binpacking(sizes, capacity)

    model.setParam("display/freq", 1) # show the output log after each node
    model.redirectOutput()
    model.optimize()

    print("objective value", model.getObjVal())
    print("Solution:")
    for var in model.getVars(transformed=True):
        val = model.getVal(var)
        if val > 1e-6:
            var_name = str(var).replace("t_", "")
            print(var_name, end=", ")