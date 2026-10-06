import random


def run(A, v):
    if not 0 <= v < len(A):
        yield "rank " + str(v) + " is out of range 0.." + str(len(A) - 1)
        return None
    return (yield from select(A, 0, len(A), v))


def select(A, lo, hi, i):
    if hi - lo <= 1:
        yield "answer " + str(A[lo])
        return A[lo]
    p = yield from partition(A, lo, hi)
    if p == i:
        yield "answer " + str(A[p])
        return A[p]
    if i < p:
        return (yield from select(A, lo, p, i))
    return (yield from select(A, p + 1, hi, i))


def partition(A, lo, hi):
    i = lo + random.randrange(hi - lo)
    A[lo], A[i] = A[i], A[lo]
    pivot = A[lo]
    i = lo
    j = hi
    yield "pivot to lo"
    while True:
        # One step per comparison.
        while True:
            i = i + 1
            yield "compare A[i] with pivot"
            if not A[i] < pivot:
                break
            if i + 1 >= hi:
                break
        while True:
            j = j - 1
            yield "compare A[j] with pivot"
            if not A[j] > pivot:
                break
        if i >= j:
            A[lo], A[j] = A[j], A[lo]
            yield "place pivot"
            return j
        A[i], A[j] = A[j], A[i]
        yield "swap"
