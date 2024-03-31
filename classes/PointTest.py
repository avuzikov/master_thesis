import unittest
from Point import Point

class TestPoint(unittest.TestCase):
    def test_point_attributes(self):
        """Test if the Point attributes are set correctly."""
        p = Point(3, 4)
        self.assertEqual(p.get_x(), 3)
        self.assertEqual(p.get_y(), 4)

    def test_point_equality(self):
        """Test the equality operation between two Point instances."""
        p1 = Point(1, 2)
        p2 = Point(1, 2)
        p3 = Point(3, 4)
        self.assertEqual(p1, p2)
        self.assertNotEqual(p1, p3)

    def test_point_distance(self):
        """Test the distance calculation between two Point instances."""
        p1 = Point(0, 0)
        p2 = Point(3, 4)  # Should form a 3-4-5 right triangle
        self.assertEqual(p1.distance_to(p2), 5.0)

    def test_point_repr(self):
        """Test the string representation of a Point instance."""
        p = Point(5, -3)
        self.assertEqual(repr(p), "Point(5, -3)")

if __name__ == '__main__':
    unittest.main()