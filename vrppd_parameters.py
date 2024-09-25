import numpy as np
import cython

@cython.cclass
class Parameters:
    #instance_name: str
    delivery_count =  cython.declare(int, visibility='public')
    delivery_capacity =  cython.declare(cython.int[:], visibility='public')
    delivery_release_time =  cython.declare(cython.double[:], visibility='public')
    delivery_pickup_location =  cython.declare(cython.int[:], visibility='public')
    delivery_dropoff_location =  cython.declare(cython.int[:], visibility='public')

    courier_count =  cython.declare(int, visibility='public')
    courier_capacity =  cython.declare(cython.int[:], visibility='public')
    courier_starting_location =  cython.declare(cython.int[:], visibility='public')

    location_count =  cython.declare(int, visibility='public')
    location_distance_matrix =  cython.declare(cython.double[:,:], visibility='public')
    location_nearest_location_matrix =  cython.declare(cython.int[:,:], visibility='public')
    location_nearest_delivery_matrix =  cython.declare(cython.int[:,:], visibility='public')

    def __init__(self, instance: dict):
        #self.instance_name = instance['instance_name']

        self.delivery_count = len(instance['deliveries'])
        self.delivery_capacity = np.array([delivery.capacity for delivery in instance['deliveries']], dtype=np.dtype("i"))
        self.delivery_release_time = np.array([delivery.time_window_start for delivery in instance['deliveries']], dtype=np.dtype("d"))
        self.delivery_pickup_location = np.array([delivery.pickup_loc - 1 for delivery in instance['deliveries']], dtype=np.dtype("i"))
        self.delivery_dropoff_location = np.array([delivery.dropoff_loc - 1 for delivery in instance['deliveries']], dtype=np.dtype("i"))

        self.courier_count = len(instance['couriers'])
        self.courier_capacity = np.array([courier.capacity for courier in instance['couriers']], dtype=np.dtype("i"))
        self.courier_starting_location = np.array([courier.location - 1 for courier in instance['couriers']], dtype=np.dtype("i"))

        self.location_count = len(instance['travel_time'])-1
        self.location_distance_matrix = np.array(
            [   
                [
                    instance['travel_time'][i][j] 
                    for i in range(1,self.location_count+1)
                ] 
                for j in range(1,self.location_count+1)
            ],
            dtype=np.dtype("d")
        )

        self.location_nearest_location_matrix = np.array(
                [list(np.setdiff1d(np.argsort(self.location_distance_matrix[i]),[i],assume_unique=True)) for i in range(self.location_count)],
                dtype=np.dtype("i")
            )

        self.location_nearest_delivery_matrix = np.array(
            [list(np.argsort([self.location_distance_matrix[i][self.delivery_pickup_location[j]] for j in range(self.delivery_count)]) + 1) for i in range(self.location_count)],
            dtype=np.dtype("i")
        )

            
            
        



