import numpy as np
import vrppd_parameters
import vrppd_solution
import math
import numba
from numba.experimental import jitclass


class CourierState:
    courier_index = 0
    current_location = 0
    current_time = 0

    def __init__(self, courier_index, current_location, current_time):
        self.courier_index = courier_index
        self.current_location = current_location
        self.current_time = current_time


class CourierMove:
    courier_index = 0
    delivery_index = 0
    cost = 0
    move_appends = True
    def __init__(self, courier_index, delivery_index, cost, move_appends):
        self.courier_index = courier_index
        self.delivery_index = delivery_index
        self.cost = cost

def apply_courier_move(param: vrppd_parameters.Parameters, sol: vrppd_solution.Solution, courier_state: CourierState, courier_move: CourierMove):
    if courier_move.move_appends:
        delivery_dropoff_location = param.delivery_dropoff_location[courier_move.delivery_index - 1]
        delivery_delivery_time = append_delivery_delivery_time(param, sol, courier_state, courier_move.delivery_index)
        courier_state.current_location = delivery_dropoff_location
        courier_state.current_time = delivery_delivery_time
        sol.total_delivery_time += delivery_delivery_time
        sol.routing_plan[courier_move.courier_index - 1][2*sol.delivery_count_assigned_to_courier[courier_move.courier_index - 1]] = courier_move.delivery_index
        sol.routing_plan[courier_move.courier_index - 1][2*sol.delivery_count_assigned_to_courier[courier_move.courier_index - 1] + 1] = -courier_move.delivery_index
        sol.delivery_assigned_courier[courier_move.delivery_index - 1] = courier_move.courier_index
        sol.delivery_count_assigned_to_courier[courier_move.courier_index - 1] += 1
        sol.delivery_delivery_time[courier_move.delivery_index - 1] = delivery_delivery_time
    else:
        raise Exception('Not implemented')

def append_delivery_delivery_time(param: vrppd_parameters.Parameters, sol: vrppd_solution.Solution, courier_state: CourierState, delivery_index: int):
    delivery_pickup_location = param.delivery_pickup_location[delivery_index - 1]
    delivery_dropoff_location = param.delivery_dropoff_location[delivery_index - 1]
    delivery_time = (
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

def random_greedy_courier_heuristic(param: vrppd_parameters.Parameters, sol: vrppd_solution.Solution):
    sol.total_delivery_time = 0
    count_of_already_considered_closest_deliveries_from_location = np.zeros(param.location_count, dtype=int)
    
    # Only implement with append moves
    def greedy_delivery_of_courier(param: vrppd_parameters.Parameters, sol: vrppd_solution.Solution, courier_state: CourierState):
        current_location = courier_state.current_location
        for i in range(count_of_already_considered_closest_deliveries_from_location[current_location], param.delivery_count):
            closest_delivery = param.location_nearest_delivery_matrix[current_location][i]
            if sol.delivery_assigned_courier[closest_delivery - 1] == 0:
                delivery_time = append_delivery_delivery_time(param, sol, courier_state, closest_delivery)
                return CourierMove(courier_state.courier_index, closest_delivery, delivery_time, True)
            count_of_already_considered_closest_deliveries_from_location[current_location] += 1
        return CourierMove(courier_state.courier_index, 0, float('inf'), False)

    courier_states = [
            CourierState(
                courier_index, 
                param.courier_starting_location[courier_index - 1], 
                0
        ) for courier_index in range(1,param.courier_count+1)
    ]

    iteration = 0
    assigned_deliveries = 0
    prob = 0
    while assigned_deliveries < param.delivery_count:
        iteration += 1
        greedy_courier_moves = [greedy_delivery_of_courier(param, sol, courier_state) for courier_state in courier_states]
        greedy_courier_moves.sort(key = lambda x: x.cost)
        random_probability_vector = np.random.rand(param.courier_count)
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
