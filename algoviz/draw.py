"""Matplotlib renderers, one per shape of data.

Each renderer reads a captured frame and infers what to draw from the local
variables. Renderers close their figure before returning so pyplot does not
keep every frame alive.
"""

from __future__ import annotations

import functools
import hashlib
import importlib
import warnings

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.text import Text

# "no-latex": the browser has no LaTeX install.
STYLE = ["science", "no-latex"]

# Registers the styles. scienceplots uses matplotlib APIs deprecated in 3.11.
with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    importlib.import_module("scienceplots")


def styled(render):
    """Run a renderer inside STYLE without touching the global rcParams.

    Figures are saved outside the style so its ``savefig.bbox: tight`` does
    not crop them.
    """
    @functools.wraps(render)
    def wrapper(*args, **kwargs):
        with plt.style.context(STYLE):
            fig = render(*args, **kwargs)
            serif = list(plt.rcParams["font.serif"])
        # Fonts resolve at draw time, after the context has exited.
        for text in fig.findobj(Text):
            text.set_fontfamily(serif)
        return fig
    return wrapper


PALETTE = [
    "#ef4444", "#3b82f6", "#f59e0b", "#10b981",
    "#8b5cf6", "#ec4899", "#14b8a6", "#f97316",
]
IDLE = "#cbd5e1"
MUTED = "#64748b"

# Rows reserved above the bars for pointer names.
POINTER_LANES = 3
# Chain cells shown per bucket before the rest collapse into "+N".
CHAIN_LANES = 6

# Integer locals that hold values, not indices.
VALUE_NAMES = {"v", "val", "value", "key", "pivot", "tmp", "temp", "target"}

# Indices into the scratch buffer when one exists; otherwise indices into `A`.
SCRATCH_CURSORS = {"k", "t"}
# Locals giving the offset in `A` where the scratch buffer is drawn.
SCRATCH_ORIGINS = ("l", "lo")


def new_axes(count=1, figsize=(6.5, 4.2), ratios=(3, 2)):
    """A fresh figure with ``count`` stacked axes, returned as ``(fig, [ax])``."""
    if count > 1:
        fig, axs = plt.subplots(
            count, 1, figsize=figsize, height_ratios=list(ratios[:count])
        )
        return fig, list(axs)
    fig, ax = plt.subplots(figsize=figsize)
    return fig, [ax]


def color_for(name: str) -> str:
    """Stable colour for a variable name."""
    digest = int(hashlib.md5(name.encode()).hexdigest(), 16)
    return PALETTE[digest % len(PALETTE)]


def heights(values):
    """Bar heights; non-numeric slots count as 0."""
    return [v if isinstance(v, (int, float)) and not isinstance(v, bool) else 0
            for v in values]


def pick_arrays(loc):
    """Split the frame's lists into ``(name, primary, scratch_or_None)``.

    The list named ``A`` is primary if present.
    """
    lists = {k: v for k, v in loc.items() if isinstance(v, list)}
    if not lists:
        raise ValueError("no list found in scope -- operate on `A`")
    primary_name = "A" if "A" in lists else next(iter(lists))
    primary = lists.pop(primary_name)
    scratch = next(iter(lists.items()), None)
    return primary_name, primary, scratch


def bars(ax, values, pointers, top, origin=0, span=None):
    """Draw one row of bars with pointer names stacked above their index.

    ``origin`` shifts the row right; ``span`` fixes the x extent.
    """
    n = len(values)
    span = n if span is None else span
    at = {}
    for name, idx in sorted(pointers.items()):
        at.setdefault(idx, []).append(name)

    hs = heights(values)
    colors = [color_for(at[x][0]) if x in at else IDLE for x in range(n)]
    ax.bar([origin + x for x in range(n)], hs, color=colors, zorder=2)

    # One font size per row, fitted to the longest label.
    slot = 1.0 / (span + 1.5)
    numbers = [str(v) for v in values
               if isinstance(v, (int, float)) and not isinstance(v, bool)]
    value_pt = _fit_pt(ax, max(numbers, key=len, default="0"), slot, 9)
    pointer_pt = _fit_pt(ax, max(pointers, key=len, default="i"), slot, 11)

    offset = top * 0.02
    for x, value in enumerate(values):
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            above = value >= 0
            ax.text(origin + x, value + (offset if above else -offset),
                    str(value), ha="center",
                    va="bottom" if above else "top", fontsize=value_pt)
    for idx, names in at.items():
        for row, name in enumerate(names):
            ax.text(origin + idx, top * (1.12 + 0.09 * row), name,
                    ha="center", va="bottom", fontsize=pointer_pt,
                    fontweight="bold", color=color_for(name))

    # Fixed limits: index n stays visible and the view does not jump.
    floor = min(0.0, min(hs, default=0.0))
    ax.set_xlim(-0.75, span + 0.75)
    ax.set_ylim(floor * 1.2 if floor < 0 else 0,
                top * (1.18 + 0.09 * POINTER_LANES))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.minorticks_off()
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)


