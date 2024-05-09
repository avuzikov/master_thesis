# Find all unique triples of clusters from MST edges
def find_triples(edges):
    pairs = {}
    for edge in edges:
        pairs.setdefault(edge.cluster1, []).append(edge.cluster2)
        pairs.setdefault(edge.cluster2, []).append(edge.cluster1)

    triples = set()
    for cluster1, neighbors in pairs.items():
        for i, cluster2 in enumerate(neighbors):
            for cluster3 in neighbors[i + 1:]:
                triples.add(tuple(sorted([cluster1, cluster2, cluster3])))

    return triples

def update_using_fermat_points(graph_builder, edges):
    return 0