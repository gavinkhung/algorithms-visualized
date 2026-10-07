---
title: Tree Search
subtitle: Searching binary search trees, splay trees, and heaps
description: Step through searches in a binary search tree, a splay tree, and a heap, and see how each structure decides where to look.
---

A binary search tree keeps smaller keys on the left and larger keys on the right, so each comparison discards a whole subtree. A splay tree also moves every key it finds to the root, which makes repeated searches fast. A heap only orders parents above their children, so searching it may have to visit every node.

<iframe src="/embed/tree_search.html" title="Tree Search Visualizer"></iframe>
