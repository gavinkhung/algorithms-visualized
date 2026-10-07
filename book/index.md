---
title: Algorithms Visualized
thumbnail: ./gifs/sorting_selection.gif
site:
  hide_outline: false
---

> An algorithm must be seen to be believed.
>
> — [Donald Knuth](https://en.wikipedia.org/wiki/Donald_Knuth)

Interactive notebooks that animate classic algorithms and data structures step by step, right in your browser. Edit the code, change the input, and watch how each algorithm responds. Happy Learning - Gavin H

[![](https://img.shields.io/github/stars/gavinkhung/algorithms-visualized?style=social)](https://github.com/gavinkhung/algorithms-visualized)
[![](https://img.shields.io/github/forks/gavinkhung/algorithms-visualized?style=social)](https://github.com/gavinkhung/algorithms-visualized)

## Array Sorting

We begin our journey with a simple problem: how to sort an array of numbers. Through different implementations, we learn that algorithms can be quantitatively measured by their time and space complexity with Big O notation. We start with the naive approach and then turn to different strategies, like divide and conquer, randomness, and clever data structures, to go from $O(n^2)$ down to $O(n \log n)$.

::::{grid} 1 2 2 3
:class: text-center

:::{card}
:link: ./array_sorting.md
:header: **Selection Sort**

![Selection sort](./gifs/sorting_selection.gif)
:::

:::{card}
:link: ./array_sorting.md
:header: **Insertion Sort**

![Insertion sort](./gifs/sorting_insertion.gif)
:::

:::{card}
:link: ./array_sorting.md
:header: **Merge Sort**

![Merge sort](./gifs/sorting_merge.gif)
:::

:::{card}
:link: ./array_sorting.md
:header: **Quick Sort**

![Quicksort](./gifs/sorting_quick.gif)
:::

:::{card}
:link: ./array_sorting.md
:header: **Heap Sort**

![Heapsort](./gifs/sorting_heap.gif)
:::

::::

## Array Search

We continue our journey with another problem: searching for an element in an array. Through this process, we understand the tradeoff and balancing act between complexity and efficiency of algorithms. A linear scan checks every element in $O(n)$ time without any constraints, while binary search requires a sorted order to halve the search space each step, for $O(\log n)$ time. Quickselect borrows quicksort's partitioning to find the $k$-th smallest element in expected $O(n)$ time, without sorting at all.

::::{grid} 1 2 2 3
:class: text-center

:::{card}
:link: ./array_search.md
:header: **Linear Search**

![Linear scan](./gifs/array_search_linear_scan.gif)
:::

:::{card}
:link: ./array_search.md
:header: **Binary Search**

![Binary search](./gifs/array_search_binary_search.gif)
:::

:::{card}
:link: ./array_search.md
:header: **Quick Select**

![Quickselect](./gifs/array_search_quickselect.gif)
:::

::::

## Hash Tables

Now, let's focus more on using data structures with algorithms. Can we search faster than $O(\log n)$? By giving up order, hash tables find, insert, and delete in expected $O(1)$ time using the concept of hash functions to calculate an index in an array. There is no free lunch, so we have to handle collisions.

::::{grid} 1 2 2 3
:class: text-center

:::{card}
:link: ./hashing.md
:header: **Separate Chaining**

![Separate chaining](./gifs/hashing_separate_chaining.gif)
:::

:::{card}
:link: ./hashing.md
:header: **Linear Probing**

![Linear probing](./gifs/hashing_linear_probing.gif)
:::

:::{card}
:link: ./hashing.md
:header: **Probing + Delete**

![Tombstones](./gifs/hashing_linear_probing_delete.gif)
:::

::::

## Tree Search

Now, let's consider alternative data structures. Recall that there is a trade-off between simplicity and efficiency. Although arrays give you $O(1)$ access to any element by its index, inserting an element requires shifting everything after it, which takes $O(n)$ time. Trees avoid this by linking nodes with pointers, so a new node can be attached without moving the others.

In other words, sorted arrays are fast to search but slow to change, while trees keep data organized and still allow quick updates. Let's explore binary search trees, splay trees that move recent finds to the top, and heaps.

::::{grid} 1 2 2 3
:class: text-center

:::{card}
:link: ./tree_search.md
:header: **BST Search**

![BST search](./gifs/tree_search_bst_search.gif)
:::

:::{card}
:link: ./tree_search.md
:header: **Splay Search**

![Splay search](./gifs/tree_search_splay_search.gif)
:::

:::{card}
:link: ./tree_search.md
:header: **Heap Search**

![Heap search](./gifs/tree_search_heap_search_array.gif)
:::

::::

## Tree Insertion

As we continue our investigation into trees, we see that most implementations rely on maintaining certain properties of the data structure. For example, a binary search tree requires every node in a node's left subtree to be smaller than it and every node in its right subtree to be larger. Insertion is where these properties are most visibly enforced.

However, ordering alone is not enough: a binary search tree is only fast if it stays balanced. Insert sorted keys and it becomes a linked list with $O(n)$ search. AVL trees and 2–3 trees rebalance as they go, guaranteeing $O(\log n)$ height.

::::{grid} 1 2 2 3
:class: text-center

:::{card}
:link: ./tree_insert.md
:header: **BST Insert**

![BST insert](./gifs/tree_insert_bst_insert.gif)
:::

:::{card}
:link: ./tree_insert.md
:header: **AVL Insert**

![AVL insert](./gifs/tree_insert_avl_insert.gif)
:::

:::{card}
:link: ./tree_insert.md
:header: **2–3 Insert**

![2-3 insert](./gifs/tree_insert_2_3_insert.gif)
:::

::::

## Graph Traversal

We have now seen how data structures and algorithm design can be combined to solve problems. Many problems can be represented with a new data structure called a graph, which is a set of nodes connected by edges.

Let's begin our exploration by seeing how graphs can be traversed. On a graph with $n$ nodes and $m$ edges, depth-first and breadth-first search visit every node in $O(n + m)$ time, and they power topological sorting and cycle detection.

::::{grid} 1 2 2 3
:class: text-center

:::{card}
:link: ./graph_traversal.md
:header: **DFS**

![DFS](./gifs/traversal_dfs.gif)
:::

:::{card}
:link: ./graph_traversal.md
:header: **BFS**

![BFS](./gifs/traversal_bfs.gif)
:::

:::{card}
:link: ./graph_traversal.md
:header: **Topological Sort**

![Toposort](./gifs/traversal_toposort_kahn.gif)
:::

:::{card}
:link: ./graph_traversal.md
:header: **Cycle Detection**

![Cycle check](./gifs/traversal_cycle_check_dfs.gif)
:::

::::

## Shortest Paths

The first graph problem we will dive into is finding the path between two nodes with the minimum total weight, where each edge can have a different weight. The challenge is that we can't simply brute force it by listing every possible path and picking the cheapest, since a graph can have exponentially many paths. Instead, we have to leverage other data structures and algorithms, each of which comes with its own constraints.

When every edge has the same weight, BFS still works. Dijkstra's algorithm handles non-negative weights by greedily settling the closest node in $O((n + m)\log n)$ time, and Bellman–Ford also handles negative weights in $O(nm)$ time.

::::{grid} 1 2 2 3
:class: text-center

:::{card}
:link: ./graph_shortest_path.md
:header: **Dijkstra**

![Dijkstra](./gifs/shortest_path_dijkstra.gif)
:::

:::{card}
:link: ./graph_shortest_path.md
:header: **Bellman–Ford**

![Bellman-Ford](./gifs/shortest_path_bellman_ford.gif)
:::

:::{card}
:link: ./graph_shortest_path.md
:header: **BFS (Unweighted)**

![BFS shortest path](./gifs/shortest_path_bfs_unweighted.gif)
:::

::::

## Minimum Spanning Trees

Another problem to investigate with graphs is connecting every node as cheaply as possible. Given a weighted, connected graph, we want to choose $n - 1$ edges that link all $n$ nodes into a single tree with the minimum total weight. This tree is called a minimum spanning tree. Prim's algorithm grows a single tree outward from a starting node, while Kruskal's algorithm adds the cheapest remaining edges and uses a union-find to merge a forest of trees together. Both are greedy, and both are provably optimal.

::::{grid} 1 2 2 3
:class: text-center

:::{card}
:link: ./mst.md
:header: **Prim**

![Prim](./gifs/mst_prim.gif)
:::

:::{card}
:link: ./mst.md
:header: **Kruskal**

![Kruskal](./gifs/mst_kruskal.gif)
:::

::::

## About the Book

While taking [CS161 Design and Analysis of Algorithms](https://web.stanford.edu/class/cs161/), I became very interested in analyzing the mathematical runtime of data structures and algorithms. I believe it is the perfect combination of probability, problem solving, and creativity.

I often found myself drawing out data structures and algorithms on paper to see how they worked. I wanted to create a tool that lets you easily visualize algorithms and even see how they change when you edit the code. Every chapter here is an interactive notebook that runs in your browser: pick an algorithm, step through it frame by frame, edit its code to see what changes, and download the animation. I hope it helps you build the same intuition that drawing them out gave me.

The source is on [GitHub](https://github.com/gavinkhung/algorithms-visualized).
