def run(A, v):
    yield from probe(A, 0, v)


def probe(A, x, v):
    if x >= len(A):
        return False
    yield "at index " + str(x) + " (" + str(A[x]) + ")"
    if A[x] == v:
        yield "found " + str(v)
        return True
    if A[x] < v:
        yield "prune: subtree max is " + str(A[x])
        return False
    if (yield from probe(A, 2 * x + 1, v)):
        return True
    return (yield from probe(A, 2 * x + 2, v))
