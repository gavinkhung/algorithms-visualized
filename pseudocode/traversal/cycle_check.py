def run(graph, start):
    ordering = []
    visited = set()
    on_stack = set()
    for node in graph.nodes:
        if node not in visited:
            found = yield from walk(graph, node, visited, on_stack, ordering)
            if found:
                yield "cycle found"
                return True
    yield "acyclic"
    return False


def walk(graph, node, visited, on_stack, ordering):
    visited.add(node)
    on_stack.add(node)
    ordering.append(node)
    yield "enter " + str(node)
    for edge in graph.Out(node):
        if edge.dst in on_stack:
            yield "back edge " + str(node) + "->" + str(edge.dst)
            return True
        if edge.dst not in visited:
            if (yield from walk(graph, edge.dst, visited, on_stack, ordering)):
                return True
    on_stack.discard(node)
    yield "leave " + str(node)
    return False
