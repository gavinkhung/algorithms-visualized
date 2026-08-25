def run(graph, start):
    dist = {n: float("inf") for n in graph.nodes}
    dist[start] = 0
    pred = {n: None for n in graph.nodes}
    for i in range(graph.n_nodes):
        changed = False
        for edge in graph.edges:
            if dist[edge.src] == float("inf"):
                continue
            if dist[edge.dst] > dist[edge.src] + edge.weight:
                dist[edge.dst] = dist[edge.src] + edge.weight
                pred[edge.dst] = edge.src
                changed = True
                yield "pass " + str(i + 1) + ": " + str(edge.src) + "->" + str(edge.dst)
        if not changed:
            yield "pass " + str(i + 1) + ": nothing changed, done"
            return
    for edge in graph.edges:
        if dist[edge.src] != float("inf"):
            if dist[edge.dst] > dist[edge.src] + edge.weight:
                yield "negative cycle via " + str(edge.src)
                return
    yield "done"
