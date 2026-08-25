TOMB = "x"


def run(A, v, nbuckets):
    buckets = [None] * nbuckets

    def slot_for(value):
        b = value % nbuckets
        probes = 0
        while buckets[b] not in (None, TOMB) and buckets[b] != value:
            b = (b + 1) % nbuckets
            probes = probes + 1
            if probes > nbuckets:
                return None
        return b

    for value in A:
        b = slot_for(value)
        buckets[b] = value
        yield "insert " + str(value) + " at " + str(b)

    b = v % nbuckets
    probes = 0
    while buckets[b] is not None and probes <= nbuckets:
        if buckets[b] == v:
            buckets[b] = TOMB
            yield "delete " + str(v) + ": tombstone at " + str(b)
            break
        b = (b + 1) % nbuckets
        probes = probes + 1
        yield "probe " + str(b)

    b = v % nbuckets
    probes = 0
    yield "search " + str(v) + " again"
    while buckets[b] is not None and probes <= nbuckets:
        if buckets[b] == v:
            yield "found (should not happen)"
            return True
        b = (b + 1) % nbuckets
        probes = probes + 1
        yield "walk past tombstone at " + str(b)
    yield "correctly not found"
    return False
