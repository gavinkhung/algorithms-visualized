def run(tree, v):
    if tree.root is None:
        tree.root = Node(keys=[v], children=[])
        yield "new root " + str(v)
        return
    promoted = yield from insert(tree.root, v)
    if promoted is not None:
        mid, left, right = promoted
        tree.root = Node(keys=[mid], children=[left, right])
        yield "split the root: height grows"


def is_leaf(node):
    return not node.children or all(c is None for c in node.children)


def split(node):
    keys = node.keys
    kids = node.children
    left = Node(keys=[keys[0]], children=kids[0:2] if kids else [])
    right = Node(keys=[keys[2]], children=kids[2:4] if kids else [])
    return keys[1], left, right


def insert(node, v):
    yield "at " + ";".join(str(k) for k in node.keys)
    if v in node.keys:
        yield "already present"
        return None
    if is_leaf(node):
        node.keys.append(v)
        node.keys.sort()
        yield "add " + str(v) + " to leaf"
    else:
        i = 0
        while i < len(node.keys) and v > node.keys[i]:
            i = i + 1
        promoted = yield from insert(node.children[i], v)
        if promoted is not None:
            mid, left, right = promoted
            node.keys.insert(i, mid)
            node.children[i : i + 1] = [left, right]
            yield "absorb " + str(mid)
    if len(node.keys) > 2:
        yield "4-node: split"
        return split(node)
    return None
