from thesisCode.algorithms.build_spanning_tree import build_spanning_tree
from thesisCode.data.parse_data import parse_data


# Load test data from JSON
graph_builder = parse_data('./thesisCode/data/test_data1.json')

components = graph_builder.getComponents()

print(build_spanning_tree(graph_builder))