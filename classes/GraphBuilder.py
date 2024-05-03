# Responsible for initializing graph

from thesisCode.classes.Segment import Segment
from thesisCode.classes.Obstacles import Obstacles
from thesisCode.classes.ConnectivityComponent import ConnectivityComponent

class GraphBuilder:
    def __init__(self, radius_bs, radius_drone_bs, base_stations, power_stations=[], obstacles=Obstacles()):
        # Filter out base and power stations that are inside obstacles
        base_stations, power_stations = self._check_stations_over_obstacles(base_stations, power_stations, obstacles)

        # Find initial connectivity components in graph
        self._components = self._find_components(base_stations, radius_bs, obstacles)

        # Filter out power stations covered by functioning ground BS
        self._power_stations = self._filter_covered_power_stations(power_stations, base_stations, radius_bs, obstacles)

        self._obstacles = obstacles
        self._radiusBS = radius_bs
        self._radiusDroneBS = radius_drone_bs

    def getComponents(self):
        return self._components

    def getPowerStations(self):
        return self._power_stations

    def getObstacles(self):
        return self._obstacles

    def getRadiusBS(self):
        return self._radiusBS

    def getRadiusDroneBS(self):
        return self._radiusDroneBS

    def _check_stations_over_obstacles(self, base_stations, power_stations, obstacles):
        filtered_base_stations = []
        filtered_power_stations = []

        # Check base stations
        for base in base_stations:
            if not obstacles.is_point_inside_any_obstacle(base):
                filtered_base_stations.append(base)
            else:
                print(f"Base station at {base} is within an obstacle and will be filtered out.")

        # Check power stations
        for power in power_stations:
            if not obstacles.is_point_inside_any_obstacle(power):
                filtered_power_stations.append(power)
            else:
                print(f"Power station at {power} is within an obstacle and will be filtered out.")

        return filtered_base_stations, filtered_power_stations

    def _filter_covered_power_stations(self, power_stations, base_stations, radius_bs, obstacles):
        filtered_power_stations = []
        for power in power_stations:
            is_close_to_base_station = False
            for base in base_stations:
                if power.distance_to(base) <= radius_bs:
                    # Check if the segment between power and base is clear of obstacles
                    segment = Segment(power, base)
                    if obstacles.is_segment_clear(segment):
                        is_close_to_base_station = True
                        print(f"Power station at {power} is initially covered by {base}.")
                        break  # No need to check further if one is found within radiusBS and clear of obstacles
            if not is_close_to_base_station:
                filtered_power_stations.append(power)
        return filtered_power_stations

    def _find_components(self, base_stations, radius_bs, obstacles):
        def dfs(node, visited, component):
            visited[node] = True
            component.addBS(base_stations[node])
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    dfs(neighbor, visited, component)

        # Create the graph
        graph = {i: [] for i in range(len(base_stations))}
        for i, base1 in enumerate(base_stations):
            for j, base2 in enumerate(base_stations):
                if i != j and base1.distance_to(base2) <= radius_bs:
                    # Check if the segment between base1 and base2 is clear of obstacles
                    segment = Segment(base1, base2)
                    if obstacles.is_segment_clear(segment):
                        graph[i].append(j)

        # Find connected components using DFS
        visited = [False] * len(base_stations)
        components = []
        component_number = 0
        for i in range(len(base_stations)):
            if not visited[i]:
                component = ConnectivityComponent(component_number)
                component_number += 1
                dfs(i, visited, component)
                components.append(component)

        return components