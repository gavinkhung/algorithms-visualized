---
title: Tree Insertion
subtitle: Keeping a search tree balanced as it grows
---

Inserting into a plain binary search tree is simple, but sorted input turns it into a long chain with $O(n)$ search time. AVL trees rotate nodes to keep the heights of every node's two subtrees within one of each other, and 2–3 trees split full nodes so every leaf stays at the same depth. Both guarantee $O(\log n)$ height.

<iframe src="/embed/tree_insert.html" title="Tree Insertion Visualizer"></iframe>
