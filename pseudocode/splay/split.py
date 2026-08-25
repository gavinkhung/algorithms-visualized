def splay_split(root, v):
    root = splay_search(root, v)
    left, right = root.left, root.right
    root.left, root.right = empty, empty
    return left, right
