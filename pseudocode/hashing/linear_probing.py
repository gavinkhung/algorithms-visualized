def run(A, v, nbuckets):
    buckets = [None] * nbuckets
    for value in A:
        b = value % nbuckets
        yield "insert " + str(value) + " -> " + str(b)
        probes = 0
        while buckets[b] is not None and buckets[b] != value:
            b = (b + 1) % nbuckets
            probes = probes + 1
            yield "occupied, probe " + str(b)
            if probes > nbuckets:
                yield "table is full"
                return False
        buckets[b] = value
        yield
    b = v % nbuckets
    yield "search " + str(v) + " from " + str(b)
    probes = 0
    while buckets[b] is not None and probes <= nbuckets:
        if buckets[b] == v:
            yield "found at " + str(b)
            return True
        b = (b + 1) % nbuckets
        probes = probes + 1
        yield "probe " + str(b)
    yield "not found"
    return False
