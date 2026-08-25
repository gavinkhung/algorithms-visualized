# ---------------------------------------------------------------------
# NOT RECONSTRUCTED. Tarjan's SCC algorithm is on the 2026 reference
# sheet but appears nowhere in the 2025 lecture notes (mentioned once,
# as out of scope), so there is no source to transcribe from. The sketch
# below is the standard formulation and has NOT been checked against the
# course's version -- see NOTES.md section 11.5.
# ---------------------------------------------------------------------

def tarjan(graph):
    index = 0
    stack = []
    SCCs = []
    for node in graph.nodes:
        if node.index is undefined:
            strongconnect(node)
    return SCCs

def strongconnect(node):
    node.index = node.lowlink = index
    index = index + 1
    stack.push(node); node.on_stack = True
    for w in graph.Out(node):
        if w.index is undefined:
            strongconnect(w)
            node.lowlink = min(node.lowlink, w.lowlink)
        else if w.on_stack:
            node.lowlink = min(node.lowlink, w.index)
    if node.lowlink == node.index:      # node roots an SCC
        pop the stack down to and including node; that set is one SCC
