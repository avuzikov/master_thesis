from thesisCode.classes.Segment import Segment


class Obstacles:
    # covered with tests
    def __init__(self):
        self.triangles = []

    # covered with tests
    def add_triangle(self, triangle):
        self.triangles.append(triangle)

    # covered with tests
    def is_point_inside_any_obstacle(self, point):
        for triangle in self.triangles:
            if triangle.is_point_inside(point):
                return True  # The point is inside at least one triangle
        return False  # The point is not inside any triangle

    # covered with tests
    def __str__(self):
        return '\n'.join(str(triangle) for triangle in self.triangles)

    # covered with tests
    # checks if ends of segment have LOS connection
    def is_segment_clear(self, segment):
        for triangle in self.triangles:
            # Check if any endpoint of the segment is inside a triangle
            if triangle.is_point_inside(segment._point1) or triangle.is_point_inside(segment._point2):
                return False

            # Check for intersection between the segment and each side of the triangle
            for tri_segment in [Segment(triangle._point1, triangle._point2),
                                Segment(triangle._point2, triangle._point3),
                                Segment(triangle._point3, triangle._point1)]:
                if segment.get_intersection_point(tri_segment) is not None:
                    return False  # The segment intersects with a triangle side

        return True  # The segment is clear of all obstacles