def prim(graph):
    reached = {start_node}
    outgoing_edges = graph.Out(start_node)
    MST_edges = set()
    while len(reached) != graph.n_nodes:
        edge = outgoing_edges.pop_lightest()
        if edge.dst in reached: continue
        MST_edges.insert(edge)
        reached.insert(edge.dst)
        for out_edge in graph.Out(edge.dst):
            outgoing_edges.insert(out_edge)
    return MST_edges
