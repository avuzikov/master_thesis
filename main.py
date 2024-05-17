from thesisCode.algorithms.build_spanning_tree import build_spanning_tree
from thesisCode.algorithms.connect_using_pso import connect_using_pso
from thesisCode.algorithms.obstacle_avoidance_pso import avoid_obstacles, generate_drone_positions_through_point
from thesisCode.algorithms.update_using_fermat_points import find_triples, find_best_triangles, opt_drone_deployment
from thesisCode.data.parse_data import parse_data
from thesisCode.classes.Segment import Segment
from thesisCode.classes.Point import Point
from thesisCode.classes.Obstacles import Obstacles
from thesisCode.classes.Triangle import Triangle

# Load test data from JSON
graph_builder = parse_data('./thesisCode/data/test_data4.json')

mst_edges, parent = build_spanning_tree(graph_builder)

triples = find_triples(mst_edges)

sorted_gain_array = find_best_triangles(mst_edges, graph_builder)

# drone positions after implementing Lovesh algorithm
initial_drone_positions = opt_drone_deployment(sorted_gain_array, mst_edges)

graph_builder.addDrones(initial_drone_positions)

if len(graph_builder.getComponents()) > 1:
    connect_using_pso(graph_builder)

# print(len(drone_positions))
# print(drone_positions)
