"""Tree insertion presets, from ``pseudocode/tree_insert/``."""

from algoviz.loader import load, wrap_tree_insert
from algoviz.presets import TREE_ENV

ENTRY = "run"
ENV = TREE_ENV
VIEW = "tree"

# Each preset inserts one value; the driver loops over the list.
driver = wrap_tree_insert

PRESETS = {
    "bst insert": load("tree_insert/bst.py"),
    "avl insert": load("tree_insert/avl.py"),
    "2-3 insert": load("tree_insert/two_three.py"),
}
