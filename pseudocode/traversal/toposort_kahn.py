def run(graph, start):
    g = graph.copy()
    ordering = []
    all_prereqs_met = [n for n in g.nodes if not g.In(n)]
    yield "no prerequisites: " + ", ".join(all_prereqs_met)
    while all_prereqs_met:
        take_next = all_prereqs_met.pop()
        ordering.append(take_next)
        yield "take " + str(take_next)
        for edge in g.Out(take_next):
            followup = edge.dst
            g.remove_edge(take_next, followup)
            if not g.In(followup):
                all_prereqs_met.append(followup)
                yield str(followup) + " is now free"
            else:
                yield
    if len(ordering) != graph.n_nodes:
        yield "stuck: the graph has a cycle"
    return ordering
