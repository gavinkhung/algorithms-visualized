def search_or_insert(root, v):
    if root is empty: # NOT FOUND, insert it
        node = new node
        node.value = v
        replace root with node
        postinsert(node)
        return node
    if v == root.value: return root
    child = root.left if v < root.value else root.right
    node = search_or_insert(child, v)
    postinsert(root)
    return node

def postinsert(node):
    # CONVENTION: height of empty node is zero
    node.height = 1 + max(node.left.height, node.right.height)
    if abs(node.left.height - node.right.height) > 1:
        determine which case the tree falls into
        perform either 1 or 2 balancing operations
        update the heights
