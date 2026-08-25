def find_root(A):
    if A.parent is empty: return A
    A.parent = find_root(A.parent)   # path compression
    return A.parent
