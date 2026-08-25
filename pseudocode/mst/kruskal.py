def run(graph, start):
    parent = {n: n for n in graph.nodes}

    def find_root(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    MST_edges = []
    reached = set()
    total = 0
    for edge in sorted(graph.edges, key=lambda e: e.weight):
        ra = find_root(edge.src)
        rb = find_root(edge.dst)
        yield "consider " + str(edge.src) + "-" + str(edge.dst) + " (" + str(edge.weight) + ")"
        if ra == rb:
            yield "same component: would cycle, skip"
            continue
        parent[ra] = rb
        MST_edges.append((edge.src, edge.dst, edge.weight))
        reached.add(edge.src)
        reached.add(edge.dst)
        total = total + edge.weight
        yield "take it (total " + str(total) + ")"
    if len(MST_edges) != graph.n_nodes - 1:
        yield "graph is disconnected: this is a spanning forest"
