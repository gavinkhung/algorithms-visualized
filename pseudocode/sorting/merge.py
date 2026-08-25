def sort(A):
    yield from merge_sort(A, 0, len(A))


def merge_sort(A, l, h):
    if h - l <= 1:
        return
    m = l + (h - l) // 2
    yield from merge_sort(A, l, m)
    yield from merge_sort(A, m, h)
    yield from merge(A, l, m, h)


def merge(A, l, m, h):
    T = [None] * (h - l)
    i = l
    j = m
    k = 0
    while i < m and j < h:
        if A[i] <= A[j]:
            T[k] = A[i]
            i = i + 1
        else:
            T[k] = A[j]
            j = j + 1
        yield
        k = k + 1
    while i < m:
        T[k] = A[i]
        i = i + 1
        yield "drain left"
        k = k + 1
    while j < h:
        T[k] = A[j]
        j = j + 1
        yield "drain right"
        k = k + 1
    k = 0
    while k < h - l:
        A[l + k] = T[k]
        yield "copy back"
        k = k + 1
