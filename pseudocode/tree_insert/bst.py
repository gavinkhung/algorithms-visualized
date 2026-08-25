def run(tree, v):
    if tree.root is None:
        tree.root = Node(v)
        yield "new root " + str(v)
        return
    node = tree.root
    while True:
        yield "at " + str(node.value)
        if v == node.value:
            yield "already present"
            return
        if v < node.value:
            if node.left is None:
                node.left = Node(v)
                yield "insert " + str(v) + " left of " + str(node.value)
                return
            node = node.left
        else:
            if node.right is None:
                node.right = Node(v)
                yield "insert " + str(v) + " right of " + str(node.value)
                return
            node = node.right
