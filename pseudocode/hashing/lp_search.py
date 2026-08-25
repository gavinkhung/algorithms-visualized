def lp_search(buckets, v):
    b = hash(v)
    while buckets[b] != v and buckets[b] not empty and not looped around:
        b = next bucket
    return buckets[b] == v