@styled
def render_array(frame):
    """Bar chart of the primary array, plus a scratch row when one exists."""
    loc = frame["locals"]
    _, arr, scratch = pick_arrays(loc)
    n = len(arr)
    # Largest magnitude, so all-negative arrays still get a positive scale.
    top = max((abs(h) for h in heights(arr)), default=1) or 1

    indices = {
        k: v for k, v in loc.items()
        if type(v) is int and k not in VALUE_NAMES and 0 <= v <= n
    }
    main = {k: v for k, v in indices.items()
            if not scratch or k not in SCRATCH_CURSORS}

    fig, panes = new_axes(
        2 if scratch else 1, (6.5, 5.6) if scratch else (6.5, 4.2)
    )
    # Set before drawing; label sizes depend on the axes width.
    fig.subplots_adjust(left=0.02, right=0.98, top=0.95, bottom=0.04,
                        hspace=0.32)
    ax = panes[0]
    ax2 = panes[1] if len(panes) > 1 else None

    if scratch and ax2 is not None:
        name, values = scratch
        scratch_ptrs = {
            k: v for k, v in indices.items()
            if k in SCRATCH_CURSORS and v <= len(values)
        }
        origin = next((loc[k] for k in SCRATCH_ORIGINS
                       if type(loc.get(k)) is int), 0)
        if origin + len(values) > n:
            origin = 0
        bars(ax2, values, scratch_ptrs, top, origin=origin,
             span=max(n, len(values)))
        ax2.set_title(f"{name}  (scratch)", fontsize=9, loc="left",
                      pad=8, color=MUTED)

    bars(ax, arr, main, top)

    plt.close(fig)
    return fig


# --------------------------------------------------------------------------
# graphs
# --------------------------------------------------------------------------

# Local names the graph renderer recognises, in priority order.
DONE_SETS = ("visited", "reached", "done", "in_tree", "ordering")
OPEN_SETS = ("frontier", "not_visited", "all_prereqs_met", "queue", "stack",
             "on_stack")
CURSORS = ("node", "current", "take_next", "u")
EDGE_SETS = ("MST_edges", "tree_edges", "path", "chosen")
# The edge currently being examined.
EDGE_CURSORS = ("edge",)
DIST_MAPS = ("dist", "distance", "d")
PRED_MAPS = ("pred", "parent", "prev")

NODE_DONE = "#10b981"
NODE_OPEN = "#f59e0b"
NODE_CURRENT = "#ef4444"
NODE_IDLE = "#e2e8f0"
EDGE_IDLE = "#cbd5e1"
EDGE_PICK = "#0f172a"
EDGE_CURRENT = NODE_CURRENT


def _as_membership(value):
    """Coerce a set/list/dict local into a membership set, or None."""
    if isinstance(value, (set, frozenset)):
        return set(value)
    if isinstance(value, (list, tuple)):
        return {v for v in value if isinstance(v, (str, int, float))}
    if isinstance(value, dict):
        return set(value.keys())
    return None


def _find_graph(loc):
    """``(graph, removed_edges)``.

    With two graphs in scope (one a copy being emptied, as in Kahn's
    algorithm), the fuller one is drawn and edges missing from the other are
    returned as removed.
    """
    graphs = [v for v in loc.values()
              if isinstance(v, dict) and v.get("kind") == "graph"]
    if not graphs:
        return None, set()
    full = max(graphs, key=lambda g: len(g["edges"]))
    live = min(graphs, key=lambda g: len(g["edges"]))
    kept = {(u, v) for u, v, _ in live["edges"]}
    removed = {(u, v) for u, v, _ in full["edges"]} - kept
    return full, removed


def _edge_key(item):
    """Normalise an edge-ish value to an unordered (a, b) pair."""
    if isinstance(item, (tuple, list)) and len(item) >= 2:
        return frozenset((item[0], item[1]))
    return None


