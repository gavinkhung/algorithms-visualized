def lp_insert(buckets, v):
    if search(buckets, v): return
    b = hash(v)
    while buckets[b] not empty:
        b = next bucket
    buckets[b] = v
