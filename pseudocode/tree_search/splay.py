def run(tree, v):
    if tree.root is None:
        yield "empty tree"
        return
    node = tree.root
    while True:
        yield "at " + str(node.value)
        if v == node.value:
            break
        step = node.left if v < node.value else node.right
        if step is None:
            break
        node = step
    yield "splay " + str(node.value)
    while tree.root is not node:
        path = path_to(tree.root, node)
        parent = path[-2]
        grand = path[-3] if len(path) >= 3 else None
        great = path[-4] if len(path) >= 4 else None
        if grand is None:
            attach(tree, None, parent, rotate(parent, node))
            yield "zig"
        elif (parent.left is node) == (grand.left is parent):
            lifted = rotate(grand, parent)
            attach(tree, great, grand, lifted)
            attach(tree, great, parent, rotate(parent, node))
            yield "zig-zig"
        else:
            attach(tree, grand, parent, rotate(parent, node))
            attach(tree, great, grand, rotate(grand, node))
            yield "zig-zag"
    yield "at root"


def path_to(root, target):
    stack = [(root, [])]
    while stack:
        cur, acc = stack.pop()
        if cur is None:
            continue
        acc = acc + [cur]
        if cur is target:
            return acc
        stack.append((cur.left, acc))
        stack.append((cur.right, acc))
    return []


def rotate(parent, child):
    if parent.left is child:
        parent.left = child.right
        child.right = parent
    else:
        parent.right = child.left
        child.left = parent
    return child


def attach(tree, above, old, new):
    if above is None:
        tree.root = new
    elif above.left is old:
        above.left = new
    elif above.right is old:
        above.right = new
