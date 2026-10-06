"""Sample inputs and parsing for the input fields.

Inputs are seeded, so the same pattern and size always give the same input
and step counts can be compared across algorithms.
"""

from __future__ import annotations

import math
import random

ARRAY_PATTERNS = ["random", "sorted", "reversed", "duplicates"]

# Longest array accepted from the text field.
MAX_LEN = 64


def make_array(pattern, n, seed=0):
    """An array of the values 1..n in the given pattern."""
    if pattern == "sorted":
        return list(range(1, n + 1))
    if pattern == "reversed":
        return list(range(n, 0, -1))
    if pattern == "duplicates":
        return [(i % 3) + 1 for i in range(n)]
    values = list(range(1, n + 1))
    random.Random(seed).shuffle(values)
    return values


def format_array(values):
    """Format an array as :func:`parse_array` reads it."""
    return ", ".join(str(v) for v in values)


def parse_array(text, max_len=MAX_LEN):
    """Parse ``5, 2, 9``, ``5 2 9`` or ``[5, 2, 9]``.

    Returns ``(values, error)``; exactly one is None.
    """
    cleaned = text.strip()
    for opener, closer in ("[]", "()"):
        if cleaned.startswith(opener) and cleaned.endswith(closer):
            cleaned = cleaned[1:-1]
            break
    cleaned = cleaned.replace(",", " ").strip()

    if not cleaned:
        return None, "Array is empty. Type some numbers, e.g. `5, 2, 9, 1, 7`."

    values = []
    for token in cleaned.split():
        try:
            values.append(int(token))
        except ValueError:
            try:
                value = float(token)
            except ValueError:
                return None, f"`{token}` is not a number."
            if not math.isfinite(value):
                return None, f"`{token}` is not a finite number."
            values.append(value)

    if len(values) > max_len:
        return None, f"{len(values)} elements is too many (limit {max_len})."
    return values, None


def whole_number(value, label="v"):
    """A number box's value as ``(int, None)``, or ``(None, message)``.

    marimo gives ``None`` for an empty box and a float for a decimal.
    """
    if value is None:
        return None, f"Type a number for `{label}`."
    if value != int(value):
        return None, f"`{label}` must be a whole number, not {value}."
    return int(value), None


# --------------------------------------------------------------------------
# graphs
# --------------------------------------------------------------------------

GRAPH_SHAPES = ["sparse", "dense", "tree (nested)", "dag", "dag (negative)",
                "grid"]

MAX_NODES = 26
_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def node_name(i):
    return _LETTERS[i] if i < len(_LETTERS) else f"N{i}"


