def search(buckets, v):
    for node in buckets[hash(v)]:
        if node.value == v:
            return True
    return False
