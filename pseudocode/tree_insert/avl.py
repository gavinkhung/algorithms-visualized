def run(tree, v):
    yield from insert(tree, None, tree.root, v)


def height(node):
    return 0 if node is None else node.meta.get("h", 1)


def retag(node):
    node.meta["h"] = 1 + max(height(node.left), height(node.right))
    node.meta["note"] = "h=" + str(node.meta["h"])


def rotate_right(y):
    x = y.left
    y.left = x.right
    x.right = y
    retag(y)
    retag(x)
    return x


def rotate_left(x):
    y = x.right
    x.right = y.left
    y.left = x
    retag(x)
    retag(y)
    return y


def replace(tree, parent, node):
    # Replace the subtree root with `node`.
    if parent is None:
        tree.root = node
    elif node.value < parent.value:
        parent.left = node
    else:
        parent.right = node


def insert(tree, parent, node, v):
    if node is None:
        fresh = Node(v)
        retag(fresh)
        replace(tree, parent, fresh)
        yield "insert " + str(v)
        return
    if v == node.value:
        yield "already present"
        return
    child = node.left if v < node.value else node.right
    yield from insert(tree, node, child, v)
    retag(node)
    yield "retag " + str(node.value)

    balance = height(node.left) - height(node.right)
    if balance > 1:
        if v > node.left.value:
            node.left = rotate_left(node.left)
            yield "zig-zag at " + str(node.value)
        replace(tree, parent, rotate_right(node))
        yield "rotate right"
    elif balance < -1:
        if v < node.right.value:
            node.right = rotate_right(node.right)
            yield "zig-zag at " + str(node.value)
        replace(tree, parent, rotate_left(node))
        yield "rotate left"
