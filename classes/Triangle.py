from Segment import Segment
from Point import Point
import math


class Triangle:
    def __init__(self, point1, point2, point3):
        self._point1 = point1
        self._point2 = point2
        self._point3 = point3
        self._segment1 = Segment(point1, point2)
        self._segment2 = Segment(point2, point3)
        self._segment3 = Segment(point1, point3)
        self._fermat_point = None

    # covered with tests
    def _sign(self, p1, p2, p3):
        return (p1.get_x() - p3.get_x()) * (p2.get_y() - p3.get_y()) - (p2.get_x() - p3.get_x()) * (
                    p1.get_y() - p3.get_y())

    # covered with tests
    def is_point_inside(self, point):
        # Special case: all vertices are the same point
        if self._point1 == self._point2 and self._point2 == self._point3:
            return point == self._point1

        # Special case: triangle is a line (degenerate case)
        if self._segment1.is_collinear(self._segment2)\
                or self._segment2.is_collinear(self._segment3)\
                or self._segment3.is_collinear(self._segment1):
            return self._segment1.is_point_on_segment(point) or self._segment2.is_point_on_segment(
                point) or self._segment3.is_point_on_segment(point)

        # Barycentric coordinate system
        d1 = self._sign(point, self._point1, self._point2)
        d2 = self._sign(point, self._point2, self._point3)
        d3 = self._sign(point, self._point3, self._point1)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        # The point is on the inside if there are no signs differing (all non-negative or all non-positive)
        return not (has_neg and has_pos)

    # TODO: fix compute_fermat_point
    def compute_fermat_point(self):
        if self._fermat_point is not None:
            return self._fermat_point

        # Special case: Collinear or two vertices are the same
        if self._point1 == self._point2 or self._point1 == self._point3 or self._point2 == self._point3 or \
                self._segment1.is_collinear(self._segment2) or self._segment2.is_collinear(
            self._segment3) or self._segment1.is_collinear(self._segment3):
            # Find the vertex that lies between the other two vertices
            if self._segment1.is_point_on_segment(self._point3):
                self._fermat_point = self._point3
            elif self._segment2.is_point_on_segment(self._point1):
                self._fermat_point = self._point1
            else:
                self._fermat_point = self._point2
            return self._fermat_point
        # Check if any angle is 120 degrees or more
        if self._angle_is_large(self._point1, self._point2, self._point3) or \
                self._angle_is_large(self._point2, self._point3, self._point1) or \
                self._angle_is_large(self._point3, self._point1, self._point2):
            # The Fermat point is at the vertex with the large angle
            # Determine which vertex it is and set it as the Fermat point
            for p in [self._point1, self._point2, self._point3]:
                if self._angle_is_large(p,
                                        *[point for point in [self._point1, self._point2, self._point3] if point != p]):
                    self._fermat_point = p
                    return self._fermat_point

        # For triangles with all angles less than 120 degrees, construct equilateral triangles and find their intersections
        fp1 = self._construct_equilateral(self._point1, self._point2)
        fp2 = self._construct_equilateral(self._point2, self._point3)

        # Find intersection of lines (point1, fp1) and (point2, fp2)
        self._fermat_point = self._find_intersection(self._point1, fp1, self._point2, fp2)
        return self._fermat_point

    def _angle_is_large(self, p1, p2, p3):
        # Use the law of cosines to calculate the angle at p1 formed by p2 and p3
        a = math.dist([p2.get_x(), p2.get_y()], [p3.get_x(), p3.get_y()])
        b = math.dist([p1.get_x(), p1.get_y()], [p3.get_x(), p3.get_y()])
        c = math.dist([p1.get_x(), p1.get_y()], [p2.get_x(), p2.get_y()])
        # Ensure the value inside acos is within the range [-1, 1]
        cos_angle = max(min((b ** 2 + c ** 2 - a ** 2) / (2 * b * c), 1), -1)
        angle = math.acos(cos_angle)
        return angle >= (2 * math.pi / 3)  # Check if the angle is 120 degrees or more in radians

    def _construct_equilateral(self, p1, p2):
        # Construct an equilateral triangle on the side formed by p1 and p2
        angle = math.pi / 3  # 60 degrees in radians
        dx = p2.get_x() - p1.get_x()
        dy = p2.get_y() - p1.get_y()
        # Calculate the length of the side and the new direction
        length = math.sqrt(dx ** 2 + dy ** 2)
        new_dx = math.cos(angle) * dx - math.sin(angle) * dy
        new_dy = math.sin(angle) * dx + math.cos(angle) * dy
        # Return the third vertex of the equilateral triangle
        return Point(p1.get_x() + new_dx / length * math.sqrt(3) * length / 2,
                     p1.get_y() + new_dy / length * math.sqrt(3) * length / 2)

    def _find_intersection(self, p1, q1, p2, q2):
        # Calculate the intersection point of lines p1q1 and p2q2
        det = (q1.get_x() - p1.get_x()) * (q2.get_y() - p2.get_y()) - (q1.get_y() - p1.get_y()) * (
                    q2.get_x() - p2.get_x())
        if det == 0:
            return None  # Lines are parallel, no intersection
        lambda_ = ((q2.get_y() - p2.get_y()) * (q2.get_x() - p1.get_x()) + (p2.get_x() - q2.get_x()) * (
                    q2.get_y() - p1.get_y())) / det
        x = p1.get_x() + lambda_ * (q1.get_x() - p1.get_x())
        y = p1.get_y() + lambda_ * (q1.get_y() - p1.get_y())
        return Point(x, y)

    '''
    Tries to position drones from all 3 ends through Fermat-Torricelli point. Chooses positioning that uses less drones
    or, in case of equality, covers more power stations
    Returns drone positions and number of covered Power Stations
    '''
    # def position_drones(self, power_stations, radiusDroneBS, obstacles):
    # TODO: Implement