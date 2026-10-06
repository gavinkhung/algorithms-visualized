#!/usr/bin/env python3
"""Render every preset to an animated GIF for the book's landing page.

    python3 utils/make_gifs.py                 # all of them
    python3 utils/make_gifs.py sorting hashing # just those topics

Writes ``book/gifs/<topic>_<preset>.gif``.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import algoviz  # noqa: E402
import algoviz.anim as anim  # noqa: E402
from algoviz.presets import (  # noqa: E402
    array_search,
    hashing,
    mst,
    runnable,
    shortest_path,
    sorting,
    traversal,
    tree_insert,
    tree_search,
    view,
)

# Small inputs: the GIFs are shown as thumbnails.
ARRAY_N = 10
GRAPH_N = 7
TREE_N = 7


def graph_args(shape="sparse", n=GRAPH_N):
    nodes, edges, directed = algoviz.make_graph(shape, n)
    graph = algoviz.Graph(nodes, edges, directed=directed)
    return (graph, nodes[0])


def array_args(pattern="random", n=ARRAY_N):
    return (algoviz.make_array(pattern, n),)


def topics():
    """topic -> (preset module, function from preset name to its args)."""
    values = algoviz.make_array("random", TREE_N)
    return {
        "sorting": (
            sorting,
            lambda name: array_args(),
        ),
        "array_search": (
            array_search,
            lambda name: (
                algoviz.make_array(
                    "sorted" if "binary" in name else "random", ARRAY_N
                ),
                0 if "quickselect" in name else 7,
            ),
        ),
        "hashing": (
            hashing,
            lambda name: (algoviz.make_array("random", 8), 7, 7),
        ),
        "tree_search": (
            tree_search,
            lambda name: (
                (algoviz.heap_from(list(values)), 7)
                if "heap" in name
                else (algoviz.bst_from(list(values)), values[len(values) // 2])
            ),
        ),
        "tree_insert": (
            tree_insert,
            lambda name: (algoviz.Tree(), list(values)),
        ),
        "traversal": (
            traversal,
            lambda name: graph_args("dag" if "topo" in name or "cycle" in name
                                    else "sparse"),
        ),
        "shortest_path": (
            shortest_path,
            lambda name: graph_args("dag (negative)" if "bellman" in name
                                    else "sparse"),
        ),
        "mst": (
            mst,
            lambda name: graph_args("sparse"),
        ),
    }


def slug(name):
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def build(topic, out_dir, only=None):
    module, args_for = topics()[topic]
    written = []
    for name, source in module.PRESETS.items():
        if only and slug(name) not in only:
            continue
        target = out_dir / f"{topic}_{slug(name)}.gif"
        args = args_for(name)
        frames, _, _, error = algoviz.capture_safely(
            runnable(module, source),
            entry=module.ENTRY,
            args=args,
            env=module.ENV,
        )
        if error:
            print(f"  SKIP {topic}/{name}: {error}")
            continue
        try:
            count = anim.to_gif(frames, target, kind=view(module, name))
        except Exception as exc:  # noqa: BLE001
            print(f"  FAIL {topic}/{name}: {type(exc).__name__}: {exc}")
            continue
        size = target.stat().st_size
        print(f"  {target.name}  ({count} frames, {size // 1024} KB)")
        written.append(target)
    return written


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topics", nargs="*", default=None,
                        help="topics to build; default is all")
    parser.add_argument("-o", "--output", type=Path,
                        default=ROOT / "book" / "gifs")
    parser.add_argument("--only", nargs="*", default=None,
                        help="slugified preset names to restrict to")
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    chosen = args.topics or list(topics())
    total = 0
    for topic in chosen:
        if topic not in topics():
            raise SystemExit(
                f"unknown topic {topic!r}; choose from {', '.join(topics())}"
            )
        print(f"--- {topic} ---")
        total += len(build(topic, args.output, args.only))
    print(f"\nwrote {total} gifs into {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
