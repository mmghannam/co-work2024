import vrppd_solution
import vrppd_parameters


def is_feasible(param: vrppd_parameters.Parameters, sol: vrppd_solution.Solution):
    feasibility = True

    # Check if every delivery is assigned to a courier
    for i in range(param.delivery_count):
        if sol.delivery_assigned_courier[i] <= 0:
            print(f"Delivery {i+1} is not assigned to any courier")
            feasibility = False
        
    # Check if the assigned courier first picks up and then delivers the delivery
    for i in range(1,param.delivery_count+1):
        delivery_courier = sol.delivery_assigned_courier[i-1]

        is_picked_up = False
        is_delivered = False

        for j in range(2*param.delivery_count):
            if sol.routing_plan[delivery_courier-1][j] == i:
                is_picked_up = True
            if sol.routing_plan[delivery_courier-1][j] == -i:
                is_delivered = True
            if is_delivered and not is_picked_up:
                print(f"Delivery {i+1} is delivered before being picked up by courier {delivery_courier}")
                feasibility = False

        if not is_picked_up:
            print(f"Delivery {i+1} is not picked by courier {delivery_courier}")
            feasibility = False
        if not is_delivered:
            print(f"Delivery {i+1} is not delivered by courier {delivery_courier}")
            feasibility = False

    # Check if the time window of each delivery is not violated
    for i in range(param.delivery_count):
        pickup_location = param.delivery_pickup_location[i]
        dropoff_location = param.delivery_dropoff_location[i]
        if sol.delivery_delivery_time[i] - param.location_distance_matrix[pickup_location][dropoff_location] < param.delivery_release_time[i]:
            print(f"Time window of delivery {i+1} is violated")
            feasibility = False

    # Check if the capacity of each courier is not exceeded
    for i in range(param.courier_count):
        courier_capacity = 0
        for j in range(2*param.delivery_count):
            if sol.routing_plan[i][j] > 0:
                courier_capacity += param.delivery_capacity[sol.routing_plan[i][j] - 1]
            if sol.routing_plan[i][j] < 0:
                courier_capacity -= param.delivery_capacity[-sol.routing_plan[i][j] - 1]
            if courier_capacity > param.courier_capacities[i]:
                print(f"Capacity of courier {i+1} is exceeded")
                feasibility = False

    # Check if the travel time is feasible
    for i in range(param.courier_count):
        current_location = param.courier_starting_location[i]
        current_time = 0
        for j in range(2*param.delivery_count):
            if sol.routing_plan[i][j] > 0:
                delivery_pickup_location = param.delivery_pickup_location[sol.routing_plan[i][j] - 1]
                current_time += param.location_distance_matrix[current_location][delivery_pickup_location]
                if current_time < param.delivery_release_time[sol.routing_plan[i][j] - 1]:
                    current_time = param.delivery_release_time[sol.routing_plan[i][j] - 1]
                current_location = delivery_pickup_location
            if sol.routing_plan[i][j] < 0:
                delivery_dropoff_location = param.delivery_dropoff_location[-sol.routing_plan[i][j] - 1]
                current_time += param.location_distance_matrix[current_location][delivery_dropoff_location]
                if sol.delivery_delivery_time[-sol.routing_plan[i][j] - 1] > current_time:
                    print(f"Delivery {-sol.routing_plan[i][j]} is delivered before the courier can reach it")
                    feasibility = False
                current_location = delivery_dropoff_location

    # Check if the total delivery time equals the sum of delivery times
    total_delivery_time = 0
    for i in range(param.delivery_count):
        total_delivery_time += sol.delivery_delivery_time[i]
        
    if total_delivery_time != sol.total_delivery_time:
        print(f"Total delivery time is not equal to sum of delivery times")
        feasibility = False

    return feasibility






