def delete(node):
    if node.left is empty:
        replace node with node.right and return
    if node.right is empty:
        replace node with node.left and return
    successor = find_min(node.right)
    swap node.value <-> successor.value
    replace successor with successor.right and return
