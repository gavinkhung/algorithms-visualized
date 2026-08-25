import random


def sort(A):
    yield from quicksort(A, 0, len(A))


def quicksort(A, lo, hi):
    if hi - lo <= 1:
        return
    p = yield from partition(A, lo, hi)
    yield from quicksort(A, lo, p)
    yield from quicksort(A, p + 1, hi)


def partition(A, lo, hi):
    i = lo + random.randrange(hi - lo)
    A[lo], A[i] = A[i], A[lo]
    v = A[lo]
    i = lo
    j = hi
    yield "pivot to lo"
    while True:
        while True:
            i = i + 1
            if not A[i] < v:
                break
            if i + 1 >= hi:
                break
        while True:
            j = j - 1
            if not A[j] > v:
                break
        yield
        if i >= j:
            A[lo], A[j] = A[j], A[lo]
            yield "place pivot"
            return j
        A[i], A[j] = A[j], A[i]
        yield "swap"
