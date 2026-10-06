"""Array search presets, from ``pseudocode/array_search/``."""

from algoviz.loader import load

ENTRY = "run"
ENV = {}
VIEW = "array"

PRESETS = {
    "binary search": load("array_search/binary_search.py"),
    "quickselect": load("array_search/quickselect.py"),
    "linear scan": load("array_search/linear_scan.py"),
}
