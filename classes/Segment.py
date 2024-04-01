import math
from Point import Point


class Segment:
    # covered with tests
    def __init__(self, point1, point2):
        self._point1 = point1
        self._point2 = point2

    # covered with tests
    def __str__(self):
        return f'Segment({self._point1}, {self._point2})'

    # covered with tests
    def _calculate_slope(self, p1, p2):
        if math.isclose(p1.get_x(), p2.get_x()):
            return float('inf')  # Vertical line
        return (p2.get_y() - p1.get_y()) / (p2.get_x() - p1.get_x())

    # covered with tests
    # line equations: y = slope * x + intercept OR x = intercept
    def _calculate_intercept(self, p, slope):
        if math.isinf(slope):  # Vertical line
            return p.get_x()
        return p.get_y() - slope * p.get_x()

    # covered with tests
    def is_parallel(self, other_segment):
        slope1 = self._calculate_slope(self._point1, self._point2)
        slope2 = self._calculate_slope(other_segment._point1, other_segment._point2)
        return math.isclose(slope1, slope2)

    # covered with tests
    def is_collinear(self, other_segment):
        if not self.is_parallel(other_segment):
            return False

        slope = self._calculate_slope(self._point1, self._point2)
        intercept1 = self._calculate_intercept(self._point1, slope)
        intercept2 = self._calculate_intercept(other_segment._point1, slope)
        return math.isclose(intercept1, intercept2)

    # covered with tests
    def is_point_on_segment(self, point):
        # Check if the point is within the x and y bounds of the segment
        x_min, x_max = sorted([self._point1.get_x(), self._point2.get_x()])
        y_min, y_max = sorted([self._point1.get_y(), self._point2.get_y()])
        within_x = x_min <= point.get_x() <= x_max
        within_y = y_min <= point.get_y() <= y_max

        # For vertical line, just check y bounds
        if math.isclose(self._point1.get_x(), self._point2.get_x()):
            return within_y

        # Calculate slope and intercept, then check if point satisfies line equation
        slope = self._calculate_slope(self._point1, self._point2)
        intercept = self._calculate_intercept(self._point1, slope)
        return within_x and within_y and math.isclose(point.get_y(), slope * point.get_x() + intercept)

    # covered with tests
    def get_intersection_point(self, other_segment):
        x1, y1 = self._point1.get_x(), self._point1.get_y()
        x2, y2 = self._point2.get_x(), self._point2.get_y()
        x3, y3 = other_segment._point1.get_x(), other_segment._point1.get_y()
        x4, y4 = other_segment._point2.get_x(), other_segment._point2.get_y()

        # For collinear case it is enough to check 3 points
        if self.is_collinear(other_segment):
            if self.is_point_on_segment(other_segment._point1):
                return other_segment._point1
            if self.is_point_on_segment(other_segment._point2):
                return other_segment._point2
            if other_segment.is_point_on_segment(self._point1):
                return self._point1
            return None

        # Calculate intersection point using line equations
        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denominator == 0:  # Lines are parallel
            return None

        px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denominator
        py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denominator

        # Check if intersection point lies within both segments
        if (min(x1, x2) <= px <= max(x1, x2) and
                min(y1, y2) <= py <= max(y1, y2) and
                min(x3, x4) <= px <= max(x3, x4) and
                min(y3, y4) <= py <= max(y3, y4)):
            return Point(px, py)

        return None

    # covered with tests
    def compute_equilateral(self):

        if self._point1 == self._point2:
            return None

        p1, p2 = self._point1, self._point2

        # Calculate the midpoint of the opposite segment
        mid_x = (p1.get_x() + p2.get_x()) / 2
        mid_y = (p1.get_y() + p2.get_y()) / 2

        # Calculate the length of the segment to find the height of the equilateral triangle
        segment_length = math.sqrt((p1.get_x() - p2.get_x()) ** 2 + (p1.get_y() - p2.get_y()) ** 2)
        height = math.sqrt(3) / 2 * segment_length

        # Handle horizontal, vertical, and oblique segments
        if p1.get_y() == p2.get_y():  # Horizontal segment
            perp1 = Point(mid_x, mid_y + height)
            perp2 = Point(mid_x, mid_y - height)
        elif p1.get_x() == p2.get_x():  # Vertical segment
            perp1 = Point(mid_x + height, mid_y)
            perp2 = Point(mid_x - height, mid_y)
        else:  # Oblique segment
            slope = (p2.get_y() - p1.get_y()) / (p2.get_x() - p1.get_x())
            perp_slope = -1 / slope
            dx = height / math.sqrt(1 + perp_slope ** 2)
            dy = perp_slope * dx

            # Adjust dx and dy based on the direction of the segment to ensure correct placement
            if p2.get_x() > p1.get_x():
                perp1 = Point(mid_x + dx, mid_y + dy)
                perp2 = Point(mid_x - dx, mid_y - dy)
            else:
                perp1 = Point(mid_x - dx, mid_y - dy)
                perp2 = Point(mid_x + dx, mid_y + dy)

        return perp1, perp2

    '''
    Tries to position drones from both ends. Chooses positioning that covers more power stations
    Returns drone positions and number of covered Power Stations
    '''

    # covered with tests
    def position_drones(self, power_stations, radius_drone_bs, obstacles):
        # Check if the segment is obstructed by any obstacle
        if not obstacles.is_segment_clear(Segment(self._point1, self._point2)):
            return None, set()

        # Calculate drone positions and covered stations starting from _point1
        drones_from_p1, covered_from_p1 = self._calculate_drone_positions(self._point1, self._point2, power_stations,
                                                                          radius_drone_bs, obstacles)

        # Calculate drone positions and covered stations starting from _point2
        drones_from_p2, covered_from_p2 = self._calculate_drone_positions(self._point2, self._point1, power_stations,
                                                                          radius_drone_bs, obstacles)

        # Determine which set of drone positions covers more power stations
        if covered_from_p1 >= covered_from_p2:
            return drones_from_p1, covered_from_p1
        else:
            return drones_from_p2, covered_from_p2

    def _calculate_drone_positions(self, start_point, end_point, power_stations, radius_drone_bs, obstacles):
        drones = []
        covered_power_stations = set()

        # Calculate direction vector from start to end point
        dx = end_point.get_x() - start_point.get_x()
        dy = end_point.get_y() - start_point.get_y()
        segment_length = math.sqrt(dx ** 2 + dy ** 2)
        direction = (dx / segment_length, dy / segment_length)

        # Position drones and count covered power stations
        distance = radius_drone_bs
        while distance < segment_length:
            # Calculate drone's position
            drone_x = start_point.get_x() + distance * direction[0]
            drone_y = start_point.get_y() + distance * direction[1]
            drone_position = Point(drone_x, drone_y)
            drones.append(drone_position)

            # Check each power station for coverage, considering obstacles
            for station in power_stations:
                station_segment = Segment(drone_position, station)
                if drone_position.distance_to(station) <= radius_drone_bs and obstacles.is_segment_clear(station_segment):
                    covered_power_stations.add(station)

            distance += radius_drone_bs

        return drones, covered_power_stations
