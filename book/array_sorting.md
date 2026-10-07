---
title: Array Sorting
subtitle: Ways to put an array in order, from quadratic to optimal
description: Watch selection, insertion, merge, quick, and heap sort run step by step, and see why some take quadratic time while others reach O(n log n).
---

Pick a sorting algorithm and watch it rearrange the array one comparison at a time. Selection and insertion sort are simple but take quadratic time. On the other hand, merge sort, quicksort, and heapsort use divide and conquer, randomness, and a heap to reach $O(n \log n)$

<iframe src="/embed/array_sorting.html" title="Sorting Visualizer"></iframe>

## Selection Sort

Each pass scans the unsorted suffix $A[i..n-1]$ for its minimum and swaps it into position $i$. The scan always runs to the end, no matter what it finds, so every input costs the same:

Best Case: $\Theta(n^2)$

Average Case: $\Theta(n^2)$

Worst Case: $\Theta(n^2)$

$$
\begin{aligned}
C(n) &= \sum_{i=0}^{n-1} (n - 1 - i) \\
     &= \sum_{k=0}^{n-1} k \\
     &= \frac{n(n-1)}{2} \\
     &= O(n^2).
\end{aligned}
$$

## Insertion Sort

Each pass takes $A[i]$ and shifts it left past every larger element in the sorted prefix $A[0..i-1]$. Every shift fixes exactly one inversion, a pair $(i, j)$ with $i < j$ and $A[i] > A[j]$, so the cost depends on how out of order the input is.

Best Case: $\Theta(n)$

In the best case the array is already sorted, so each element is compared once and never moves:

$$
\begin{aligned}
C_{\text{best}}(n) &= \sum_{i=1}^{n-1} 1 \\
                   &= n - 1 \\
                   &= \Theta(n).
\end{aligned}
$$

Worst Case: $\Theta(n^2)$

In the worst case the array is reversed, so element $i$ is shifted past all $i$ elements before it:

$$
\begin{aligned}
C_{\text{worst}}(n) &= \sum_{i=1}^{n-1} i \\
                    &= \frac{n(n-1)}{2} \\
                    &= \Theta(n^2).
\end{aligned}
$$

Average Case: $\Theta(n^2)$

On average, each of the $\binom{n}{2}$ pairs is inverted with probability $\frac{1}{2}$, so the expected number of shifts is

$$
\begin{aligned}
\mathbb{E}[I] &= \binom{n}{2} \cdot \frac{1}{2} \\
              &= \frac{n(n-1)}{4} \\
              &= \Theta(n^2).
\end{aligned}
$$
