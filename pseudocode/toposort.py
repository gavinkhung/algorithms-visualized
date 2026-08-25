def toposort(graph):
    make a temporary copy of graph
    ordering = []
    all_prereqs_met = {node for node in graph if graph.In(node) is empty}
    while all_prereqs_met:
        take_next = all_prereqs_met.pop()
        ordering.append(take_next)
        for followup in graph.Out(take_next):
            remove edge take_next -> followup
            if graph.In(followup) is now empty:
                all_prereqs_met.append(followup)
    return ordering
