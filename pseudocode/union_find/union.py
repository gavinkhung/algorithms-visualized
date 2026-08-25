def union(A, B):
    A, B = find_root(A), find_root(B)
    if A == B: return
    if B.weight < A.weight: A, B = B, A   # join-by-size
    A.parent = B
    B.weight = B.weight + A.weight
    return B
