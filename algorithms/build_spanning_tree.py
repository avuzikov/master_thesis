def build_spanning_tree(graph_builder):
    components = graph_builder.getComponents()
    power_stations = graph_builder.getPowerStations()
    obstacles = graph_builder.getObstacles()
    radius_drone_bs = graph_builder.getRadiusDroneBS()

    # Creating a list to store the edges of the spanning tree
    mst_edges = []

    # A set to keep track of connected components (using component names)
    connected = set()
    edges = []

    # Function to find all possible edges
    for i, comp in enumerate(components):
        for j in range(i + 1, len(components)):
            edge = comp.computeEdge(components[j], radius_drone_bs, power_stations, obstacles)
            if edge:
                edges.append(edge)

    # Sort edges by the number of drones, and if equal, by covered power stations
    edges.sort(key=lambda e: (len(e.dronesPositions), -len(e.coveredPS)))

    # Implementing a disjoint set to keep track of component connectivity
    parent = {comp._component_name: comp._component_name for comp in components}

    def find(comp_name):
        if parent[comp_name] != comp_name:
            parent[comp_name] = find(parent[comp_name])
        return parent[comp_name]

    def union(comp1, comp2):
        root1 = find(comp1)
        root2 = find(comp2)
        if root1 != root2:
            parent[root2] = root1

    # Building the MST
    for edge in edges:
        if find(edge.cluster1) != find(edge.cluster2):
            union(edge.cluster1, edge.cluster2)
            mst_edges.append(edge)
            connected.update([edge.cluster1, edge.cluster2])

            # If all components are connected, we can stop early
            if len(connected) == len(components):
                break

    return mst_edges