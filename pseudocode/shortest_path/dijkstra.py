def run(graph, start):
    dist = {n: float("inf") for n in graph.nodes}
    dist[start] = 0
    pred = {n: None for n in graph.nodes}
    visited = set()
    not_visited = set(graph.nodes)
    ordering = []
    yield "start at " + str(start)
    while not_visited:
        # Ties go to the alphabetically first node.
        node = min(not_visited, key=lambda n: (dist[n], n))
        if dist[node] == float("inf"):
            yield "unreachable nodes remain"
            return
        not_visited.remove(node)
        visited.add(node)
        ordering.append(node)
        yield "settle " + str(node) + " at " + str(dist[node])
        # One step per edge examined.
        for edge in graph.Out(node):
            if dist[edge.dst] > dist[edge.src] + edge.weight:
                dist[edge.dst] = dist[edge.src] + edge.weight
                pred[edge.dst] = edge.src
                yield "relax " + str(edge.src) + "->" + str(edge.dst)
            else:
                yield "no improvement via " + str(edge.src) + "->" + str(edge.dst)
