from vrppd_parameters import Parameters
from vrppd_solution import Solution

def route_list(param: Parameters, sol: Solution):
    """
    This function creates a list of routes for each vehicle.
    Parameters:
        param: Parameters
            The parameters of the problem.
        sol: Solution
            The solution of the problem.
    Returns:
        list
            A list of routes for each vehicle.
    """
    routes = []
    for v in range(len(sol.routing_plan)):
        route = [param.courier_starting_location[v]]
        for i in range(len(sol.routing_plan[v])):
            if sol.routing_plan[v][i] == 0:
                break
            elif sol.routing_plan[v][i] > 0:
                route.append(
                    param.delivery_pickup_location[sol.routing_plan[v][i] - 1]
                )
            else:
                route.append(
                    param.delivery_dropoff_location[-sol.routing_plan[v][i] - 1]
                )
        routes.append(route)
    return routes