# Largest node diameter in pixels.
MAX_GRAPH_NODE_PX = 34


def _graph_view(ax, positions, label_below):
    """Fit the graph to the axes and return the node diameter in pixels.

    Margins leave room for half a node and, if shown, the distance labels.
    """
    fig = ax.figure
    box = ax.get_position()
    w = box.width * fig.get_figwidth() * fig.dpi
    h = box.height * fig.get_figheight() * fig.dpi
    pts = list(positions.values())
    if not pts:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        return MAX_GRAPH_NODE_PX
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    xspan = (max(xs) - min(xs)) or 1.0
    yspan = (max(ys) - min(ys)) or 1.0
    below = 16 if label_below else 0

    def scales(node):
        mx, top = node / 2 + 6, node / 2 + 6
        return (w - 2 * mx) / xspan, (h - top - (top + below)) / yspan, mx, top

    # Node size comes from the closest pair of nodes.
    sx, sy, _, _ = scales(MAX_GRAPH_NODE_PX)
    closest = min(
        (((a[0] - b[0]) * sx) ** 2 + ((a[1] - b[1]) * sy) ** 2) ** 0.5
        for i, a in enumerate(pts) for b in pts[i + 1:]
    ) if len(pts) > 1 else MAX_GRAPH_NODE_PX
    node = max(12.0, min(MAX_GRAPH_NODE_PX, 0.62 * closest))
    sx, sy, mx, top = scales(node)
    ax.set_xlim(min(xs) - mx / sx, max(xs) + mx / sx)
    ax.set_ylim(min(ys) - (top + below) / sy, max(ys) + top / sy)
    return node


@styled
def render_graph(frame):
    """Draw a graph, styled from the frame's locals.

    Sets like ``visited`` and ``frontier`` colour nodes, ``dist`` labels
    them, and ``pred`` or ``MST_edges`` highlight edges.
    """
    loc = frame["locals"]
    graph, removed = _find_graph(loc)
    if graph is None:
        raise ValueError("no Graph in scope -- build one with `Graph(...)`")

    pos = graph["positions"]
    done = next((_as_membership(loc[n]) for n in DONE_SETS if n in loc), None) or set()
    opened = next((_as_membership(loc[n]) for n in OPEN_SETS if n in loc), None) or set()
    current = next((loc[n] for n in CURSORS
                    if isinstance(loc.get(n), (str, int)) and loc[n] in pos),
                   None)
    dist = next((loc[n] for n in DIST_MAPS
                 if n in loc and isinstance(loc[n], dict)), None)
    pred = next((loc[n] for n in PRED_MAPS
                 if n in loc and isinstance(loc[n], dict)), None)

    picked = set()
    for name in EDGE_SETS:
        value = loc.get(name)
        if isinstance(value, (set, frozenset, list, tuple)):
            for item in value:
                key = _edge_key(item)
                if key:
                    picked.add(key)
    if pred:
        for child, parent in pred.items():
            if parent is not None and parent in pos and child in pos:
                picked.add(frozenset((parent, child)))

    # Ignore a stale `edge` from a previous node's loop.
    edge = next((loc[n] for n in EDGE_CURSORS if n in loc), None)
    looking = _edge_key(edge)
    if looking and current is not None and edge[0] != current:
        looking = None

    fig, panes = new_axes(1, (6.5, 5.0))
    # Set before measuring; node sizes depend on the axes size.
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    ax = panes[0]
    node_px = _graph_view(ax, pos, label_below=dist is not None)
    node_pt = node_px * 72.0 / ax.figure.dpi
    # 6.5pt minimum; the site shows figures at about 80% size.
    small_pt = max(6.5, min(8.0, node_pt * 0.34))

    # One LineCollection per edge style and one scatter for all nodes, for
    # speed.
    styles = {}
    for src, dst, weight in graph["edges"]:
        if src not in pos or dst not in pos:
            continue
        x0, y0 = pos[src]
        x1, y1 = pos[dst]
        key = frozenset((src, dst))
        chosen = key in picked
        hot = key == looking
        gone = (src, dst) in removed
        color = EDGE_CURRENT if hot else EDGE_PICK if chosen else EDGE_IDLE
        style = (color, 2.4 if (chosen or hot) else 1.0,
                 ":" if gone else "-",
                 1.0 if (chosen or hot) else 0.25 if gone else 0.7)
        styles.setdefault(style, []).append([(x0, y0), (x1, y1)])
        if graph["directed"]:
            ax.annotate(
                "", xy=(x1, y1), xytext=(x0, y0), zorder=1,
                annotation_clip=True,
                arrowprops=dict(
                    arrowstyle="-|>", shrinkA=node_pt / 2 + 1,
                    shrinkB=node_pt / 2 + 1,
                    color=color, alpha=0.25 if gone else 1.0,
                    linewidth=0),
            )
        if weight != 1 and not gone:
            # Under the nodes, so a node label wins any overlap.
            ax.text((x0 + x1) / 2, (y0 + y1) / 2, str(weight),
                    fontsize=small_pt, ha="center", va="center", zorder=1.5,
                    color=MUTED,
                    bbox=dict(boxstyle="round,pad=0.12", fc="white",
                              ec="none", alpha=0.85))

    for (color, width, dash, alpha), segments in styles.items():
        ax.add_collection(LineCollection(
            segments, colors=color, linewidths=width, linestyles=dash,
            alpha=alpha, zorder=1))

    xs, ys, faces = [], [], []
    for node in graph["nodes"]:
        if node not in pos:
            continue
        x, y = pos[node]
        if node == current:
            face = NODE_CURRENT
        elif node in done:
            face = NODE_DONE
        elif node in opened and not (
            dist is not None and dist.get(node) == float("inf")
        ):
            # Open but at distance infinity means not yet discovered.
            face = NODE_OPEN
        else:
            face = NODE_IDLE
        xs.append(x)
        ys.append(y)
        faces.append(face)
        ax.text(x, y, str(node), ha="center", va="center", zorder=4,
                fontsize=min(10.0, node_pt * 0.45), fontweight="bold",
                color="white" if face != NODE_IDLE else "#0f172a")
        if dist is not None and node in dist:
            value = dist[node]
            shown = "inf" if value == float("inf") else str(value)
            # Offset in points because the marker size is in points.
            ax.annotate(shown, (x, y), xytext=(0, -(node_pt / 2 + 2)),
                        textcoords="offset points", ha="center",
                        va="top", zorder=4, fontsize=small_pt,
                        color="#0f172a",
                        fontweight="bold")
    ax.scatter(xs, ys, s=node_pt ** 2, zorder=2, c=faces,
               edgecolors="#334155", linewidths=1.0)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.minorticks_off()
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(False)
    plt.close(fig)
    return fig


