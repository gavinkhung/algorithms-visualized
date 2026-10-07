---
title: Array Search
subtitle: Finding a value, or the k-th smallest, in an array
description: Step through linear scan, binary search, and quickselect to see how a sorted array turns an O(n) search into O(log n).
---

A linear scan checks every element in $O(n)$ time, while binary search uses a sorted array to halve the search space each step, finding a value in $O(\log n)$. Quickselect borrows quicksort's partitioning to find the $k$-th smallest element in expected $O(n)$ time without sorting the whole array.

<iframe src="/embed/array_search.html" title="Array Search Visualizer"></iframe>
