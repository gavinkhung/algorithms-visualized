def splay_search(root, v):
    if root is empty: return
    if v == root.value:
        splay(root)
        return root
    child = root.left if v < root.value else root.right
    if child is empty:
        splay(root)
        return NotFound
    return splay_search(child, v)
