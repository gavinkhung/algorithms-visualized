def delete(buckets, v):
    for node in buckets[hash(v)]:
        if node.value == v:
            delete node from list
    (maybe rehash)
