def find_min(root):
    if root is empty: (error)

    if root.left is not empty:
        return find_min(root.left)

    return root.value
