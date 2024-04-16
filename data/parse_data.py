import json
import os

def parse_data(file_path):
    # Read and parse the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Access data
    radius_drones_bs = data['radius_drones_bs']
    base_stations = data['base_stations']
    power_stations = data['power_stations']
    obstacles = data['obstacles']

    # Example: Print the radius and the first base station
    print("Radius of drone base station:", radius_drones_bs)
    print("First base station coordinates:", base_stations[0])
    print("First obstacle's points:", obstacles[0]['points'])
