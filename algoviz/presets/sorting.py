"""Sorting presets, from ``pseudocode/sorting/``."""

from algoviz.loader import load

ENTRY = "sort"
ENV = {}
VIEW = "array"

PRESETS = {
    "selection": load("sorting/selection.py"),
    "insertion": load("sorting/insertion.py"),
    "merge": load("sorting/merge.py"),
    "quick": load("sorting/quick.py"),
    "heap": load("sorting/heap.py"),
}
