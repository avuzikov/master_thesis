import json


def save_drones_to_json(file_path, points):
    points_list = [point.to_list() for point in points]
    data = {"drones": points_list}
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
