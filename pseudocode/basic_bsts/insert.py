def search_or_insert(root, v):
    if root is empty: # NOT FOUND, insert it
        node = new node
        node.value = v
        replace root with node
        return node
    if v == root.value:
        return root
    if v < root.value:
        return search_or_insert(root.left, v)
    if v > root.value:
        return search_or_insert(root.right, v)
