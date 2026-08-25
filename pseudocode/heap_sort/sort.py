def heapsort(A, n):
    heapify(A, n)
    for k = n-1 down to 1:
        swap A[0] <-> A[k]
        sink(A, k, 0)
