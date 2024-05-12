from math import inf
from thesisCode.classes.Triangle import Triangle


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


def find_component_by_name(components, name):
    for component in components:
        if component.getComponentName() == name:
            return component
    return None


def find_best_triangle(triple, components, radius_drone_bs, power_stations, obstacles):
    comp1 = find_component_by_name(components, triple[0])
    comp2 = find_component_by_name(components, triple[1])
    comp3 = find_component_by_name(components, triple[2])

    points_cluster1 = comp1.getBSs() if comp1 else []
    points_cluster2 = comp2.getBSs() if comp2 else []
    points_cluster3 = comp3.getBSs() if comp3 else []

    best_drones = None
    best_covered_ps = None
    min_drones_count = inf

    for p1 in points_cluster1:
        for p2 in points_cluster2:
            for p3 in points_cluster3:
                triangle = Triangle(p1, p2, p3)
                drones, covered_ps = triangle.position_drones_fermat(power_stations, radius_drone_bs, obstacles)
                if drones is None:
                    continue

                drones_count = len(drones)
                if drones_count < min_drones_count or (drones_count == min_drones_count and
                                                       len(covered_ps) > len(best_covered_ps)):
                    min_drones_count = drones_count
                    best_drones = drones
                    best_covered_ps = covered_ps

    return best_drones, best_covered_ps


def calculate_gain(edges_in_triple, best_drones_fermat):
    edge_drones_sum = sum([len(edge.dronesPositions) for edge in edges_in_triple])
    return edge_drones_sum - len(best_drones_fermat)


def create_edge_dict(edges):
    edge_dict = {}
    for edge in edges:
        pair = (min(edge.cluster1, edge.cluster2), max(edge.cluster1, edge.cluster2))
        edge_dict[pair] = edge
    return edge_dict


def evaluate_triple(triple, edges, graph_builder):
    radius_drone_bs = graph_builder.getRadiusDroneBS()
    power_stations = graph_builder.getPowerStations()
    obstacles = graph_builder.getObstacles()
    components = graph_builder.getComponents()

    edge_dict = create_edge_dict(edges)

    edges_in_triple = []
    for i in range(3):
        for j in range(i + 1, 3):
            edge = edge_dict.get((min(triple[i], triple[j]), max(triple[i], triple[j])))
            if edge:
                edges_in_triple.append(edge)

    if len(edges_in_triple) != 2:
        print("Something went wrong with triples array")
        return None

    best_drones, best_covered_ps = find_best_triangle(triple, components, radius_drone_bs, power_stations, obstacles)

    if best_drones is None:
        return {
            "triple": triple,
            "edges": edges_in_triple,
            "best_triangle": None,
            "gain": -inf
        }

    gain = calculate_gain(edges_in_triple, best_drones)

    return {
        "triple": triple,
        "edges": edges_in_triple,
        "best_triangle": {
            "triangle_drones": best_drones,
            "covered_power_stations": best_covered_ps
        },
        "gain": gain
    }


def find_best_triangles(edges, graph_builder):
    triples = find_triples(edges)
    results = [evaluate_triple(triple, edges, graph_builder) for triple in triples]
    return sorted(results, key=lambda x: x["gain"], reverse=True)


def opt_drone_deployment(sorted_gain_array, mst_edges):
    final_drones = []
    used_edges = set()

    i = 0
    while i < len(sorted_gain_array):
        entry = sorted_gain_array[0]
        if entry['gain'] <= 0:
            break

        final_drones.extend(entry['best_triangle']['triangle_drones'])
        for edge in entry['edges']:
            used_edges.add((edge.cluster1, edge.cluster2))
            used_edges.add((edge.cluster2, edge.cluster1))  # Handle bidirectional

        mst_edges = [e for e in mst_edges if
                     (e.cluster1, e.cluster2) not in used_edges and (e.cluster2, e.cluster1) not in used_edges]

        sorted_gain_array = [
            e for e in sorted_gain_array
            if not any((ed.cluster1, ed.cluster2) in used_edges or (ed.cluster2, ed.cluster1) in used_edges for ed in
                       e['edges'])
        ]
        i += 1

    for edge in mst_edges:
        final_drones.extend(edge.dronesPositions)

    final_drones = list(set(final_drones))

    return final_drones
