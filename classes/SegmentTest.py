import unittest
from Point import Point
from Segment import Segment
from Triangle import Triangle
from Obstacles import Obstacles

class TestSegment(unittest.TestCase):
    def setUp(self):
        self.p1 = Point(0, 0)
        self.p2 = Point(10, 0)
        self.segment = Segment(self.p1, self.p2)

    '''__str__ '''

    def test_str_representation(self):
        """Test string representation of a segment."""
        self.assertEqual(str(self.segment), 'Segment(Point(0, 0), Point(10, 0))')

    '''_calculate_slope'''

    def test_non_vertical_slope_calculation(self):
        """Test calculation of non-vertical slope."""
        # Create two points that form a non-vertical segment with a known slope
        point1 = Point(1, 1)
        point2 = Point(3, 5)  # This creates a segment with a slope of 2 ((5-1) / (3-1))

        # Create a segment using these points
        non_vertical_segment = Segment(point1, point2)

        # Calculate the slope of the segment
        calculated_slope = non_vertical_segment._calculate_slope(point1, point2)

        # Assert that the calculated slope matches the expected value
        self.assertEqual(calculated_slope, 2, "The calculated slope should be 2 for the given points.")

    def test_slope_calculation(self):
        """Test calculation of slope."""
        vertical_segment = Segment(Point(0, 0), Point(0, 10))
        self.assertEqual(self.segment._calculate_slope(self.p1, self.p2), 0)
        self.assertEqual(vertical_segment._calculate_slope(Point(0, 0), Point(0, 10)), float('inf'))

    def test_negative_slope_calculation(self):
        """Test calculation of negative slope."""
        # Create two points that form a segment with a known negative slope
        point1 = Point(1, 5)
        point2 = Point(3, 1)  # This creates a segment with a slope of -2 ((1-5) / (3-1))

        # Create a segment using these points
        negative_slope_segment = Segment(point1, point2)

        # Calculate the slope of the segment
        calculated_slope = negative_slope_segment._calculate_slope(point1, point2)

        # Assert that the calculated slope matches the expected negative value
        self.assertEqual(calculated_slope, -2, "The calculated slope should be -2 for the given points.")

    '''_calculate_intercept'''

    def test_non_vertical_intercept_calculation(self):
        """Test calculation of y-intercept for non-vertical lines."""
        # Create a segment with a known slope and intercept
        point1 = Point(1, 3)  # Choose a point on the line
        point2 = Point(2, 5)  # This creates a segment with a slope of 2 ((5-3) / (2-1))
        segment = Segment(point1, point2)

        # Calculate the slope for use in intercept calculation
        slope = segment._calculate_slope(point1, point2)

        # Calculate the intercept using the method
        calculated_intercept = segment._calculate_intercept(point1, slope)

        # Assert that the calculated intercept matches the expected value
        # Expected intercept using point (1, 3) and slope 2: b = 3 - (2*1) = 1
        self.assertEqual(calculated_intercept, 1, "The calculated y-intercept should be 1 for the given line.")

    def test_vertical_intercept_calculation(self):
        """Test calculation of 'intercept' for vertical lines."""
        # Create a vertical segment
        point1 = Point(4, 0)  # Start point of the vertical line
        point2 = Point(4, 10)  # End point of the vertical line, same x-coordinate
        vertical_segment = Segment(point1, point2)

        # Calculate the slope for use in determining if the line is vertical
        slope = vertical_segment._calculate_slope(point1, point2)

        # Calculate the 'intercept' for the vertical line
        calculated_intercept = vertical_segment._calculate_intercept(point1, slope)

        # Assert that the 'intercept' for a vertical line is the x-coordinate
        self.assertEqual(calculated_intercept, 4,
                         "The 'intercept' for a vertical line should be the x-coordinate, which is 4 in this case.")

    '''is_parallel'''

    def test_non_parallel_segments(self):
        """Test that the method correctly identifies non-parallel segments."""
        # Create two segments with different slopes
        segment1 = Segment(Point(0, 0), Point(4, 4))  # Segment with a slope of 1
        segment2 = Segment(Point(1, 1), Point(4, 3))  # Segment with a different slope, not parallel to segment1

        # Use the is_parallel method to check if segment1 and segment2 are not parallel
        self.assertFalse(segment1.is_parallel(segment2),
                         "Segments with different slopes should not be identified as parallel.")

    def test_parallel_vertical_lines(self):
        """Test that the method correctly identifies two vertical lines as parallel."""
        segment1 = Segment(Point(0, 0), Point(0, 10))
        segment2 = Segment(Point(2, 0), Point(2, 10))  # Both segments are vertical

        self.assertTrue(segment1.is_parallel(segment2), "Two vertical lines should be identified as parallel.")

    def test_parallel_non_collinear_segments(self):
        """Test that the method correctly identifies parallel but not collinear segments."""
        # Create two parallel segments that are not collinear
        # Both segments will have a slope of 1, but they will have different y-intercepts
        segment1 = Segment(Point(0, 0), Point(5, 5))  # Passes through origin, slope of 1
        segment2 = Segment(Point(0, 2), Point(5, 7))  # Does not pass through origin, slope of 1, y-intercept of 2

        # Use the is_parallel method to check if segment1 and segment2 are parallel
        self.assertTrue(segment1.is_parallel(segment2),
                        "Segments that are parallel but not collinear should still be identified as parallel.")

    '''is_collinear'''

    def test_collinear_segments(self):
        """Test that the method correctly identifies collinear segments."""
        segment1 = Segment(Point(0, 0), Point(5, 5))
        segment2 = Segment(Point(10, 10), Point(15, 15))  # Continuation of segment1, hence collinear

        self.assertTrue(segment1.is_collinear(segment2), "Collinear segments should be identified as such.")

    def test_parallel_non_collinear_segments(self):
        """Test that parallel but not collinear segments are not identified as collinear."""
        segment1 = Segment(Point(0, 0), Point(5, 5))
        segment2 = Segment(Point(0, 1), Point(5, 6))  # Parallel to segment1 but shifted up by 1

        self.assertFalse(segment1.is_collinear(segment2),
                         "Parallel but not collinear segments should not be identified as collinear.")

    def test_non_parallel_segments(self):
        """Test that non-parallel segments are not identified as collinear."""
        segment1 = Segment(Point(0, 0), Point(5, 5))
        segment2 = Segment(Point(0, 0), Point(5, 4))  # Different slope from segment1

        self.assertFalse(segment1.is_collinear(segment2),
                         "Non-parallel segments should not be identified as collinear.")

    def test_vertical_non_parallel_segments(self):
        """Test that vertical non-parallel segments are not identified as collinear."""
        segment1 = Segment(Point(0, 0), Point(0, 5))
        segment2 = Segment(Point(1, 0), Point(1, 5))  # Both are vertical but not on the same line

        self.assertFalse(segment1.is_collinear(segment2),
                         "Vertical non-parallel segments should not be identified as collinear.")

    '''is_point_on_segment'''

    def test_point_on_segment(self):
        """Test a point lying on the segment between the endpoints."""
        segment = Segment(Point(0, 0), Point(10, 10))
        point_on_segment = Point(5, 5)

        self.assertTrue(segment.is_point_on_segment(point_on_segment), "The point should be on the segment.")

    def test_point_at_segment_end(self):
        """Test a point that coincides with one of the segment's endpoints."""
        segment = Segment(Point(0, 0), Point(10, 10))
        point_at_end = Point(10, 10)

        self.assertTrue(segment.is_point_on_segment(point_at_end),
                        "The point at the segment's end should be considered on the segment.")

    def test_point_outside_segment_on_line(self):
        """Test a point that lies outside the segment but on the line extended from the segment."""
        segment = Segment(Point(0, 0), Point(10, 10))
        point_outside = Point(15, 15)  # On the line extended from the segment

        self.assertFalse(segment.is_point_on_segment(point_outside),
                         "The point outside the segment bounds should not be considered on the segment.")

    def test_point_not_on_segment(self):
        """Test a point that does not lie on the segment or its extended line."""
        segment = Segment(Point(0, 0), Point(10, 10))
        point_not_on_line = Point(10, 0)  # Not on the line

        self.assertFalse(segment.is_point_on_segment(point_not_on_line),
                         "The point not on the segment or its extended line should not be considered on the segment.")

    def test_degenerate_segment_with_coinciding_point(self):
        """Test a degenerate segment (a point) with a coinciding point."""
        degenerate_segment = Segment(Point(5, 5), Point(5, 5))
        coinciding_point = Point(5, 5)

        self.assertTrue(degenerate_segment.is_point_on_segment(coinciding_point),
                        "The point coinciding with a degenerate segment (a point) should be considered on the segment.")

    def test_degenerate_segment_with_non_coinciding_point(self):
        """Test a degenerate segment (a single point) with a point outside the segment."""
        degenerate_segment = Segment(Point(5, 5), Point(5, 5))  # Segment is just a single point at (5, 5)
        outside_point = Point(6, 6)  # Point is not the same as the segment's single point

        self.assertFalse(degenerate_segment.is_point_on_segment(outside_point),
                         "A point outside a degenerate segment (a single point) should not be considered on the segment.")

    '''get_intersection_point'''

    def test_segments_do_not_intersect(self):
        """Test that the method returns None for non-intersecting segments."""
        segment1 = Segment(Point(0, 0), Point(0, 5))
        segment2 = Segment(Point(1, 1), Point(2, 2))  # Parallel to segment1, no intersection

        self.assertIsNone(segment1.get_intersection_point(segment2),
                          "The method should return None for non-intersecting segments.")

    def test_segments_intersect(self):
        """Test that the method returns the correct intersection point for intersecting segments."""
        segment1 = Segment(Point(0, 0), Point(10, 10))
        segment2 = Segment(Point(0, 10), Point(10, 0))  # Crosses segment1 at (5, 5)

        intersection = segment1.get_intersection_point(segment2)
        expected_point = Point(5, 5)

        self.assertIsNotNone(intersection, "There should be an intersection point.")
        self.assertEqual(intersection.get_x(), expected_point.get_x(),
                         "The intersection point x-coordinate is incorrect.")
        self.assertEqual(intersection.get_y(), expected_point.get_y(),
                         "The intersection point y-coordinate is incorrect.")

    def test_collinear_overlapping_segments(self):
        """Test that the method returns a valid intersection point for collinear overlapping segments."""
        segment1 = Segment(Point(0, 0), Point(10, 10))
        segment2 = Segment(Point(5, 5), Point(15, 15))  # Overlaps with segment1 from (5, 5) to (10, 10)

        intersection = segment1.get_intersection_point(segment2)
        valid_points = [Point(5, 5), Point(6, 6), Point(7, 7), Point(8, 8), Point(9, 9),
                        Point(10, 10)]  # Any of these points is a valid intersection

        self.assertIsNotNone(intersection, "There should be an intersection point for overlapping segments.")
        self.assertIn(intersection, valid_points, "The intersection point should be within the overlapping region.")

    def test_parallel_non_collinear_segments_no_intersection(self):
        """Test that parallel, non-collinear segments do not intersect."""
        segment1 = Segment(Point(0, 0), Point(10, 0))
        segment2 = Segment(Point(0, 1), Point(10, 1))  # Parallel to segment1 but with a different y-intercept

        self.assertIsNone(segment1.get_intersection_point(segment2),
                          "Parallel, non-collinear segments should not have an intersection point.")

    def test_collinear_segments_sharing_one_point(self):
        """Test that collinear segments sharing just one point intersect at that point."""
        segment1 = Segment(Point(0, 0), Point(5, 5))
        segment2 = Segment(Point(5, 5), Point(10, 10))  # Shares the endpoint (5, 5) with segment1

        intersection = segment1.get_intersection_point(segment2)
        expected_point = Point(5, 5)

        self.assertIsNotNone(intersection,
                             "There should be an intersection point for collinear segments sharing one point.")
        self.assertEqual(intersection, expected_point,
                         "The intersection point should be the common endpoint for collinear segments sharing one point.")

    def test_one_segment_inside_the_other(self):
        """Test that when one segment lies entirely within another, their intersection is the smaller segment itself."""
        larger_segment = Segment(Point(0, 0), Point(10, 10))
        smaller_segment = Segment(Point(3, 3), Point(6, 6))  # Entirely within larger_segment

        # Check intersection at one endpoint of the smaller segment
        intersection_start = larger_segment.get_intersection_point(smaller_segment)
        expected_start_point = smaller_segment._point1

        # Check intersection at the other endpoint of the smaller segment
        intersection_end = larger_segment.get_intersection_point(
            Segment(smaller_segment._point2, smaller_segment._point1))  # Reversed to use the other endpoint
        expected_end_point = smaller_segment._point2

        self.assertIsNotNone(intersection_start,
                             "The start point of the smaller segment should be an intersection point.")
        self.assertEqual(intersection_start, expected_start_point,
                         "The intersection should be at the start point of the smaller segment.")

        self.assertIsNotNone(intersection_end, "The end point of the smaller segment should be an intersection point.")
        self.assertEqual(intersection_end, expected_end_point,
                         "The intersection should be at the end point of the smaller segment.")

if __name__ == '__main__':
    unittest.main()