# --------------------------------------------------------------------------
# trees
# --------------------------------------------------------------------------


# Locals that name the current tree node, in priority order.
TREE_CURSORS = ("node", "cur", "current")


def _tree_cursor(loc):
    """Identity of the node the algorithm is at, or None."""
    for name in TREE_CURSORS:
        value = loc.get(name)
        if isinstance(value, dict) and value.get("kind") == "node":
            return value.get("id")
    return None


def _find_tree(loc):
    """Root of the Tree in scope, else the first Node, else None."""
    for value in loc.values():
        if isinstance(value, dict) and value.get("kind") == "tree":
            return value.get("root")
    for value in loc.values():
        if isinstance(value, dict) and value.get("kind") == "node":
            return value
    return None


def _place(node, depth, counter, out):
    """Lay out nodes by in-order position and depth; return the node's x.

    Nodes with three children (2-3 nodes) are centred over their children.
    """
    if node is None:
        return None
    kids = node.get("children") or []
    if sum(c is not None for c in kids) > 2:
        xs = [_place(c, depth + 1, counter, out) for c in kids]
        xs = [x for x in xs if x is not None]
        x = (xs[0] + xs[-1]) / 2
    else:
        _place(kids[0] if kids else None, depth + 1, counter, out)
        x = counter[0]
        counter[0] += 1
        for child in kids[1:]:
            _place(child, depth + 1, counter, out)
    out.append((node, x, depth))
    return x


