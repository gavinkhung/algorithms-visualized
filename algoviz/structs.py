"""Graph and tree types for algorithms to manipulate.

Each has a ``snapshot()`` method, which :func:`algoviz.capture.snapshot` uses
to record it. Graph node positions are computed once, so nodes do not move
during an animation.
"""

from __future__ import annotations

import math
from collections import namedtuple

Edge = namedtuple("Edge", "src dst weight")


# --------------------------------------------------------------------------
# graphs
# --------------------------------------------------------------------------


class Graph:
    """Adjacency-list graph with fixed node positions.

    ``edges`` takes ``(u, v)`` or ``(u, v, weight)``; the default weight is 1.
    An undirected edge is stored once in :attr:`edges` and reachable both
    ways through :meth:`Out`.
    """

    # Recorded even when only an outer frame holds it.
    is_holder = True

    def __init__(self, nodes, edges, directed=False, positions=None,
                 layout="spring", seed=0):
        self.nodes = list(nodes)
        self.directed = bool(directed)
        self._edges = []
        self._out = {n: [] for n in self.nodes}
        self._in = {n: [] for n in self.nodes}
        for raw in edges:
            u, v = raw[0], raw[1]
            w = raw[2] if len(raw) > 2 else 1
            self._edges.append(Edge(u, v, w))
            self._link(u, v, w)
            if not self.directed:
                self._link(v, u, w)
        self.positions = dict(positions) if positions else _layout(
            self.nodes, self._edges, layout, seed, self.directed
        )

    def _link(self, u, v, w):
        for node in (u, v):
            if node not in self._out:
                self._out[node] = []
                self._in[node] = []
                self.nodes.append(node)
        self._out[u].append(Edge(u, v, w))
        self._in[v].append(Edge(u, v, w))

    # Named as in the course pseudocode.
    def Out(self, node):  # noqa: N802
        return list(self._out.get(node, ()))

    def In(self, node):  # noqa: N802
        return list(self._in.get(node, ()))

    def neighbors(self, node):
        return [e.dst for e in self.Out(node)]

    def weight(self, u, v):
        for e in self._out.get(u, ()):
            if e.dst == v:
                return e.weight
        return None

    @property
    def edges(self):
        """All edges; an undirected edge appears once."""
        return list(self._edges)

    @property
    def n_nodes(self):
        return len(self.nodes)

    def remove_edge(self, u, v):
        """Remove u->v, and v->u if undirected."""
        self._edges = [
            e for e in self._edges
            if not (e.src == u and e.dst == v)
            and not (not self.directed and e.src == v and e.dst == u)
        ]
        self._out[u] = [e for e in self._out.get(u, ()) if e.dst != v]
        self._in[v] = [e for e in self._in.get(v, ()) if e.src != u]
        if not self.directed:
            self._out[v] = [e for e in self._out.get(v, ()) if e.dst != u]
            self._in[u] = [e for e in self._in.get(u, ()) if e.src != v]

    def copy(self):
        """A copy with the same node positions."""
        return Graph(
            self.nodes,
            [tuple(e) for e in self._edges],
            directed=self.directed,
            positions=self.positions,
        )

    def snapshot(self):
        return {
            "kind": "graph",
            "nodes": list(self.nodes),
            "edges": [tuple(e) for e in self._edges],
            "directed": self.directed,
            "positions": {n: tuple(p) for n, p in self.positions.items()},
        }


def _layout(nodes, edges, kind, seed, directed=False):
    """Node positions scaled to [-1, 1] on both axes.

    DAGs are drawn in layers and trees by depth. Other graphs use the best of
    a few seeded spring layouts, scored by how far nodes stay from edges. A
    circle is the fallback without networkx.
    """
    try:
        import networkx as nx
    except ImportError:
        return _circle(nodes)
    pairs = [(e.src, e.dst) for e in edges]
    g = nx.DiGraph() if directed else nx.Graph()
    g.add_nodes_from(nodes)
    g.add_edges_from(pairs)
    try:
        if kind == "circular":
            pos = nx.circular_layout(g)
        elif kind == "shell":
            pos = nx.shell_layout(g)
        elif directed and nx.is_directed_acyclic_graph(g):
            layers = [sorted(layer, key=nodes.index)
                      for layer in nx.topological_generations(g)]
            pos = _best_layered(g, layers, pairs, seed)
        elif not directed and nodes and nx.is_tree(g):
            depth = nx.single_source_shortest_path_length(g, nodes[0])
            layers = [[n for n in nodes if depth[n] == d]
                      for d in range(max(depth.values()) + 1)]
            pos = _best_layered(g, layers, pairs, seed)
        else:
            k = 2.0 / math.sqrt(max(len(nodes), 1))
            pos = max(
                (nx.spring_layout(g, seed=seed + i, k=k, iterations=150)
                 for i in range(4)),
                key=lambda p: _clearance(p, pairs),
            )
    except Exception:  # noqa: BLE001
        return _circle(nodes)
    return _fill({n: (float(p[0]), float(p[1])) for n, p in pos.items()})


def _best_layered(g, layers, pairs, seed):
    """Layered layout, trying row offsets that keep nodes off other edges."""
    import random

    rng = random.Random(seed)
    candidates = [[0.0] * len(layers),
                  [0.5 * (d % 2) for d in range(len(layers))]]
    candidates += [[rng.uniform(-0.5, 0.5) for _ in layers] for _ in range(10)]
    return max((_layered(g, layers, shift) for shift in candidates),
               key=lambda p: _clearance(p, pairs))