def make_graph(shape, n=7, seed=0, max_weight=9):
    """Generate ``(nodes, edges, directed)`` with seeded random weights.

    Undirected shapes start from a spanning tree, so they are connected. DAG
    edges always go from a lower to a higher index, so there are no cycles.
    "dag (negative)" always includes A->C(1), C->D(1), A->B(3), B->C(-4),
    which Dijkstra gets wrong.
    """
    n = max(2, min(int(n), MAX_NODES))
    rng = random.Random(f"{shape}|{n}|{seed}")
    nodes = [node_name(i) for i in range(n)]
    seen = set()
    edges = []

    def add(a, b, weight):
        if a == b:
            return False
        key = (a, b) if shape.startswith("dag") else frozenset((a, b))
        if key in seen:
            return False
        seen.add(key)
        edges.append((a, b, weight))
        return True

    if shape == "grid":
        cols = max(2, int(round(n ** 0.5)))
        for i in range(n):
            r, c = divmod(i, cols)
            if c + 1 < cols and i + 1 < n:
                add(nodes[i], nodes[i + 1], rng.randint(1, max_weight))
            if i + cols < n:
                add(nodes[i], nodes[i + cols], rng.randint(1, max_weight))
        return nodes, edges, False

    if shape.startswith("dag"):
        low = -4 if "negative" in shape else 1
        if "negative" in shape and n >= 4:
            a, b, c, d = nodes[:4]
            for u, v, w in ((a, c, 1), (a, b, 3), (b, c, -4), (c, d, 1)):
                add(u, v, w)
        for i in range(1, n):
            add(nodes[rng.randrange(i)], nodes[i], rng.randint(low, max_weight))
        for _ in range(int(0.5 * n)):
            a, b = sorted(rng.sample(range(n), 2))
            add(nodes[a], nodes[b], rng.randint(low, max_weight))
        return nodes, edges, True

    # Spanning tree first, for connectivity.
    for i in range(1, n):
        add(nodes[rng.randrange(i)], nodes[i], rng.randint(1, max_weight))
    if shape == "tree (nested)":
        return nodes, edges, False

    complete = n * (n - 1) // 2
    extra = max(1, n // 3) if shape == "sparse" else int(0.45 * complete)
    attempts = 0
    while len(edges) < (n - 1) + extra and attempts < 20 * complete:
        attempts += 1
        a, b = rng.sample(range(n), 2)
        add(nodes[a], nodes[b], rng.randint(1, max_weight))
    return nodes, edges, False


def format_adjacency(nodes, edges, directed=False):
    """Format as an adjacency list, one line per node.

    Undirected edges are listed under both endpoints.
    """
    out = {node: [] for node in nodes}
    for u, v, w in edges:
        out.setdefault(u, []).append((v, w))
        if not directed:
            out.setdefault(v, []).append((u, w))
    lines = []
    for node in nodes:
        listed = ", ".join(f"{v}({w})" for v, w in out.get(node, []))
        lines.append(f"{node}: {listed}")
    return "\n".join(lines)


def _parse_neighbour(item):
    """Parse ``B(4)``, ``B 4`` or ``B`` into ``((name, weight), error)``."""
    if item.endswith(")") and "(" in item:
        head, _, tail = item.partition("(")
        name, raw = head.strip(), tail[:-1].strip()
    else:
        parts = item.split()
        name, raw = parts[0], (parts[1] if len(parts) > 1 else None)
    if not name:
        return None, "missing neighbour name"
    if raw is None:
        return (name, 1), None
    try:
        weight = int(raw)
    except ValueError:
        try:
            weight = float(raw)
        except ValueError:
            return None, f"`{raw}` is not a weight"
    return (name, weight), None


def parse_adjacency(text, directed=False):
    """Parse an adjacency list into ``(nodes, edges, error)``.

    Accepts ``A: B(4), C(2)``, ``A: B 4, C 2`` or ``A: B, C`` (weight 1).
    Blank lines and ``#`` comments are ignored. In an undirected graph a
    repeated back-edge counts once.
    """
    nodes = []
    edges = []
    seen = set()

    def note(name):
        if name not in nodes:
            nodes.append(name)

    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            return None, None, (
                f"Line {lineno}: expected `NODE: neighbour, ...` "
                f"but found `{line}`."
            )
        head, _, tail = line.partition(":")
        source = head.strip()
        if not source:
            return None, None, f"Line {lineno}: missing a node name."
        note(source)
        for item in tail.split(","):
            item = item.strip()
            if not item:
                continue
            parsed, problem = _parse_neighbour(item)
            if problem:
                return None, None, f"Line {lineno}: {problem}."
            target, weight = parsed
            if target == source:
                return None, None, (
                    f"Line {lineno}: `{source}` links to itself; self-loops "
                    "are not supported."
                )
            note(target)
            key = (source, target) if directed else frozenset((source, target))
            if key in seen:
                continue
            seen.add(key)
            edges.append((source, target, weight))

    if not nodes:
        return None, None, "No nodes. Try `A: B(3), C(1)` on its own line."
    if len(nodes) > MAX_NODES:
        return None, None, f"{len(nodes)} nodes is too many (limit {MAX_NODES})."
    return nodes, edges, None
