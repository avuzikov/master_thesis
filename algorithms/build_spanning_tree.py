def build_spanning_tree(graphBuilder):
    components = graphBuilder.getComponents()
    powerStations = graphBuilder.getPowerStations()
    obstacles = graphBuilder.getObstacles()
    radiusBS = graphBuilder.getRadiusBS()
    radiusDroneBS = graphBuilder.getRadiusDroneBS()
    print(components)
    print(powerStations)
    print(obstacles)
    print(radiusBS)
    print(radiusDroneBS)
    return 0
    # Что я хочу на выходе? Массив ребер, для каждого я хочу знать начало, конец(как точки, так и кластеры), позиции дронов на ребре