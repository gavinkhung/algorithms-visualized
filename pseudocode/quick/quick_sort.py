def quicksort(A, lo, hi):
    if (hi - lo) <= 1: return
    p = partition(A, lo, hi)
    quicksort(A, lo, p)
    quicksort(A, p + 1, hi)
