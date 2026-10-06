def run(graph, start):
    ordering = []
    on_stack = set()  # entered, not yet finished ("grey")
    done = set()      # finished ("black")
    for node in graph.nodes:
        if node not in done:
            found = yield from walk(graph, node, None, on_stack, done, ordering)
            if found:
                yield "cycle found"
                return True
    yield "acyclic"
    return False


def walk(graph, node, parent, on_stack, done, ordering):
    on_stack.add(node)
    ordering.append(node)
    yield "enter " + str(node)
    for edge in graph.Out(node):
        # In an undirected graph, the edge back to the parent is not a cycle.
        if not graph.directed and edge.dst == parent:
            continue
        if edge.dst in on_stack:
            yield "back edge " + str(node) + "->" + str(edge.dst)
            return True
        if edge.dst not in done:
            if (yield from walk(graph, edge.dst, node, on_stack, done, ordering)):
                return True
    on_stack.discard(node)
    done.add(node)
    yield "leave " + str(node)
    return False
