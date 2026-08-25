def splay_insert(root, v):
    new_node = normal_bst_insert(root, v)
    splay(new_node)
    return new_node
