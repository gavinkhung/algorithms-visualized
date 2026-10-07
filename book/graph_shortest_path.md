---
title: Graph Shortest Paths
subtitle: Finding the cheapest route with BFS, Dijkstra, and Bellman–Ford
description: Watch BFS, Dijkstra's algorithm, and Bellman–Ford find the cheapest paths through a weighted graph.
---

When every edge has the same weight, breadth-first search already finds shortest paths. Dijkstra's algorithm handles non-negative weights by always settling the closest unsettled node, in $O((n + m) \log n)$ time with a heap. Bellman–Ford relaxes every edge $n - 1$ times, which takes $O(nm)$ time but also works with negative weights.

<iframe src="/embed/shortest_path.html" title="Shortest Path Visualizer"></iframe>
