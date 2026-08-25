def run(graph, start):
    reached = {start}
    MST_edges = []
    total = 0
    candidates = list(graph.Out(start))
    yield "start at " + str(start)
    while candidates and len(reached) != graph.n_nodes:
        candidates.sort(key=lambda e: e.weight)
        edge = candidates.pop(0)
        if edge.dst in reached:
            continue
        MST_edges.append((edge.src, edge.dst, edge.weight))
        reached.add(edge.dst)
        total = total + edge.weight
        yield "take " + str(edge.src) + "-" + str(edge.dst) + " (" + str(edge.weight) + ")"
        for out_edge in graph.Out(edge.dst):
            if out_edge.dst not in reached:
                candidates.append(out_edge)
    if len(reached) != graph.n_nodes:
        yield "graph is disconnected: no spanning tree"
