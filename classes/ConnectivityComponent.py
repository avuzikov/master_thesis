from thesisCode.classes.Segment import Segment

class Edge:
    def __init__(self, cluster1, cluster2, point1, point2, drones_positions, covered_ps):
        self.cluster1 = cluster1
        self.cluster2 = cluster2
        self.point1 = point1
        self.point2 = point2
        self.dronesPositions = drones_positions
        self.coveredPS = covered_ps

    def __str__(self):
        drones_str = ", ".join([f"({drone._x}, {drone._y})" for drone in self.dronesPositions])
        covered_ps_str = ", ".join([f"({ps._x}, {ps._y})" for ps in self.coveredPS])
        return (f"  Edge connects '{self.cluster1}' with '{self.cluster2}'\n"
                f"  Points: ({self.point1._x}, {self.point1._y}) -> ({self.point2._x}, {self.point2._y})\n"
                f"  Drones positioned at: [{drones_str}]\n"
                f"  Power Stations covered: [{covered_ps_str}]\n")

    __repr__ = __str__

class ConnectivityComponent:
    def __init__(self, component_name):
        self._component_name = component_name
        self.BSs = []

    def getComponentName(self):
        return self._component_name

    def addBS(self, new_bs):
        self.BSs.append(new_bs)

    def getBSs(self):
        return self.BSs

    def __str__(self):
        # Generate a list of string representations of Point objects and join them with ', '
        bs_strings = [str(bs) for bs in self.BSs]
        component_str = "Connectivity Component " + str(self._component_name) + ": [" + ', '.join(bs_strings) + "]"
        return component_str
    __repr__ = __str__

    def computeEdge(self, another_component, radius_drone_bs, power_stations=[], obstacles=[]):
        edge = None
        edge = None
        for first_station in self.BSs:
            for second_station in another_component.getBSs():
                drones, covered_power_stations =\
                    Segment(first_station, second_station).position_drones_evenly(power_stations, radius_drone_bs,
                                                                                  obstacles)
                if drones is None:
                    continue
                if edge is None or \
                        len(drones) < len(edge.dronesPositions) or \
                        (len(drones) == len(edge.dronesPositions) and
                         len(covered_power_stations) > len(edge.coveredPS)):
                    edge = Edge(self._component_name, another_component.getComponentName(),
                                first_station, second_station, drones, covered_power_stations)
        return edge
