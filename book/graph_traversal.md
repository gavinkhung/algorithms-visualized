---
title: Graph Traversal
subtitle: Exploring every node with depth-first and breadth-first search
description: Step through depth-first search, breadth-first search, and topological sorting on graphs you can edit.
---

Depth-first search follows one path as far as it can before backtracking, while breadth-first search visits nodes in order of their distance from the start. Both visit every node and edge in $O(n + m)$ time on a graph with $n$ nodes and $m$ edges. Kahn's algorithm builds on them to order a directed acyclic graph so that every edge points forward.

<iframe src="/embed/graph_traversal.html" title="Graph Traversal Visualizer"></iframe>
