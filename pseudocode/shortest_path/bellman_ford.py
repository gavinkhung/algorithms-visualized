def run(graph, start):
    dist = {n: float("inf") for n in graph.nodes}
    dist[start] = 0
    pred = {n: None for n in graph.nodes}
    # Out() covers both directions of an undirected edge.
    edges = [edge for n in graph.nodes for edge in graph.Out(n)]
    for i in range(graph.n_nodes):
        changed = False
        # One step per edge examined.
        for edge in edges:
            if dist[edge.dst] > dist[edge.src] + edge.weight:
                dist[edge.dst] = dist[edge.src] + edge.weight
                pred[edge.dst] = edge.src
                changed = True
                yield "pass " + str(i + 1) + ": relax " + str(edge.src) + "->" + str(edge.dst)
            else:
                yield "pass " + str(i + 1) + ": no improvement via " + str(edge.src) + "->" + str(edge.dst)
        if not changed:
            yield "pass " + str(i + 1) + ": nothing changed, done"
            return
    for edge in edges:
        if dist[edge.src] != float("inf"):
            if dist[edge.dst] > dist[edge.src] + edge.weight:
                yield "negative cycle via " + str(edge.src)
                return
    yield "done"
