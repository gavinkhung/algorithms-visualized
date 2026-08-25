def delete(A, n, x):
    A[x] = A[n-1]       # rightmost leaf of the last layer
    n = n - 1
    if x > 0 and A[x] > A[parent(x)]: swim(A, x)
    else:                             sink(A, n, x)
    return n
