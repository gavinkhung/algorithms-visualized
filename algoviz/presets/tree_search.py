"""Tree search presets, from ``pseudocode/tree_search/``."""

from algoviz.loader import load
from algoviz.presets import TREE_ENV

ENTRY = "run"
ENV = TREE_ENV

VIEW = {
    "bst search": "tree",
    "splay search": "tree",
    "heap search (array)": "array",
}

PRESETS = {
    "bst search": load("tree_search/bst.py"),
    "splay search": load("tree_search/splay.py"),
    "heap search (array)": load("tree_search/heap.py"),
}
