def splay_join(root1, root2):
    root1 = splay(find_max(root1))
    root1.right = root2
    return root1
