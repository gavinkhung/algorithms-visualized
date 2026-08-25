def run(graph, start):
    dist = {n: float("inf") for n in graph.nodes}
    dist[start] = 0
    pred = {n: None for n in graph.nodes}
    ordering = []
    frontier = [start]
    visited = set()
    while frontier:
        node = frontier.pop(0)
        if node in visited:
            continue
        visited.add(node)
        ordering.append(node)
        yield "visit " + str(node) + " at depth " + str(dist[node])
        for edge in graph.Out(node):
            if edge.dst not in visited and dist[edge.dst] == float("inf"):
                dist[edge.dst] = dist[node] + 1
                pred[edge.dst] = node
                frontier.append(edge.dst)
                yield "reach " + str(edge.dst)
