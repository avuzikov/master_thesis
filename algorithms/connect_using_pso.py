from thesisCode.algorithms.obstacle_avoidance_pso import avoid_obstacles_pso, generate_drone_positions_through_point
from thesisCode.classes.Segment import Segment


def connect_using_pso(graph_builder, limit=-1):
    # Check if there is only one connectivity component
    if len(graph_builder._components) <= 1:
        return []

    # Find all pairs of base stations from different components and sort them by distance
    def generate_pairs(components):
        pairs = []
        for i, component1 in enumerate(components):
            for j, component2 in enumerate(components):
                if i >= j:
                    continue
                for bs1 in component1.getBSs():
                    for bs2 in component2.getBSs():
                        distance = bs1.distance_to(bs2)
                        pairs.append((distance, bs1, bs2))
        pairs.sort(key=lambda x: x[0])
        return pairs

    pairs = generate_pairs(graph_builder._components)
    answer = []
    initial_limit = limit

    while pairs:
        distance, bs1, bs2 = pairs.pop(0)
        if limit == 0:
            break

        # Try to find a connecting point using avoid_obstacles_pso
        best_point = avoid_obstacles_pso(Segment(bs1, bs2), graph_builder.getPowerStations(),
                                         graph_builder.getRadiusBS(), graph_builder.getObstacles())
        if best_point:
            # Generate drone positions through the best point
            drone_positions = generate_drone_positions_through_point(Segment(bs1, bs2), best_point,
                                                                     graph_builder.getRadiusBS(),
                                                                     graph_builder.getObstacles())
            if drone_positions:
                # Add drones to the answer and update the graph
                answer.extend(drone_positions)
                graph_builder.addDrones(drone_positions)

                # Update components and regenerate pairs
                pairs = generate_pairs(graph_builder._components)
                limit = initial_limit  # Reset limit after a successful connection
            else:
                limit -= 1
        else:
            limit -= 1

    print('PSO drones: ', answer)
    return answer