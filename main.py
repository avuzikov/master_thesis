from thesisCode.algorithms.build_spanning_tree import build_spanning_tree
from thesisCode.algorithms.update_using_fermat_points import find_triples, evaluate_triple, find_best_triangles
from thesisCode.data.parse_data import parse_data


# Load test data from JSON
graph_builder = parse_data('./thesisCode/data/test_data3.json')

mst_edges, parent = build_spanning_tree(graph_builder)

triples = find_triples(mst_edges)

sorted_gain_array = find_best_triangles(mst_edges, graph_builder)
