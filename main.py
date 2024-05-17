from thesisCode.algorithms.build_spanning_tree import build_spanning_tree
from thesisCode.algorithms.obstacle_avoidance import avoid_obstacles, generate_drone_positions_through_point
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

drone_positions = opt_drone_deployment(sorted_gain_array, mst_edges)

# print(len(drone_positions))
# print(drone_positions)

segment = Segment(Point(0, 0), Point(10, 0))
power_stations = [Point(5, 2), Point(7, -1)]
radius_drone_bs = 5
obstacles = Obstacles()
obstacles.add_triangle(Triangle(Point(4, 1), Point(6, 1), Point(5, 3)))

best_point = avoid_obstacles(segment, power_stations, radius_drone_bs, obstacles)

print(obstacles.is_segment_clear(Segment(segment._point1, best_point)), obstacles.is_segment_clear(Segment(segment._point2, best_point)))

print(best_point)

drone_positions = generate_drone_positions_through_point(segment, best_point, radius_drone_bs, obstacles)
print("Drone positions (including best_point):")
for drone in drone_positions:
    print(drone)
