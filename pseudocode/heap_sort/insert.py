def insert(A, n, v):
    A[n] = v            # leftmost empty slot of the last layer
    swim(A, n)
    return n + 1
