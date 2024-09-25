import csv

def write_solution_to_csv(solution, output_file):
     with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
         # Write header for routing plan
        writer.writerow(['Courier', 'Routing Plan'])
        # Write the routing plan for each courier
        for courier_idx in range(solution.routing_plan.shape[0]):
            writer.writerow([f'Courier {courier_idx}', solution.routing_plan[courier_idx].tolist()])

        # Write header for delivery times
        writer.writerow([])
        writer.writerow(['Delivery', 'Assigned Courier', 'Delivery Time'])
        # Write the delivery times and assigned couriers
        for delivery_idx in range(len(solution.delivery_delivery_time)):
            writer.writerow([delivery_idx, solution.delivery_assigned_courier[delivery_idx], solution.delivery_delivery_time[delivery_idx]])

        # Write header for delivery count assigned to couriers
        writer.writerow([])
        writer.writerow(['Courier', 'Number of Deliveries'])
        # Write the number of deliveries assigned to each courier
        for courier_idx in range(len(solution.delivery_count_assigned_to_courier)):
            writer.writerow([f'Courier {courier_idx}', solution.delivery_count_assigned_to_courier[courier_idx]])
