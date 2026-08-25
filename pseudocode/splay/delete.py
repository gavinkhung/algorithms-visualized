def splay_delete(root, v):
    smaller, greater = splay_split(root, v)
    return splay_join(smaller, greater)
