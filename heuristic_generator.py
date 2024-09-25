import numpy as np
import vrppd_parameters
import vrppd_solution
import math
import cython

@cython.cclass
class CourierState:
    courier_index = cython.declare(cython.int, visibility='public')
    current_location = cython.declare(cython.int, visibility='public')
    current_time = cython.declare(cython.double, visibility='public')

    def __init__(self, courier_index, current_location, current_time):
        self.courier_index = courier_index
        self.current_location = current_location
        self.current_time = current_time

@cython.cclass
class CourierMove:
    courier_index = cython.declare(cython.int, visibility='public')
    delivery_index = cython.declare(cython.int, visibility='public')
    cost = cython.declare(cython.double, visibility='public')
    move_appends = cython.declare(cython.bint, visibility='public')

    def __init__(self, courier_index, delivery_index, cost, move_appends = True):
        self.courier_index = courier_index
        self.delivery_index = delivery_index
        self.cost = cost
        self.move_appends = move_appends

@cython.cfunc
def apply_courier_move(param: vrppd_parameters.Parameters, sol: vrppd_solution.Solution, courier_state: CourierState, courier_move: CourierMove):
    if courier_move.move_appends:
        delivery_dropoff_location: int = param.delivery_dropoff_location[courier_move.delivery_index - 1]
        delivery_delivery_time: cython.double = append_delivery_delivery_time(param, sol, courier_state, courier_move.delivery_index)
        courier_state.current_location = delivery_dropoff_location
        courier_state.current_time = delivery_delivery_time
        sol.total_delivery_time += delivery_delivery_time
        sol.routing_plan[courier_move.courier_index - 1][2*sol.delivery_count_assigned_to_courier[courier_move.courier_index - 1]] = courier_move.delivery_index
        sol.routing_plan[courier_move.courier_index - 1][2*sol.delivery_count_assigned_to_courier[courier_move.courier_index - 1] + 1] = -courier_move.delivery_index
        sol.delivery_assigned_courier[courier_move.delivery_index - 1] = courier_move.courier_index
        sol.delivery_count_assigned_to_courier[courier_move.courier_index - 1] += 1
        sol.delivery_delivery_time[courier_move.delivery_index - 1] = delivery_delivery_time
        sol.courier_attributed_delivery_time[courier_move.courier_index - 1] += delivery_delivery_time
    else:
        raise Exception('Not implemented')

@cython.cfunc
def append_delivery_delivery_time(param: vrppd_parameters.Parameters, sol: vrppd_solution.Solution, courier_state: CourierState, delivery_index: np.int64):
    delivery_pickup_location: int = param.delivery_pickup_location[delivery_index - 1]
    delivery_dropoff_location: int = param.delivery_dropoff_location[delivery_index - 1]
    delivery_time: cython.double = (
        max(
            courier_state.current_time
            + param.location_distance_matrix[
                courier_state.current_location
            ][
                delivery_pickup_location
            ] 
            , 
            param.delivery_release_time[delivery_index - 1]
        )
        + param.location_distance_matrix[delivery_pickup_location][delivery_dropoff_location]
    )
    return delivery_time

@cython.cclass
class greedy_delivery_finder:
    count_of_already_considered_closest_deliveries_from_location: cython.int[:]
    def __init__(self, param: vrppd_parameters.Parameters):
        self.count_of_already_considered_closest_deliveries_from_location = np.zeros(param.location_count, dtype=np.dtype("i"))

    def greedy_delivery_of_courier(self, param: vrppd_parameters.Parameters, sol: vrppd_solution.Solution, courier_state: CourierState):
        current_location: cython.int = courier_state.current_location
        for i in range(self.count_of_already_considered_closest_deliveries_from_location[current_location], param.delivery_count):
            closest_delivery: cython.int = param.location_nearest_delivery_matrix[current_location][i]
            if sol.delivery_assigned_courier[closest_delivery - 1] > 0 or param.delivery_capacity[closest_delivery - 1] > param.courier_capacity[courier_state.courier_index - 1]:
                self.count_of_already_considered_closest_deliveries_from_location[current_location] += 1
            else:
                delivery_time: cython.double = append_delivery_delivery_time(param, sol, courier_state, closest_delivery)
                return CourierMove(courier_state.courier_index, closest_delivery, delivery_time, True)

        return CourierMove(courier_state.courier_index, 0, float('inf'), False)


def random_greedy_courier_heuristic(param: vrppd_parameters.Parameters, sol: vrppd_solution.Solution):
    sol.total_delivery_time = 0
    
    # Only implement with append moves
    greedy_delivery_finder_singleton : greedy_delivery_finder = greedy_delivery_finder(param)

    courier_states = [
            CourierState(
                courier_index, 
                param.courier_starting_location[courier_index - 1], 
                0
        ) for courier_index in range(1,param.courier_count+1)
    ]

    iteration: cython.int = 0
    assigned_deliveries: cython.int = 0
    prob: cython.double = 0
    while assigned_deliveries < param.delivery_count:
        iteration += 1
        greedy_courier_moves = [greedy_delivery_finder_singleton.greedy_delivery_of_courier(param, sol, courier_state) for courier_state in courier_states]
        greedy_courier_moves.sort(key = lambda x: x.cost)
        random_probability_vector: np.ndarray[np.int64] = np.random.rand(param.courier_count)
        for courier_move in greedy_courier_moves:
            if assigned_deliveries == param.delivery_count:
                break
            prob = random_probability_vector[courier_move.courier_index - 1]
            prob = prob * prob
            if prob <= (assigned_deliveries+1)/param.delivery_count:
                if sol.delivery_assigned_courier[courier_move.delivery_index - 1] == 0:
                    sol.delivery_assigned_courier[courier_move.delivery_index - 1] = courier_move.courier_index
                    assigned_deliveries += 1
                    apply_courier_move(param, sol, courier_states[courier_move.courier_index - 1], courier_move)
    return sol
