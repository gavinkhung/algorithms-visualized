def select(A, lo, hi, i):
    if (hi - lo) <= 1: return A[lo]
    p = partition(A, lo, hi)
    if p == i: return A[p]
    if i < p:  select(A, lo, p, i)
    if i > p:  select(A, p+1, hi, i)
