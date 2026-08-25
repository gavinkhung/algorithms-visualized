def sort(A):
    N = len(A)
    i = 0
    while i < N:
        j = i
        while j > 0 and A[j] < A[j - 1]:
            A[j], A[j - 1] = A[j - 1], A[j]
            yield "shift"
            j = j - 1
        yield
        i = i + 1
