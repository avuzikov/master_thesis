import json
import os
from ..classes.GraphBuilder import GraphBuilder

def parse_data(file_path):
    # Read and parse the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Access data
    radius_drones_bs = data['radius_drones_bs']
    radius_bs = data['radius_bs']
    base_stations = data['base_stations']
    power_stations = data['power_stations']
    obstacles = data['obstacles']

    return GraphBuilder(radius_bs, radius_drones_bs, base_stations)  # power_stations=[], obstacles=[]
