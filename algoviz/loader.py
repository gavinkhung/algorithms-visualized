"""Load algorithm source files from ``pseudocode/``.

In the browser build, ``utils/bundle_wasm.py`` places ``pseudocode/`` beside
``algoviz/``, so the same paths work there.
"""

from __future__ import annotations

from pathlib import Path

_CACHE: dict[str, str] = {}


def _root() -> Path:
    return Path(__file__).resolve().parent.parent


def load(*parts: str) -> str:
    """Read ``pseudocode/<parts>.py`` and return the source text."""
    key = "/".join(parts)
    if not key.endswith(".py"):
        key = key + ".py"
    if key not in _CACHE:
        path = _root() / "pseudocode" / key
        if not path.is_file():
            raise FileNotFoundError(path)
        _CACHE[key] = path.read_text()
    return _CACHE[key]


def wrap_tree_insert(source: str) -> str:
    """Wrap a single-value ``run(tree, v)`` as ``run(tree, values)``."""
    return source + """

_insert_one = run


def run(tree, values):
    for v in values:
        yield from _insert_one(tree, v)
"""
