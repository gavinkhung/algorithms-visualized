def explore(graph, start):
    reachable = set()
    frontier = set({start})
    while frontier:
        node = frontier.pop()
        reachable.insert(node)
        for neighbor in graph.Out(node):
            if neighbor not in reachable:
                frontier.insert(neighbor)
    return reachable

# pop the most-recently inserted item (a stack) -> depth-first search
# pop the least-recently inserted item (a queue) -> breadth-first search
