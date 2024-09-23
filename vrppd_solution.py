import numpy as np
import numba
import sys



class Solution:
    total_delivery_time = float(sys.maxsize)

    # routing_plan: 2D array of size (courier_count, 2*delivery_count)
    # If courier i picks up delivery j at the k'th location then routing_plan[i][k] = j
    # If courier i delivers delivery j at the k'th location then routing_plan[i][k] = -j
    routing_plan = np.array([])

    # delivery_count_assigned_to_courier: 1D array of size courier_count
    # delivery_count_assigned_to_courier[i] = number of deliverys assigned to courier i
    delivery_count_assigned_to_courier = np.array([])

    # delivery_delivery_time: 1D array of size delivery_count
    # delivery_delivery_time[i] = time at which delivery i is delivered
    delivery_delivery_time = np.array([])

    # delivery_assigned_courier: 1D array of size delivery_count
    # delivery_assigned_courier[i] = courier assigned to delivery i
    delivery_assigned_courier = np.array([])

    def __init__(self, delivery_count, courier_count):
        self.routing_plan = np.zeros((courier_count, 2*delivery_count), dtype=int)
        self.delivery_count_assigned_to_courier = np.zeros(courier_count, dtype=int)
        self.delivery_delivery_time = np.zeros(delivery_count, dtype=float)
        self.delivery_assigned_courier = np.zeros(delivery_count, dtype=int)

    def __init__(self, parameters):
        self.routing_plan = np.zeros((parameters.courier_count, 2*parameters.delivery_count), dtype=int)
        self.delivery_count_assigned_to_courier = np.zeros(parameters.courier_count, dtype=int)
        self.delivery_delivery_time = np.zeros(parameters.delivery_count, dtype=float)
        self.delivery_assigned_courier = np.zeros(parameters.delivery_count, dtype=int)
