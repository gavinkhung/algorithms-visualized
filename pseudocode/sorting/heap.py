def sort(A):
    yield from heapsort(A, len(A))


def heapsort(A, n):
    yield from heapify(A, n)
    k = n - 1
    while k > 0:
        A[0], A[k] = A[k], A[0]
        yield "extract max"
        yield from sink(A, k, 0)
        k = k - 1


def heapify(A, n):
    x = n // 2 - 1
    while x >= 0:
        yield from sink(A, n, x)
        x = x - 1


def sink(A, n, x):
    while True:
        l = 2 * x + 1
        r = 2 * x + 2
        big = x
        if l < n and A[l] > A[big]:
            big = l
        if r < n and A[r] > A[big]:
            big = r
        yield
        if big == x:
            return
        A[x], A[big] = A[big], A[x]
        yield "sink"
        x = big
