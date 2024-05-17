import math
import random
from thesisCode.classes.Segment import Segment
from thesisCode.classes.Point import Point


def avoid_obstacles_pso(segment, power_stations, radius_drone_bs, obstacles, margin=1.0, num_particles=30,
                    max_iterations=200):
    def objective_function(P):
        seg1 = Segment(segment._point1, P)
        seg2 = Segment(segment._point2, P)
        if not (obstacles.is_segment_clear(seg1) and obstacles.is_segment_clear(seg2)):
            return float('inf'), 0, float('inf')

        drones_seg1, covered1 = seg1.position_drones_evenly(power_stations, radius_drone_bs, obstacles)
        drones_seg2, covered2 = seg2.position_drones_evenly(power_stations, radius_drone_bs, obstacles)
        if drones_seg1 is None or drones_seg2 is None:
            return float('inf'), 0, float('inf')

        total_drones = len(drones_seg1) + len(drones_seg2) + 1
        total_coverage = len(covered1.union(covered2))
        total_length = seg1._point1.distance_to(seg1._point2) + seg2._point1.distance_to(seg2._point2)

        return total_drones, total_coverage, total_length

    def generate_random_point():
        while True:
            theta = random.uniform(0, 2 * math.pi)
            r = random.uniform(0, max_distance_to_centers / 2)
            x = center_x + r * math.cos(theta)
            y = center_y + r * math.sin(theta)
            P = Point(x, y)
            if is_point_within_ellipse(P):
                return P

    def is_point_within_ellipse(P):
        dist1 = segment._point1.distance_to(P)
        dist2 = segment._point2.distance_to(P)
        return math.isclose(dist1 + dist2, max_distance_to_centers, rel_tol=1e-5)

    def update_velocity(particle, best_position, global_best_position):
        inertia = 0.5
        r1 = random.random()
        r2 = random.random()
        cognitive_component = (best_position - particle['position']) * (1.5 * r1)
        social_component = (global_best_position - particle['position']) * (1.5 * r2)
        particle['velocity'] = (particle['velocity'] * inertia) + cognitive_component + social_component

    def update_position(particle):
        new_position = particle['position'] + particle['velocity']
        if is_point_within_ellipse(new_position):
            particle['position'] = new_position

    center_x = (segment._point1.get_x() + segment._point2.get_x()) / 2
    center_y = (segment._point1.get_y() + segment._point2.get_y()) / 2
    distance_between_centers = segment._point1.distance_to(segment._point2)
    max_distance_to_centers = distance_between_centers * (1 + margin)

    particles = [
        {'position': generate_random_point(), 'velocity': Point(random.uniform(-1, 1), random.uniform(-1, 1)),
         'best_position': None, 'best_cost': (float('inf'), 0, float('inf'))}
        for _ in range(num_particles)
    ]
    global_best_position = None
    global_best_cost = (float('inf'), 0, float('inf'))

    for particle in particles:
        cost = objective_function(particle['position'])
        particle['best_position'] = particle['position']
        particle['best_cost'] = cost
        if cost < global_best_cost:
            global_best_position = particle['position']
            global_best_cost = cost

    for _ in range(max_iterations):
        for particle in particles:
            update_velocity(particle, particle['best_position'], global_best_position)
            update_position(particle)

            cost = objective_function(particle['position'])
            if cost < particle['best_cost']:
                particle['best_position'] = particle['position']
                particle['best_cost'] = cost

            if cost < global_best_cost:
                global_best_position = particle['position']
                global_best_cost = cost

    if global_best_position is None or global_best_cost[0] == float('inf'):
        return None
    return global_best_position


def generate_drone_positions_through_point(segment, best_point, radius_drone_bs, obstacles):
    segment1 = Segment(segment._point1, best_point)
    segment2 = Segment(segment._point2, best_point)

    drones_seg1, _ = segment1.position_drones_evenly([], radius_drone_bs, obstacles)
    drones_seg2, _ = segment2.position_drones_evenly([], radius_drone_bs, obstacles)

    all_drones = drones_seg1 + [best_point] + drones_seg2

    unique_drones = []
    seen = set()
    for drone in all_drones:
        if (drone.get_x(), drone.get_y()) not in seen:
            seen.add((drone.get_x(), drone.get_y()))
            unique_drones.append(drone)

    return unique_drones
