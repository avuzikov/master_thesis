from thesisCode.data.parse_data import parse_data


# Load test data from JSON
graph_builder = parse_data('./thesisCode/data/test_data1.json')
print("Components:", graph_builder.getComponents())
print("Radius BS:", graph_builder.getRadiusBS())
print("Radius drone:", graph_builder.getRadiusDroneBS())