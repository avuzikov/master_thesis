from thesisCode.classes.Segment import Segment
from thesisCode.classes.Point import Point
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
    def __str__(self):
        return f'Triangle({self._point1}, {self._point2}, {self._point3})'

    # covered with tests
    __repr__ = __str__

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

    # covered with tests
    def _is_triangle_degenerate(self):
        # Check if any vertices are the same
        if self._point1 == self._point2 or self._point2 == self._point3 or self._point1 == self._point3:
            return True

        # Check if any edges are parallel by calculating the cross product of vectors
        vector_a = (self._point2.get_x() - self._point1.get_x(), self._point2.get_y() - self._point1.get_y())
        vector_b = (self._point3.get_x() - self._point2.get_x(), self._point3.get_y() - self._point2.get_y())
        vector_c = (self._point1.get_x() - self._point3.get_x(), self._point1.get_y() - self._point3.get_y())

        cross_ab = vector_a[0] * vector_b[1] - vector_a[1] * vector_b[0]
        cross_bc = vector_b[0] * vector_c[1] - vector_b[1] * vector_c[0]
        cross_ca = vector_c[0] * vector_a[1] - vector_c[1] * vector_a[0]

        # If the cross product of any two edges is zero, the edges are parallel
        if cross_ab == 0 or cross_bc == 0 or cross_ca == 0:
            return True

        return False

    # covered with tests
    def _angle_is_large(self):
        if self._is_triangle_degenerate():
            return None

        # Calculate the lengths of the sides
        a = self._point2.distance_to(self._point3)
        b = self._point1.distance_to(self._point3)
        c = self._point1.distance_to(self._point2)

        # Check each angle using the law of cosines
        cos_angle_A = (b ** 2 + c ** 2 - a ** 2) / (2 * b * c)
        cos_angle_B = (a ** 2 + c ** 2 - b ** 2) / (2 * a * c)
        cos_angle_C = (a ** 2 + b ** 2 - c ** 2) / (2 * a * b)

        if cos_angle_A < -0.5:
            return self._point1
        if cos_angle_B < -0.5:
            return self._point2
        if cos_angle_C < -0.5:
            return self._point3

        return None

    # covered with tests
    def compute_fermat_point(self):
        # Step 1: Check for degenerate triangle
        if self._is_triangle_degenerate():
            return None

        # Step 2: Check for angles >= 120 degrees
        large_angle_vertex = self._angle_is_large()
        if large_angle_vertex is not None:
            return large_angle_vertex

        # Helper function to find the point farthest from a given point among two options
        def _farthest_point(point, option1, option2):
            distance1 = point.distance_to(option1)
            distance2 = point.distance_to(option2)
            return option1 if distance1 > distance2 else option2

        # Step 3: Compute equilateral points and find Segment s3
        equilateral_3_1, equilateral_3_2 = Segment(self._point1, self._point2).compute_equilateral()
        farthest_point_3 = _farthest_point(self._point3, equilateral_3_1, equilateral_3_2)
        s3 = Segment(farthest_point_3, self._point3)

        # Repeat step 3 for another triangle edge and find Segment s
        equilateral_1_1, equilateral_1_2 = Segment(self._point2, self._point3).compute_equilateral()
        farthest_point_1 = _farthest_point(self._point1, equilateral_1_1, equilateral_1_2)
        s1 = Segment(farthest_point_1, self._point1)

        # Step 5: Return the intersection of s and s3
        return s1.get_intersection_point(s3)

    # NOT covered with tests
    def position_drones_fermat(self, power_stations, radius_drone_bs, obstacles):
        fermat_point = self.compute_fermat_point()

        if fermat_point is None:
            return None, None

        large_angle_vertex = self._angle_is_large()
        if large_angle_vertex:
            return None, None

        # Handle the case with the Fermat point
        segments_to_fermat = [Segment(vertex, fermat_point) for vertex in [self._point1, self._point2, self._point3]]
        clear_segments = [seg for seg in segments_to_fermat if obstacles.is_segment_clear(seg)]

        if len(clear_segments) != 3:
            return None, None

        drones = [fermat_point]
        covered_stations = set()
        for seg in clear_segments:
            seg_drones, seg_covered = seg.position_drones(power_stations, radius_drone_bs, obstacles)
            if seg_drones is not None:
                drones += seg_drones
                covered_stations.update(seg_covered)

        return drones, covered_stations
