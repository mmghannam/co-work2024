import cython
import numpy as np
from vrppd_parameters import Parameters
import sys

@cython.cclass
class Solution:
    total_delivery_time = cython.declare(cython.double, visibility='public')

    # routing_plan: 2D array of size (courier_count, 2*delivery_count)
    # If courier i picks up delivery j at the k'th location then routing_plan[i][k] = j
    # If courier i delivers delivery j at the k'th location then routing_plan[i][k] = -j
    routing_plan =  cython.declare(cython.int[:,:], visibility='public')

    # delivery_count_assigned_to_courier: 1D array of size courier_count
    # delivery_count_assigned_to_courier[i] = number of deliverys assigned to courier i
    delivery_count_assigned_to_courier =  cython.declare(cython.int[:], visibility='public')

    # delivery_delivery_time: 1D array of size delivery_count
    # delivery_delivery_time[i] = time at which delivery i is delivered
    delivery_delivery_time =  cython.declare(cython.double[:], visibility='public')

    # delivery_assigned_courier: 1D array of size delivery_count
    # delivery_assigned_courier[i] = courier assigned to delivery i
    delivery_assigned_courier =  cython.declare(cython.int[:], visibility='public')

    # courier_attributed_delivery_time: 1D array of size courier_count
    # courier_attributed_delivery_time[i] = sum of delivery times of deliveries performed by courier i
    courier_attributed_delivery_time =  cython.declare(cython.double[:], visibility='public')

    # courier_current_load: 1D array of size courier_count
    # courier_current_load[i] = current load of courier i
    courier_current_load =  cython.declare(cython.double[:], visibility='public')

    def __init__(self, parameters: Parameters):
        self.total_delivery_time = float(sys.maxsize)
        self.routing_plan = np.zeros((parameters.courier_count, 2*parameters.delivery_count), dtype=np.dtype("i"))
        self.delivery_count_assigned_to_courier = np.zeros(parameters.courier_count, dtype=np.dtype("i"))
        self.delivery_delivery_time = np.zeros(parameters.delivery_count, dtype=np.dtype("d"))
        self.delivery_assigned_courier = np.zeros(parameters.delivery_count, dtype=np.dtype("i"))
        self.courier_attributed_delivery_time = np.zeros(parameters.courier_count, dtype=np.dtype("d"))
        self.courier_current_load = np.zeros(parameters.courier_count, dtype=np.dtype("d"))
