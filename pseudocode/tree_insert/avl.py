def run(tree, v):
    tree.root = yield from insert(tree.root, v)


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


def insert(node, v):
    if node is None:
        fresh = Node(v)
        retag(fresh)
        yield "insert " + str(v)
        return fresh
    if v == node.value:
        return node
    if v < node.value:
        node.left = yield from insert(node.left, v)
    else:
        node.right = yield from insert(node.right, v)
    retag(node)
    yield "retag " + str(node.value)

    balance = height(node.left) - height(node.right)
    if balance > 1:
        if v > node.left.value:
            node.left = rotate_left(node.left)
            yield "zig-zag at " + str(node.value)
        node = rotate_right(node)
        yield "rotate right"
    elif balance < -1:
        if v < node.right.value:
            node.right = rotate_right(node.right)
            yield "zig-zag at " + str(node.value)
        node = rotate_left(node)
        yield "rotate left"
    return node
