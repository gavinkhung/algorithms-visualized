def run(tree, v):
    node = tree.root
    while node is not None:
        yield "at " + str(node.value)
        if v == node.value:
            yield "found " + str(v)
            return node
        node = node.left if v < node.value else node.right
    yield str(v) + " not found"
    return None
