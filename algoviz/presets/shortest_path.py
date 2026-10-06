"""Shortest path presets, from ``pseudocode/shortest_path/``."""

from algoviz.loader import load
from algoviz.presets import GRAPH_ENV

ENTRY = "run"
ENV = GRAPH_ENV
VIEW = "graph"

PRESETS = {
    "dijkstra": load("shortest_path/dijkstra.py"),
    "bellman-ford": load("shortest_path/bellman_ford.py"),
    "bfs (unweighted)": load("shortest_path/bfs_unweighted.py"),
}
