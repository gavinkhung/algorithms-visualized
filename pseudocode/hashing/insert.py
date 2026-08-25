def insert(buckets, v):
    if search(buckets, v): return
    (maybe rehash)
    buckets[hash(v)].prepend(v)
