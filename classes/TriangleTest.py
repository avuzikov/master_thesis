import unittest
from Point import Point
from Segment import Segment
from Triangle import Triangle
from Obstacles import Obstacles
import math

class TestTriangle(unittest.TestCase):

    def setUp(self):
        self.epsilon = 1e-6  # Tolerance for floating point comparison
    '''is_point_inside'''

    def assertPointAlmostEqual(self, point1, point2):
        self.assertAlmostEqual(point1.get_x(), point2.get_x(), delta=self.epsilon)
        self.assertAlmostEqual(point1.get_y(), point2.get_y(), delta=self.epsilon)

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

    '''_is_triangle_degenerate'''
    def test_non_degenerate_triangle(self):
        triangle = Triangle(Point(0, 0), Point(1, 1), Point(1, 0))
        self.assertFalse(triangle._is_triangle_degenerate(), "The triangle should not be degenerate.")

    def test_triangle_with_repeated_vertices(self):
        triangle = Triangle(Point(0, 0), Point(0, 0), Point(1, 1))
        self.assertTrue(triangle._is_triangle_degenerate(),
                        "The triangle should be degenerate due to repeated vertices.")

    def test_triangle_with_same_vertex(self):
        triangle = Triangle(Point(0, 0), Point(0, 0), Point(0, 0))
        self.assertTrue(triangle._is_triangle_degenerate(),
                        "The triangle should be degenerate due to being a point.")

    def test_collinear_vertices(self):
        # Points (0,0), (2,2), and (4,4) are collinear
        triangle = Triangle(Point(0, 0), Point(2, 2), Point(4, 4))
        self.assertTrue(triangle._is_triangle_degenerate(),
                        "The triangle should be degenerate due to collinear vertices.")

    '''_angle_is_large'''
    def test_angle_greater_than_120(self):
        # Triangle with one angle greater than 120 degrees
        triangle = Triangle(Point(0, 0), Point(20, 0), Point(2, 1))
        large_angle_vertex = triangle._angle_is_large()
        self.assertIsNotNone(large_angle_vertex, "Expected a vertex with a large angle.")
        self.assertTrue(large_angle_vertex in [triangle._point1, triangle._point2, triangle._point3],
                        "The vertex should be one of the triangle's vertices.")

        self.assertPointAlmostEqual(large_angle_vertex, Point(2, 1))

    def test_all_angles_less_than_120(self):
        # Acute triangle where all angles are less than 90 degrees
        triangle = Triangle(Point(0, 0), Point(4, 0), Point(2, 3))
        large_angle_vertex = triangle._angle_is_large()
        self.assertIsNone(large_angle_vertex, "Expected no vertex since all angles are less than 120 degrees.")

    def test_degenerate_triangle_repeated_vertices(self):
        # Degenerate triangle with repeated vertices
        triangle = Triangle(Point(0, 0), Point(0, 0), Point(2, 2))
        large_angle_vertex = triangle._angle_is_large()
        self.assertIsNone(large_angle_vertex, "Expected None for a degenerate triangle with repeated vertices.")

    def test_degenerate_triangle_collinear_vertices(self):
        # Degenerate triangle with collinear vertices
        triangle = Triangle(Point(0, 0), Point(2, 2), Point(4, 4))
        large_angle_vertex = triangle._angle_is_large()
        self.assertIsNone(large_angle_vertex, "Expected None for a degenerate triangle with collinear vertices.")

    '''compute_fermat_point'''
    def test_degenerate_triangle(self):
        # Degenerate triangle with repeated vertices
        triangle = Triangle(Point(0, 0), Point(0, 0), Point(1, 1))
        fermat_point = triangle.compute_fermat_point()
        self.assertIsNone(fermat_point, "Expected None for a degenerate triangle.")

    def test_triangle_with_large_angle(self):
        # Triangle with one angle >= 120 degrees
        triangle = Triangle(Point(0, 0), Point(40, 0), Point(2, 1))
        fermat_point = triangle.compute_fermat_point()
        self.assertTrue(fermat_point in [Point(0, 0), Point(40, 0), Point(2, 1)],
                        "The Fermat point should be a triangle vertex with a large angle.")

    def test_acute_triangle(self):
        # Acute triangle (all angles < 120 degrees)
        triangle = Triangle(Point(0, 0), Point(4, 0), Point(2, 3))
        # Known Fermat point for this triangle setup, if applicable
        known_fermat_point = Point(2, 1.1547005)
        fermat_point = triangle.compute_fermat_point()
        self.assertPointAlmostEqual(fermat_point, known_fermat_point)

    '''position_drones_triangle'''
    def test_degenerate_triangle(self):
        # Degenerate triangle: all points on a line
        triangle = Triangle(Point(0, 0), Point(5, 5), Point(10, 10))
        power_stations = [Point(2, 2), Point(8, 8)]
        radius_drone_bs = 3
        obstacles = Obstacles()  # Assume no obstacles for simplicity

        drones, covered_stations = triangle.position_drones_triangle(power_stations, radius_drone_bs, obstacles)
        self.assertEqual(len(drones), 4, "There should be exactly 4 drones.")
        self.assertTrue(len(covered_stations) == len(power_stations))

    def test_degenerate_triangle_obstacle(self):
        # Degenerate triangle: all points on a line
        triangle = Triangle(Point(0, 0), Point(5, 5), Point(10, 10))
        power_stations = [Point(2, 2), Point(8, 8)]
        radius_drone_bs = 3
        obstacles = Obstacles()  # Assume no obstacles for simplicity
        obstacles.add_triangle(Triangle(Point(2, 3), Point(3, 2), Point(4, 4)))
        drones, covered_stations = triangle.position_drones_triangle(power_stations, radius_drone_bs, obstacles)
        self.assertIsNone(drones, "drones value is None")
        self.assertIsNone(covered_stations, "covered_stations is None")

    def test_large_angle_all_edges_clear(self):
        # Triangle with a large angle and all edges clear
        triangle = Triangle(Point(0, 0), Point(10, 2), Point(20, 0))
        power_stations = [Point(1, 1), Point(1, 9)]
        radius_drone_bs = 5
        obstacles = Obstacles()  # No obstacles

        drones, covered_stations = triangle.position_drones_triangle(power_stations, radius_drone_bs, obstacles)
        self.assertEqual(len(drones), 4, "There should be exactly 4 drones.")
        self.assertEqual(len(covered_stations), 1)

    def test_large_angle_two_clear_edges(self):
        # Triangle with a large angle and two clear edges
        triangle = Triangle(Point(0, 0), Point(10, 2), Point(20, 0))
        power_stations = [Point(1, 1), Point(1, 9)]
        radius_drone_bs = 5
        obstacles = Obstacles()  # No obstacles
        obstacles.add_triangle(Triangle(Point(9, 1), Point(9, 3), Point(2, 2)))

        drones, covered_stations = triangle.position_drones_triangle(power_stations, radius_drone_bs, obstacles)
        self.assertEqual(len(drones), 5, "There should be exactly 5 drones.")
        self.assertEqual(len(covered_stations), 1)

    def test_large_angle_one_clear_edge(self):
        # Triangle with one clear edge
        triangle = Triangle(Point(0, 0), Point(10, 2), Point(20, 0))
        power_stations = [Point(1, 1), Point(1, 9)]
        radius_drone_bs = 5
        obstacles = Obstacles()  # No obstacles
        obstacles.add_triangle(Triangle(Point(9, -1), Point(9, 3), Point(2, 2)))

        drones, covered_stations = triangle.position_drones_triangle(power_stations, radius_drone_bs, obstacles)
        self.assertIsNone(drones, "drones value is None")
        self.assertIsNone(covered_stations, "covered_stations is None")

    # TODO: check
    def test_fermat_point_applicable_all_paths_clear(self):
        # Fermat point applicable and all paths clear
        triangle = Triangle(Point(0, 0), Point(0, 10), Point(10, 0))
        power_stations = [Point(1, 1), Point(5, 5)]
        radius_drone_bs = 5
        obstacles = Obstacles()  # No obstacles

        drones, covered_stations = triangle.position_drones_triangle(power_stations, radius_drone_bs, obstacles)
        self.assertIn(triangle.compute_fermat_point(), drones)  # Fermat point should have a drone
        self.assertTrue(len(covered_stations) == len(power_stations))

    def test_obstructed_paths(self):
        # Path to Fermat point is obstructed
        triangle = Triangle(Point(0, 0), Point(0, 10), Point(10, 0))
        power_stations = [Point(1, 1), Point(5, 5)]
        radius_drone_bs = 5
        obstacles = Obstacles()
        obstacles.add_triangle(Triangle(Point(2, 2), Point(3, 3), Point(2, 3)))  # Obstacle blocking the path

        drones, covered_stations = triangle.position_drones_triangle(power_stations, radius_drone_bs, obstacles)
        self.assertIsNone(drones)
        self.assertIsNone(covered_stations)

if __name__ == '__main__':
    unittest.main()