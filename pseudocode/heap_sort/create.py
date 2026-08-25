def heapify(A, n):
    for x = (n // 2) - 1 down to 0:
        sink(A, n, x)
