def merge(A, l, m, h):
    T = scratch array of size (h - l)
    i, j, k = l, m, 0
    while i < m and j < h:
        if A[i] <= A[j]:
            T[k] = A[i]; i = i + 1
        else:
            T[k] = A[j]; j = j + 1
        k = k + 1
    while i < m:
        T[k] = A[i]; i = i + 1; k = k + 1
    while j < h:
        T[k] = A[j]; j = j + 1; k = k + 1
    for k = 0 .. (h - l - 1):
        A[l + k] = T[k]
