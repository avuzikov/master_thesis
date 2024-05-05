import json
import os
from thesisCode.classes.GraphBuilder import GraphBuilder
from thesisCode.classes.Point import Point
from thesisCode.classes.Obstacles import Obstacles
from thesisCode.classes.Triangle import Triangle

def parse_data(file_path):
    # Read and parse the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Access data
    radius_drones_bs = data['radius_drones_bs']
    radius_bs = data['radius_bs']
    base_stations_array = data['base_stations']
    power_stations_array = data['power_stations']
    obstacles_array = data['obstacles']

    base_stations = []
    power_stations = []
    obstacles = Obstacles()

    for station in base_stations_array:
        base_stations.append(Point(station[0], station[1]))

    for station in power_stations_array:
        power_stations.append(Point(station[0], station[1]))

    for obstacle in obstacles_array:
        points_array = obstacle['points']
        point0 = Point(points_array[0][0], points_array[0][1])
        point1 = Point(points_array[1][0], points_array[1][1])
        point2 = Point(points_array[2][0], points_array[2][1])
        obstacles.add_triangle(Triangle(point0, point1, point2))

    return GraphBuilder(radius_bs, radius_drones_bs, base_stations, power_stations, obstacles)
