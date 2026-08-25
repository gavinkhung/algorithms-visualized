i = 0
while i < N:
    j = i
    while j > 0 and A[j] < A[j-1]:
        swap A[j] <-> A[j-1]
        j = j - 1
    i = i + 1
