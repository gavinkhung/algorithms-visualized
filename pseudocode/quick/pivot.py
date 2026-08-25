def partition(A, lo, hi):
    swap A[lo] <-> A[random(lo, hi)]
    v = A[lo]
    i, j = lo, hi
    while True:
        while A[++i] < v:
            if (i+1) >= hi: break
        while A[--j] > v: pass
        if i >= j:
            swap A[lo] <-> A[j]
            return j
        swap A[i] <-> A[j]
