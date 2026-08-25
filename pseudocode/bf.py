def BF(graph, start):
    dist = {node: infinity for node in graph.nodes}
    dist[start] = 0
    pred = {node: none for node in graph.nodes}
    for i = 1..n:
        for edge in graph.edges:
            relax(graph, dist, pred, edge)