@styled
def render_tree(frame, highlight=()):
    """Draw a binary or 2-3 tree.

    The ``node`` local is drawn as the current node. ``highlight`` is a set
    of keys to mark, such as a search target.
    """
    loc = frame["locals"]
    root = _find_tree(loc)
    cursor = _tree_cursor(loc)

    fig, panes = new_axes(1, (6.5, 4.6))
    fig.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)
    ax = panes[0]
    placed = []
    counter = [0]
    _place(root, 0, counter, placed)

    if not placed:
        ax.text(0.5, 0.5, "(empty tree)", ha="center", va="center",
                transform=ax.transAxes, color=MUTED, fontsize=11)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
    else:
        levels = 1 + max(depth for _, _, depth in placed)
        slots = max(counter[0], 1)
        labels = [";".join(str(k) for k in (n.get("keys") or [])) for n, _, _ in placed]
        noted = any(n.get("meta", {}).get("note") is not None for n, _, _ in placed)
        node_px, note_pt = _tree_sizes(ax, slots, levels, noted)
        node_pt = node_px * 72.0 / ax.figure.dpi

        for node, x, depth in placed:
            for child in node.get("children") or []:
                if child is None:
                    continue
                cx, cd = next(((px, pd) for n, px, pd in placed if n is child),
                              (None, None))
                if cx is not None:
                    ax.plot([x, cx], [-depth, -cd], color=EDGE_IDLE,
                            linewidth=1.2, zorder=1)
        for (node, x, depth), label in zip(placed, labels):
            keys = node.get("keys") or []
            marked = any(k in highlight for k in keys)
            face = node.get("meta", {}).get("color")
            if face is None:
                if cursor is not None and node.get("id") == cursor:
                    face = NODE_CURRENT
                elif marked:
                    face = NODE_OPEN
                else:
                    face = NODE_IDLE
            ax.scatter([x], [-depth], s=node_pt ** 2,
                       marker="o" if len(keys) < 2 else "s",
                       zorder=2, color=face,
                       edgecolors="#334155", linewidths=1.0)
            ax.text(x, -depth, label, ha="center", va="center", zorder=3,
                    fontsize=_label_pt(label, node_px, ax.figure.dpi),
                    fontweight="bold",
                    color="white" if face != NODE_IDLE else "#0f172a")
            note = node.get("meta", {}).get("note")
            if note is not None:
                # Offset in points so the note clears the node at any scale.
                ax.annotate(str(note), (x, -depth),
                            xytext=(0, node_pt / 2 + 1),
                            textcoords="offset points", ha="center",
                            va="bottom", fontsize=note_pt, color=MUTED,
                            zorder=3)
        # One slot per in-order position, one band per level.
        ax.set_xlim(-0.5, slots - 0.5)
        ax.set_ylim(-(levels - 1) - 0.5, 0.5 + (0.25 if noted else 0))

    ax.set_xticks([])
    ax.set_yticks([])
    ax.minorticks_off()
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(False)
    plt.close(fig)
    return fig


# Largest node diameter in pixels.
MAX_NODE_PX = 36


def _tree_sizes(ax, slots, levels, noted):
    """``(node diameter px, note font pt)`` that fit this tree."""
    fig = ax.figure
    pos = ax.get_position()
    width_px = pos.width * fig.get_figwidth() * fig.dpi
    height_px = pos.height * fig.get_figheight() * fig.dpi
    bands = levels + (0.25 if noted else 0)
    node_px = min(MAX_NODE_PX, 0.82 * width_px / slots,
                  (0.55 if noted else 0.65) * height_px / bands)
    return node_px, max(_label_pt("00", node_px, fig.dpi) * 0.8, 6.5)


def _label_pt(label, node_px, dpi):
    """Largest font size (pt) that fits ``label`` inside the node.

    Assumes a bold digit is about 0.62 em wide.
    """
    font_px = min(0.42 * node_px,
                  0.85 * node_px / (0.62 * max(len(label), 2)))
    return font_px * 72.0 / dpi


# --------------------------------------------------------------------------
# hash tables
# --------------------------------------------------------------------------


