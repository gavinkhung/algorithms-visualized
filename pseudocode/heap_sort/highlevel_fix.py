# parent(x) = (x - 1) // 2

def swim(A, x):          # x's value may be too large for its position
    while x > 0 and A[x] > A[parent(x)]:
        swap A[x] <-> A[parent(x)]
        x = parent(x)

def sink(A, n, x):       # x's value may be too small for its position
    while True:
        l, r = 2*x + 1, 2*x + 2
        big = x
        if l < n and A[l] > A[big]: big = l
        if r < n and A[r] > A[big]: big = r
        if big == x: return
        swap A[x] <-> A[big]
        x = big
