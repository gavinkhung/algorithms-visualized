def kruskal(graph):
    MST_edges = set()
    for edge in sort_by_weight(graph.edges):
        if not same_set(edge.src, edge.dst):
            MST_edges.insert(edge)
            union(edge.src, edge.dst)
    return MST_edges