@styled
def render_buckets(frame):
    """Draw a hash table's ``buckets``.

    A list of lists is drawn as separate chaining, a flat list as linear
    probing.
    """
    loc = frame["locals"]
    buckets = loc.get("buckets")
    if not isinstance(buckets, list):
        raise ValueError("no `buckets` list in scope")

    chained = any(isinstance(b, list) for b in buckets)
    n = max(len(buckets), 1)
    probe = next((loc[k] for k in ("b", "idx", "slot")
                  if isinstance(loc.get(k), int)), None)

    # Fixed size per strategy so the figure does not resize mid-run.
    fig, panes = new_axes(
        1, (6.8, 3.8) if chained else (6.8, 1.8)
    )
    fig.subplots_adjust(left=0.02, right=0.98, top=0.94, bottom=0.04)
    ax = panes[0]
    ax.set_xlim(-0.6, n - 0.4)
    slot_w, cell_w = 0.84, 0.72

    def fit(text, width, base):
        """Font that keeps ``text`` inside a cell ``width`` data units wide."""
        return _fit_pt(ax, text, width / n, base)

    # One font size for the table, fitted to the longest entry.
    entries = [str(v) for b in buckets
               for v in (b if isinstance(b, list) else [b]) if v is not None]
    widest = max(entries + [f"+{len(entries)}"], key=len)
    slot_pt = fit(widest, slot_w, 8.5)
    cell_pt = fit(widest, cell_w, 8)

    for i, bucket in enumerate(buckets):
        hot = (probe == i)
        ax.add_patch(plt.Rectangle(
            (i - slot_w / 2, 0.1), slot_w, 0.7, zorder=2,
            facecolor=NODE_CURRENT if hot else NODE_IDLE,
            edgecolor="#334155", linewidth=0.9))
        # Index labels go above when chains hang below.
        ax.text(i, 0.88 if chained else -0.12, str(i), ha="center",
                va="bottom" if chained else "top",
                fontsize=fit(str(i), slot_w, 7.5), color=MUTED)

        if chained:
            items = bucket if isinstance(bucket, list) else []
            if len(items) > CHAIN_LANES:
                # Collapse the tail of a long chain into "+N".
                shown = [str(v) for v in items[:CHAIN_LANES - 1]]
                shown.append(f"+{len(items) - (CHAIN_LANES - 1)}")
            else:
                shown = [str(v) for v in items]
            for depth, text in enumerate(shown):
                y = -0.5 - depth * 0.62
                more = text.startswith("+") and depth == CHAIN_LANES - 1
                ax.add_patch(plt.Rectangle(
                    (i - cell_w / 2, y), cell_w, 0.5, zorder=2,
                    facecolor="white" if more else "#dbeafe",
                    edgecolor="#334155", linewidth=0.8,
                    linestyle=":" if more else "-"))
                ax.text(i, y + 0.25, text, ha="center", va="center",
                        fontsize=cell_pt, zorder=3,
                        color=MUTED if more else "#0f172a")
                top_y = 0.1 if depth == 0 else y + 0.62
                ax.plot([i, i], [top_y, y + 0.5], color=EDGE_IDLE,
                        linewidth=1.0, zorder=1)
        else:
            text = "" if bucket is None else str(bucket)
            ax.text(i, 0.45, text, ha="center", va="center",
                    fontsize=slot_pt, zorder=3,
                    color="white" if hot else "#0f172a")

    if chained:
        ax.set_ylim(-0.5 - 0.62 * (CHAIN_LANES - 1) - 0.12, 1.25)
    else:
        ax.set_ylim(-0.5, 0.95)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.minorticks_off()
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(False)
    plt.close(fig)
    return fig


def _fit_pt(ax, text, fraction, base):
    """Font size (pt), at most ``base``, fitting ``text`` in ``fraction`` of
    the axes width."""
    fig = ax.figure
    width_px = ax.get_position().width * fig.get_figwidth() * fig.dpi
    room_px = 0.9 * fraction * width_px
    need_em = 0.62 * max(len(text), 1)
    return min(base, room_px / need_em * 72.0 / fig.dpi)


# Renderer for each VIEW kind in algoviz.presets.
RENDERERS = {
    "array": render_array,
    "graph": render_graph,
    "tree": render_tree,
    "buckets": render_buckets,
}


def renderer_for(module, name):
    """The renderer for preset ``name`` of a presets ``module``."""
    from .presets import view

    return RENDERERS[view(module, name)]


def array_never_changed(frames, original):
    """Warn when a sort fills another list instead of reordering `A`.

    Fires only if `A` never changes and another list ends as a reordering of
    it, so read-only searches and already-sorted input do not trigger it.
    """
    baseline = list(original)
    for frame in frames:
        try:
            _, arr, _ = pick_arrays(frame["locals"])
        except ValueError:
            return None
        if arr != baseline:
            return None

    _, arr, scratch = pick_arrays(frames[-1]["locals"])
    if scratch is None:
        return None
    name, values = scratch
    if any(v is None for v in values):
        return None
    try:
        rearrangement = sorted(values) == sorted(arr) and values != arr
    except TypeError:
        return None
    if not rearrangement:
        return None
    return (
        f"`A` was never modified; you appear to be building `{name}` "
        f"instead. The animation follows `A`, so modify it in place (or "
        f"rename `{name}` to `A`)."
    )
