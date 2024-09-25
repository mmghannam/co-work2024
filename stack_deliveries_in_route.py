from vrppd_parameters import Parameters
from vrppd_solution import Solution
import numpy as np
import itertools

def catalan_combinations(n):
    def backtrack(s=[], open=0, close=0):
        if len(s) == 2 * n:
            result.append(s)
            return
        if open < n:
            backtrack(s + [0], open + 1, close)
        if close < open:
            backtrack(s + [1], open, close + 1)

    result = []
    backtrack()

    for i in range(len(result)):
        open_bracket_count = 1
        closed_bracket_count = 1
        for j in range(len(result[i])):
            if result[i][j] == 0:
                result[i][j] = open_bracket_count
                open_bracket_count += 1
            else:
                result[i][j] = -closed_bracket_count
                closed_bracket_count += 1
    return result

catalan_combinations_list = [catalan_combinations(i) for i in range(0, 6)]

def delivery_time_of_rerouting(param: Parameters, sol: Solution, courier_index: int, new_route: np.array):
    courier_attributed_delivery_time = 0
    current_time = 0
    current_location = param.courier_starting_location[courier_index - 1]
    for i in range(2*sol.delivery_count_assigned_to_courier[courier_index - 1]):
        if new_route[i] > 0:
            current_time = max(
                current_time 
                + param.location_distance_matrix[current_location][param.delivery_pickup_location[new_route[i] - 1]], 
                param.delivery_release_time[new_route[i] - 1]
            )
            current_location = param.delivery_pickup_location[new_route[i] - 1]
        elif new_route[i] < 0:
            current_time += param.location_distance_matrix[current_location][param.delivery_dropoff_location[-new_route[i] - 1]] 
            courier_attributed_delivery_time += current_time
            current_location = param.delivery_dropoff_location[-new_route[i] - 1]
        else:
            break
    return courier_attributed_delivery_time

def apply_rerouting(param: Parameters, sol: Solution, courier_index: int, new_route: np.array):
    #print(f'old route: {sol.routing_plan[courier_index - 1]}')
    #print(f'new route: {new_route}')
    #print(f'old courier attributed delivery time: {sol.courier_attributed_delivery_time[courier_index - 1]}')
    #print(f'delivery delivery time before rerouting: {sol.delivery_delivery_time}')
    #print(f'total delivery time before rerouting: {sol.total_delivery_time}')

    sol.routing_plan[courier_index - 1] = new_route
    old_courier_attributed_delivery_time = sol.courier_attributed_delivery_time[courier_index - 1]
    sol.courier_attributed_delivery_time[courier_index - 1] = 0
    current_time = 0
    current_location = param.courier_starting_location[courier_index - 1]
    for i in range(2*sol.delivery_count_assigned_to_courier[courier_index - 1]):
        if new_route[i] > 0:
            current_time = max(
                current_time 
                + param.location_distance_matrix[current_location][param.delivery_pickup_location[new_route[i] - 1]], 
                param.delivery_release_time[new_route[i] - 1]
            )
            current_location = param.delivery_pickup_location[new_route[i] - 1]
        elif new_route[i] < 0:
            sol.delivery_delivery_time[-new_route[i] - 1] = current_time + param.location_distance_matrix[current_location][param.delivery_dropoff_location[-new_route[i] - 1]]
            current_time = sol.delivery_delivery_time[-new_route[i] -1]
            current_location = param.delivery_dropoff_location[-new_route[i] - 1]
            sol.courier_attributed_delivery_time[courier_index - 1] += current_time
    #print("####")
    #print(f' former total delivery time {sol.total_delivery_time}')
    #print(f' old courier {old_courier_attributed_delivery_time}')
    #print(f' new courier {sol.courier_attributed_delivery_time[courier_index - 1]}')
    sol.total_delivery_time = sol.total_delivery_time - old_courier_attributed_delivery_time + sol.courier_attributed_delivery_time[courier_index - 1]
    #print(f'new courier attributed delivery time: {sol.courier_attributed_delivery_time[courier_index - 1]}')
    #print(f'delivery delivery time after rerouting: {sol.delivery_delivery_time}')
    #print(f'total delivery time after rerouting: {sol.total_delivery_time}')

def stack_courier_deliveries(param: Parameters, sol: Solution, courier_index: int):
    if sol.delivery_count_assigned_to_courier[courier_index - 1] <= 1:
        return
    #print('####')
    #print(f'route before local improvement: {sol.routing_plan[courier_index - 1]}')
    #print(f'route length before local improvement: {sol.courier_attributed_delivery_time[courier_index - 1]}')

    # Initialize variables, change this later to object variables
    best_route = sol.routing_plan[courier_index - 1]
    best_route_total_delivery_time = sol.courier_attributed_delivery_time[courier_index - 1]

    incumbent_route = np.zeros(2*param.delivery_count, dtype=int)

    deliveries_in_route = np.zeros(sol.delivery_count_assigned_to_courier[courier_index - 1], dtype=int)
    temp_counted_deliveries = 0
    for i in range(2*sol.delivery_count_assigned_to_courier[courier_index - 1]):
        if sol.routing_plan[courier_index - 1][i] == 0:
            break
        elif sol.routing_plan[courier_index - 1][i] > 0:
            deliveries_in_route[temp_counted_deliveries] = sol.routing_plan[courier_index - 1][i]
            temp_counted_deliveries += 1
    
    # Case distinction: 
    # If there are less than six deliveries in the route, we consider all permutations of the deliveries in the route
    # If there are six or more deliveries in the route, we reinsert orders using local search until no improvement is possible
    if sol.delivery_count_assigned_to_courier[courier_index - 1] < 6:
        route_variant = itertools.product(
            itertools.permutations(deliveries_in_route), 
            catalan_combinations_list[sol.delivery_count_assigned_to_courier[courier_index - 1]]
        )
        for (permutation, combination) in route_variant:
            # Construct the route from the (permutation, combination)-encoding
            for i in range(2*sol.delivery_count_assigned_to_courier[courier_index - 1]):
                if combination[i] > 0:
                    incumbent_route[i] = permutation[combination[i] - 1]
                else:
                    incumbent_route[i] = -permutation[-combination[i] - 1]
            incumbent_route_total_delivery_time = delivery_time_of_rerouting(param, sol, courier_index, incumbent_route)
            if incumbent_route_total_delivery_time <= best_route_total_delivery_time:
                best_route = incumbent_route.copy()
                best_route_total_delivery_time = incumbent_route_total_delivery_time
    else:
        pass

    # Update the solution
    apply_rerouting(param, sol, courier_index, best_route)

        
def stack_deliveries_in_route(param: Parameters, sol: Solution):
    best_route = np.zeros(2*param.delivery_count, dtype=int)
    incumbent_route = np.zeros(2*param.delivery_count, dtype=int)
    deliveries_in_route = np.zeros(param.delivery_count, dtype=int)
    for courier_index in range(1,param.courier_count+1):
        stack_courier_deliveries(param, sol, courier_index)
        
                    



        

        





