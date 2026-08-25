def relax(graph, dist, pred, edge):
    if dist[edge.dst] > dist[edge.src] + edge.weight:
        dist[edge.dst] = dist[edge.src] + edge.weight
        pred[edge.dst] = edge.src
