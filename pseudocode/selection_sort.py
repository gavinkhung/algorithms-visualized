def sort(A):
    N = len(A)
    i = 0
    while i < N:
        m = i
        j = i + 1
        while j < N:
            if A[m] > A[j]:
                m = j
            yield
            j = j + 1
        A[i], A[m] = A[m], A[i]
        yield "swap"
        i = i + 1
