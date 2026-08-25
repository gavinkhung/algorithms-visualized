def insert(root, v):
    if v in root.values: return
    if root is empty:
        replace root with new leaf node
    if root is leaf:
        add v to root.values
    else:
        child = (find child that v must be in)
        insert(child, v)
        if child split:
            absorb it into root
    if root is now a 4-node:
        split it
