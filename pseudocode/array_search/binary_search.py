def run(A, v):
    lo = 0
    hi = len(A)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        yield "probe " + str(A[mid])
        if A[mid] == v:
            yield "found at " + str(mid)
            return mid
        if A[mid] < v:
            lo = mid + 1
        else:
            hi = mid
    yield "not found"
    return -1
