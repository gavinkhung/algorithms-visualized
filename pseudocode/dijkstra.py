def dijkstra(graph, start):
    dist = {node: infinity for node in graph.nodes}
    dist[start] = 0
    pred = {node: none for node in graph.nodes}
    visited, not_visited = set(), set(graph.nodes)
    while not_visited:
        node = not_visited.pop_smallest_dist()
        visited.insert(node)
        for edge in graph.Out(node):
            relax(graph, dist, pred, edge)
