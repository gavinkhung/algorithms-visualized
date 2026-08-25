def run(graph, start):
    ordering = []
    visited = set()
    frontier = [start]
    while frontier:
        node = frontier.pop()
        if node in visited:
            continue
        visited.add(node)
        ordering.append(node)
        yield "visit " + str(node)
        for edge in graph.Out(node):
            if edge.dst not in visited:
                frontier.append(edge.dst)
        yield
    return ordering
