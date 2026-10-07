---
title: Minimum Spanning Trees
subtitle: Connecting every node as cheaply as possible
---

A minimum spanning tree links all the nodes of a weighted graph using the least total edge weight. Prim's algorithm grows a single tree outward from a starting node, always adding the cheapest edge that reaches a new node. Kruskal's algorithm instead adds edges from cheapest to most expensive, using a union-find to skip any edge that would form a cycle. For contrast, the worst-case spanning tree picks the most expensive edges instead.

<iframe src="/embed/mst.html" title="Minimum Spanning Tree Visualizer"></iframe>
