def merge_sort(A, l, h):
    if (h - l) <= 1: return
    m = l + (h - l)//2
    merge_sort(A, l, m)
    merge_sort(A, m, h)
    merge(A, l, m, h)
