def run(A, v):
    i = 0
    while i < len(A):
        yield "check " + str(A[i])
        if A[i] == v:
            yield "found at " + str(i)
            return i
        i = i + 1
    yield "not found"
    return -1
