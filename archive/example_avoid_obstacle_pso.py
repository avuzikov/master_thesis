'''
segment = Segment(Point(0, 0), Point(10, 0))
power_stations = [Point(5, 2), Point(7, -1)]
radius_drone_bs = 5
obstacles = Obstacles()
obstacles.add_triangle(Triangle(Point(4, 1), Point(6, 1), Point(5, 3)))

best_point = avoid_obstacles_pso(segment, power_stations, radius_drone_bs, obstacles)

print(obstacles.is_segment_clear(Segment(segment._point1, best_point)), obstacles.is_segment_clear(Segment(segment._point2, best_point)))

print(best_point)

drone_positions = generate_drone_positions_through_point(segment, best_point, radius_drone_bs, obstacles)
print("Drone positions (including best_point):")
for drone in drone_positions:
    print(drone)
'''

