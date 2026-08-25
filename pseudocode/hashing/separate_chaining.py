def run(A, v, nbuckets):
    buckets = [[] for _ in range(nbuckets)]
    for value in A:
        b = value % nbuckets
        yield "insert " + str(value) + " -> bucket " + str(b)
        if value not in buckets[b]:
            buckets[b].insert(0, value)
        yield
    b = v % nbuckets
    yield "search " + str(v) + " in bucket " + str(b)
    for item in buckets[b]:
        yield "compare " + str(item)
        if item == v:
            yield "found"
            return True
    yield "not found"
    return False
