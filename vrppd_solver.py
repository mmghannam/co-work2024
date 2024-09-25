from vrppd_parameters import Parameters
from vrppd_solution import Solution
import time
from heuristic_generator import random_greedy_courier_heuristic

def optimize(param: Parameters, solver_settings: dict) -> Solution:
    best_sol = random_greedy_courier_heuristic(param, Solution(param))
    starting_time = time.time()
    incumbent_sol = Solution(param)
    while time.time() - starting_time < solver_settings['time_limit']:
        incumbent_sol = Solution(param)
        random_greedy_courier_heuristic(param, incumbent_sol)
        if incumbent_sol.total_delivery_time < best_sol.total_delivery_time:
            best_sol = incumbent_sol
    return best_sol