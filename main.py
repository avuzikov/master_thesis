from thesisCode.algorithms.build_spanning_tree import build_spanning_tree
from thesisCode.algorithms.connect_using_pso import connect_using_pso
from thesisCode.algorithms.obstacle_avoidance_pso import generate_drone_positions_through_point
from thesisCode.algorithms.update_using_fermat_points import find_triples, find_best_triangles, opt_drone_deployment
from thesisCode.data.parse_data_from_json import parse_data
from thesisCode.classes.Segment import Segment
from thesisCode.classes.Point import Point
from thesisCode.classes.Obstacles import Obstacles
from thesisCode.classes.Triangle import Triangle
from thesisCode.data.save_drones_to_json import save_drones_to_json

dataset_num = '0'
# Load test data from JSON
graph_builder = parse_data('./thesisCode/data/real_test_data_obstacles' + dataset_num + '.json')

mst_edges, parent = build_spanning_tree(graph_builder)

triples = find_triples(mst_edges)

sorted_gain_array = find_best_triangles(mst_edges, graph_builder)

# drone positions after implementing Lovesh algorithm
initial_drone_positions = opt_drone_deployment(sorted_gain_array, mst_edges)

graph_builder.addDrones(initial_drone_positions)

if len(graph_builder.getComponents()) > 1:
    print("Connecting with the help of PSO...")
    pso_drones = connect_using_pso(graph_builder)

save_drones_to_json('./thesisCode/data/results/drone_positions_obstacles' + dataset_num + '.json',
                    initial_drone_positions + pso_drones)
