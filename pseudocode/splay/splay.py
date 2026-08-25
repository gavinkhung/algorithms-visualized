def splay(node):
    while node is not root:
        if node is zig from root:
            do splay-zig rotation to move node to the root level
        if node is zig-zig from grandparent:
            do splay-zig-zig rotation to move node up two levels
        if node is zig-zag from grandparent:
            do splay-zig-zag rotation to move node up two levels
