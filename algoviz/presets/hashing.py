"""Hash table presets, from ``pseudocode/hashing/``."""

from algoviz.loader import load

ENTRY = "run"
ENV = {}
VIEW = "buckets"

PRESETS = {
    "separate chaining": load("hashing/separate_chaining.py"),
    "linear probing": load("hashing/linear_probing.py"),
    "linear probing + delete": load("hashing/linear_probing_delete.py"),
}
