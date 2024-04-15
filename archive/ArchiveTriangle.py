'''
    def position_drones_triangle(self, power_stations, radius_drone_bs, obstacles):
        fermat_point = self.compute_fermat_point()

        if fermat_point is None:
            # Handle degenerate triangle case by using the two shortest edges
            edges = sorted([self._segment1, self._segment2, self._segment3],
                           key=lambda seg: seg._point1.distance_to(seg._point2))
            # return None, None if at least one of edges is blocked
            for edge in edges:
                if not obstacles.is_segment_clear(edge):
                    return None, None

            shortest_edges = edges[:2]  # Get the two shortest edges
            drones = []
            covered_stations = set()

            # Iterate over the two shortest edges
            for edge in shortest_edges:
                if obstacles.is_segment_clear(edge):
                    edge_drones, edge_covered = edge.position_drones(power_stations, radius_drone_bs, obstacles)
                    if edge_drones is not None:
                        drones += edge_drones  # Merge drone positions from both edges
                        covered_stations.update(edge_covered)  # Merge covered power stations from both edges

            if drones:  # If both edges were covered successfully, return result
                return drones, covered_stations

            return None, None  # No shortest edges were clear or no drones could be positioned

        large_angle_vertex = self._angle_is_large()
        if large_angle_vertex:
            # Check all edges for clarity
            clear_edges = [edge for edge in [self._segment1, self._segment2, self._segment3] if
                           obstacles.is_segment_clear(edge)]

            # If fewer than 2 edges are clear, return None, None
            if len(clear_edges) < 2:
                return None, None

            # Initialize containers for drones and covered stations
            drones = []
            covered_stations = set()

            # If exactly 2 edges are clear, use them
            if len(clear_edges) == 2:
                for edge in clear_edges:
                    edge_drones, edge_covered = edge.position_drones(power_stations, radius_drone_bs, obstacles)
                    if edge_drones is not None:
                        drones += edge_drones
                        covered_stations.update(edge_covered)
                return drones, covered_stations

            # If all 3 edges are clear, use the two edges connected to the large angle vertex
            if len(clear_edges) == 3:
                connected_edges = [edge for edge in clear_edges if large_angle_vertex in [edge._point1, edge._point2]]
                for edge in connected_edges:
                    edge_drones, edge_covered = edge.position_drones(power_stations, radius_drone_bs, obstacles)
                    if edge_drones is not None:
                        drones += edge_drones
                        covered_stations.update(edge_covered)
                return drones, covered_stations

        # Handle the case with the Fermat point
        segments_to_fermat = [Segment(vertex, fermat_point) for vertex in [self._point1, self._point2, self._point3]]
        clear_segments = [seg for seg in segments_to_fermat if obstacles.is_segment_clear(seg)]

        # TODO: fix this part of test
        if len(clear_segments) < 3:
            return None, None  # At least one path to Fermat point is blocked

        drones = [fermat_point]
        covered_stations = set()
        for seg in clear_segments:
            seg_drones, seg_covered = seg.position_drones(power_stations, radius_drone_bs, obstacles)
            if seg_drones is not None:
                drones += seg_drones
                covered_stations.update(seg_covered)

        return drones, covered_stations
'''

# Tests:

'''
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

    def test_equilateral(self):
        # Triangle with one clear edge
        triangle = Triangle(Point(0, 0), Point(20, 0), Point(10, 17.32050807))
        power_stations = [Point(1, 1), Point(1, 9)]
        radius_drone_bs = 2
        obstacles = Obstacles()  # No obstacles

        drones, covered_stations = triangle.position_drones_triangle(power_stations, radius_drone_bs, obstacles)
        self.assertEqual(len(drones), 16, "There should be exactly 16 drones.")
        self.assertEqual(len(covered_stations), 1)

    # TODO: fix test from here
    def test_equilateral_blocked_fermat_segment(self):
        # Triangle with one clear edge
        triangle = Triangle(Point(0, 0), Point(20, 0), Point(10, 17.32050807))
        power_stations = [Point(1, 1), Point(1, 9)]
        radius_drone_bs = 2
        obstacles = Obstacles()  # No obstacles
        obstacles.add_triangle(Triangle(Point(1.72, 1.0), Point(1.78, 1.0), Point(1.75, 1.1)))

        drones, covered_stations = triangle.position_drones_triangle(power_stations, radius_drone_bs, obstacles)
        self.assertEqual(len(drones), 16, "There should be exactly 5 drones.")
        self.assertEqual(len(covered_stations), 1)


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
'''