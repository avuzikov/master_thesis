import unittest
from Obstacles import Obstacles
from Triangle import Triangle
from Point import Point
from Segment import Segment

class TestObstacles(unittest.TestCase):
    def setUp(self):
        self.obstacles = Obstacles()
        # Add a triangle obstacle
        self.obstacles.add_triangle(Triangle(Point(0, 0), Point(5, 0), Point(2.5, 5)))
        # Add another triangle obstacle
        self.obstacles.add_triangle(Triangle(Point(6, 0), Point(11, 0), Point(8.5, 5)))

    '''is_point_inside_any_obstacle'''
    def test_point_inside_obstacle(self):
        """Point is inside one of the obstacles."""
        inside_point1 = Point(2.5, 2)
        self.assertTrue(self.obstacles.is_point_inside_any_obstacle(inside_point1))
        inside_point2 = Point(8.5, 2)
        self.assertTrue(self.obstacles.is_point_inside_any_obstacle(inside_point2))
        inside_point3 = Point(1.25, 2.5)
        self.assertTrue(self.obstacles.is_point_inside_any_obstacle(inside_point3))
        inside_point4 = Point(5, 0)
        self.assertTrue(self.obstacles.is_point_inside_any_obstacle(inside_point4))

    def test_point_outside_but_near_obstacle(self):
        """Point is outside but near the obstacles."""
        outside_point = Point(1.22, 2.5)  # Between the two triangles
        self.assertFalse(self.obstacles.is_point_inside_any_obstacle(outside_point))

    def test_point_clearly_outside_obstacle(self):
        """Point is clearly outside any obstacles."""
        outside_point = Point(-10, -10)
        self.assertFalse(self.obstacles.is_point_inside_any_obstacle(outside_point))

    '''is_segment_clear'''
    # TODO: check failing test
    def test_segment_intersects_obstacle(self):
        """Segment intersects one of the obstacles."""
        intersecting_segment = Segment(Point(0, 0), Point(5, 5))
        self.assertFalse(self.obstacles.is_segment_clear(intersecting_segment))

    def test_segment_endpoint_inside_obstacle(self):
        """Segment's endpoint is inside an obstacle."""
        endpoint_inside_segment = Segment(Point(2.5, 2), Point(10, 10))
        self.assertFalse(self.obstacles.is_segment_clear(endpoint_inside_segment))

    def test_segment_clear_of_obstacles(self):
        """Segment is entirely clear of obstacles."""
        clear_segment = Segment(Point(12, 0), Point(15, 5))
        self.assertTrue(self.obstacles.is_segment_clear(clear_segment))

    '''
    def test_segment_along_obstacle_edge(self):
        """Segment lies along the edge of an obstacle but doesn't intersect its interior."""
        edge_segment = Segment(Point(0, 0), Point(5, 0))  # Along the base of the first triangle
        self.assertTrue(self.obstacles.is_segment_clear(edge_segment))
    '''