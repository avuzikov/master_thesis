from thesisCode.algorithms.build_spanning_tree import build_spanning_tree
from thesisCode.algorithms.update_using_fermat_points import find_triples
from thesisCode.data.parse_data import parse_data


# Load test data from JSON
graph_builder = parse_data('./thesisCode/data/test_data3.json')

components = graph_builder.getComponents()

mst_edges, parent = build_spanning_tree(graph_builder)

# print(mst_edges)

# print(find_triples(mst_edges))
