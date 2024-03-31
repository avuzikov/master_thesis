import unittest
from Point import Point
from Segment import Segment
from Triangle import Triangle
from Obstacles import Obstacles

class TestTriangle(unittest.TestCase):

    '''is_point_inside'''

    def test_triangle_degenerate_all_vertices_one_point(self):
        """Test a degenerate triangle where all vertices are at the same point."""
        degenerate_triangle = Triangle(Point(1, 1), Point(1, 1), Point(1, 1))
        inside_point = Point(1, 1)
        outside_point = Point(2, 2)

        self.assertTrue(degenerate_triangle.is_point_inside(inside_point),
                        "The point coinciding with the degenerate triangle should be considered inside.")
        self.assertFalse(degenerate_triangle.is_point_inside(outside_point),
                         "Any point other than the degenerate point should be considered outside.")

    def test_triangle_degenerate_two_vertices_one_point_1_2(self):
        """Test a degenerate triangle where the first two vertices are at the same point."""
        degenerate_triangle = Triangle(Point(1, 1), Point(1, 1), Point(3, 3))
        inside_point = Point(1, 1)  # Coincides with the degenerate line
        outside_point = Point(0, 0)  # Outside the line

        self.assertTrue(degenerate_triangle.is_point_inside(inside_point),
                        "Points on the degenerate line segment should be considered inside.")
        self.assertFalse(degenerate_triangle.is_point_inside(outside_point),
                         "Points not on the degenerate line segment should be considered outside.")

    def test_triangle_degenerate_two_vertices_one_point_1_3(self):
        """Test a degenerate triangle where the first and third vertices are at the same point."""
        degenerate_triangle = Triangle(Point(1, 1), Point(3, 3), Point(1, 1))
        inside_point = Point(1, 1)  # Coincides with the degenerate line
        outside_point = Point(2, 4)  # Outside the line

        self.assertTrue(degenerate_triangle.is_point_inside(inside_point),
                        "Points on the degenerate line segment should be considered inside.")
        self.assertFalse(degenerate_triangle.is_point_inside(outside_point),
                         "Points not on the degenerate line segment should be considered outside.")

    def test_triangle_degenerate_two_vertices_one_point_2_3(self):
        """Test a degenerate triangle where the second and third vertices are at the same point."""
        degenerate_triangle = Triangle(Point(3, 3), Point(1, 1), Point(1, 1))
        inside_point = Point(1, 1)  # Coincides with the degenerate line
        outside_point = Point(4, 2)  # Outside the line

        self.assertTrue(degenerate_triangle.is_point_inside(inside_point),
                        "Points on the degenerate line segment should be considered inside.")
        self.assertFalse(degenerate_triangle.is_point_inside(outside_point),
                         "Points not on the degenerate line segment should be considered outside.")

    def test_normal_triangle(self):
        """Test a normal, non-degenerate triangle."""
        triangle = Triangle(Point(0, 0), Point(5, 0), Point(2.5, 5))
        inside_point = Point(2.5, 2)  # Inside the triangle
        outside_point = Point(0, 5)  # Outside the triangle

        self.assertTrue(triangle.is_point_inside(inside_point),
                        "Points inside the triangle should be considered inside.")
        self.assertFalse(triangle.is_point_inside(outside_point),
                         "Points outside the triangle should be considered outside.")

    def test_point_on_triangle_segment(self):
        """Test that a point lying on one of the triangle's segments is considered inside."""
        triangle = Triangle(Point(0, 0), Point(5, 0), Point(2.5, 5))
        point_on_segment = Point(2.5, 0)  # Lies on the segment between Point(0, 0) and Point(5, 0)

        self.assertTrue(triangle.is_point_inside(point_on_segment),
                        "A point on one of the triangle's segments should be considered inside.")

    def test_point_on_triangle_vertex(self):
        """Test that a point coinciding with one of the triangle's vertices is considered inside."""
        triangle = Triangle(Point(0, 0), Point(5, 0), Point(2.5, 5))
        point_on_vertex = Point(0, 0)  # Coincides with one of the triangle's vertices

        self.assertTrue(triangle.is_point_inside(point_on_vertex),
                        "A point coinciding with a triangle's vertex should be considered inside.")

    '''compute_fermat_point'''

if __name__ == '__main__':
    unittest.main()