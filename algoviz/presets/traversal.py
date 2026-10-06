"""Graph traversal presets, from ``pseudocode/traversal/``."""

from algoviz.loader import load
from algoviz.presets import GRAPH_ENV

ENTRY = "run"
ENV = GRAPH_ENV
VIEW = "graph"

PRESETS = {
    "dfs": load("traversal/dfs.py"),
    "bfs": load("traversal/bfs.py"),
    "toposort (Kahn)": load("traversal/toposort_kahn.py"),
    "cycle check (DFS)": load("traversal/cycle_check.py"),
}
