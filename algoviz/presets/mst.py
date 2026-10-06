"""Minimum spanning tree presets, from ``pseudocode/mst/``."""

from algoviz.loader import load
from algoviz.presets import GRAPH_ENV

ENTRY = "run"
ENV = GRAPH_ENV
VIEW = "graph"

PRESETS = {
    "prim": load("mst/prim.py"),
    "kruskal": load("mst/kruskal.py"),
    "worst-case spanning tree": load("mst/maximum.py"),
}