def _layered(g, layers, shift):
    """Rows top to bottom; each node placed under the mean of its parents."""
    pos = {}
    for depth, layer in enumerate(layers):
        if depth:
            def anchor(n):
                above = [pos[p][0] for p in g.pred[n] if p in pos] \
                    if g.is_directed() else \
                    [pos[p][0] for p in g.adj[n] if p in pos]
                return sum(above) / len(above) if above else 0.0
            layer = sorted(layer, key=anchor)
        for i, n in enumerate(layer):
            pos[n] = (i - (len(layer) - 1) / 2 + shift[depth], -depth)
    return pos


def _clearance(pos, pairs):
    """Smallest node-to-edge distance, relative to the drawing's size."""
    pts = list(pos.values())
    span = max(max(p[0] for p in pts) - min(p[0] for p in pts),
               max(p[1] for p in pts) - min(p[1] for p in pts)) or 1.0
    best = float("inf")
    for n, (px, py) in pos.items():
        for u, v in pairs:
            if n in (u, v):
                continue
            (ax, ay), (bx, by) = pos[u], pos[v]
            dx, dy = bx - ax, by - ay
            t = ((px - ax) * dx + (py - ay) * dy) / ((dx * dx + dy * dy) or 1)
            t = max(0.0, min(1.0, t))
            best = min(best, math.hypot(px - ax - t * dx, py - ay - t * dy))
    return best / span


def _fill(pos):
    """Stretch positions to [-1, 1] on both axes."""
    if not pos:
        return pos
    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]

    def scale(v, lo, hi):
        return 0.0 if hi == lo else 2 * (v - lo) / (hi - lo) - 1

    return {n: (scale(x, min(xs), max(xs)), scale(y, min(ys), max(ys)))
            for n, (x, y) in pos.items()}


def _circle(nodes):
    n = max(len(nodes), 1)
    return {
        node: (math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n))
        for i, node in enumerate(nodes)
    }


# --------------------------------------------------------------------------
# trees
# --------------------------------------------------------------------------


class Node:
    """A binary or 2-3 tree node.

    Binary nodes use ``value``, ``left`` and ``right``; 2-3 nodes use
    ``keys`` and ``children``. Extra keyword arguments go into ``meta``, and
    ``meta["note"]`` is drawn beside the node (AVL heights, for example).
    """

    def __init__(self, value=None, keys=None, children=None, **meta):
        if keys is not None:
            self.keys = list(keys)
        else:
            self.keys = [] if value is None else [value]
        self.children = list(children) if children is not None else [None, None]
        self.meta = dict(meta)

    @property
    def value(self):
        return self.keys[0] if self.keys else None

    @value.setter
    def value(self, v):
        if self.keys:
            self.keys[0] = v
        else:
            self.keys.append(v)

    def _child(self, i):
        return self.children[i] if i < len(self.children) else None

    def _set_child(self, i, node):
        while len(self.children) <= i:
            self.children.append(None)
        self.children[i] = node

    @property
    def left(self):
        return self._child(0)

    @left.setter
    def left(self, node):
        self._set_child(0, node)

    @property
    def right(self):
        return self._child(1)

    @right.setter
    def right(self, node):
        self._set_child(1, node)

    def is_leaf(self):
        return not any(c is not None for c in self.children)

    def snapshot(self):
        return {
            "kind": "node",
            # Lets the renderer match a `node` local to its place in the tree.
            "id": id(self),
            "keys": list(self.keys),
            "meta": {k: v for k, v in self.meta.items()
                     if isinstance(v, (int, float, str, bool, type(None)))},
            "children": [c.snapshot() if c is not None else None
                         for c in self.children],
        }


class Tree:
    """Holds the root, so an algorithm can replace it via ``tree.root``."""

    # Recorded even when only an outer frame holds it.
    is_holder = True

    def __init__(self, root=None):
        self.root = root

    def insert_bst(self, value):
        """BST insert without animation, for building a starting tree."""
        if self.root is None:
            self.root = Node(value)
            return
        cur = self.root
        while True:
            if value == cur.value:
                return
            if value < cur.value:
                if cur.left is None:
                    cur.left = Node(value)
                    return
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = Node(value)
                    return
                cur = cur.right

    def snapshot(self):
        return {
            "kind": "tree",
            "root": self.root.snapshot() if self.root is not None else None,
        }


def graph_from_text(text, directed=False, start=None):
    """Parse an adjacency list into ``(graph, start, error)``.

    Also checks that ``start`` names a node (case-insensitively).
    """
    from .inputs import parse_adjacency

    nodes, edges, error = parse_adjacency(text, directed=directed)
    if error:
        return None, None, error
    graph = Graph(nodes, edges, directed=directed)
    if start is None:
        return graph, None, None
    typed = str(start).strip()
    by_case = {str(n).lower(): n for n in graph.nodes}
    chosen = typed if typed in graph.nodes else by_case.get(typed.lower())
    if chosen is None:
        return None, None, (
            f"`{typed}` is not a node. Available: {', '.join(graph.nodes)}."
        )
    return graph, chosen, None


def bst_from(values):
    """Build a BST by inserting ``values`` in order."""
    tree = Tree()
    for v in values:
        tree.insert_bst(v)
    return tree


def heap_from(values):
    """``values`` heapified into a max-heap list."""
    heap = list(values)
    n = len(heap)
    for start in range(n // 2 - 1, -1, -1):
        x = start
        while True:
            left, right, big = 2 * x + 1, 2 * x + 2, x
            if left < n and heap[left] > heap[big]:
                big = left
            if right < n and heap[right] > heap[big]:
                big = right
            if big == x:
                break
            heap[x], heap[big] = heap[big], heap[x]
            x = big
    return heap
