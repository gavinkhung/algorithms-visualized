def run(graph, start):
    ordering = []
    visited = set()
    frontier = [start]
    while frontier:
        node = frontier.pop(0)
        if node in visited:
            continue
        visited.add(node)
        ordering.append(node)
        yield "visit " + str(node)
        for out_edge in graph.Out(node):
            if out_edge.dst not in visited:
                frontier.append(out_edge.dst)
        yield
    return ordering
