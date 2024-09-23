import numpy as np



class Parameters:
    instance_name = ''
    delivery_count = 0
    delivery_capacity = np.array([])
    delivery_release_time = np.array([])
    delivery_pickup_location = np.array([])
    delivery_dropoff_location = np.array([])

    courier_count = 0
    courier_capacities = np.array([])
    courier_starting_location = np.array([])

    location_count = 0
    location_distance_matrix = []
    location_nearest_location_matrix = []
    location_nearest_delivery_matrix = []

    def __init__(self, instance):
        self.instance_name = instance['instance_name']
        #print(instance)
        #print([courier.capacity for courier in instance['couriers']])
        
        self.delivery_count = len(instance['deliveries'])
        self.delivery_capacity = np.array([delivery.capacity for delivery in instance['deliveries']])
        self.delivery_release_time = np.array([delivery.time_window_start for delivery in instance['deliveries']])
        self.delivery_pickup_location = np.array([delivery.pickup_loc - 1 for delivery in instance['deliveries']])
        self.delivery_dropoff_location = np.array([delivery.dropoff_loc - 1 for delivery in instance['deliveries']])

        self.courier_count = len(instance['couriers'])
        self.courier_capacities = np.array([courier.capacity for courier in instance['couriers']])
        self.courier_starting_location = np.array([courier.location - 1 for courier in instance['couriers']])

        self.location_count = len(instance['travel_time'])-1
        self.location_distance_matrix = np.array(
            [   
                [
                    instance['travel_time'][i][j] 
                    for i in range(1,self.location_count+1)
                ] 
                for j in range(1,self.location_count+1)
            ]
        )

        self.location_nearest_location_matrix = np.zeros((self.location_count,self.location_count - 1),dtype=int)
        for i in range(self.location_count):
            self.location_nearest_location_matrix[i] = np.setdiff1d(
                                                            np.argsort(self.location_distance_matrix[i]),
                                                            [i],
                                                            assume_unique=True
                                                        )


        self.location_nearest_delivery_matrix = np.zeros((self.location_count,self.delivery_count),dtype=int)
        for i in range(self.location_count):
            self.location_nearest_delivery_matrix[i] = np.argsort(
                [self.location_distance_matrix[i][self.delivery_pickup_location[j]] for j in range(self.delivery_count)]
            ) + 1
        



