"""Shared code for the algorithm visualizer notebooks.

``capture``  run a generator-based algorithm, recording locals at each yield
``draw``     matplotlib renderers, one per shape of data
``structs``  Graph, Tree and Node
``ui``       marimo widgets and layout
``inputs``   sample inputs and input parsing
``presets``  per-notebook algorithms and how to run and draw them
``loader``   reads algorithm files from ``pseudocode/``
``anim``     frames to GIF

An algorithm is a generator function that mutates its input and yields at
each step to show.
"""

# `draw` (matplotlib), `ui` (marimo) and the presets are imported explicitly
# by the notebooks, so the rest can be imported without them.
from .capture import AlgorithmError, Run, capture, capture_safely, ints_in
from .inputs import (
    ARRAY_PATTERNS,
    GRAPH_SHAPES,
    MAX_NODES,
    format_adjacency,
    format_array,
    make_array,
    make_graph,
    parse_adjacency,
    parse_array,
    whole_number,
)
from .structs import (
    Edge,
    Graph,
    Node,
    Tree,
    bst_from,
    graph_from_text,
    heap_from,
)

__all__ = [
    "ARRAY_PATTERNS",
    "GRAPH_SHAPES",
    "MAX_NODES",
    "AlgorithmError",
    "Edge",
    "Graph",
    "Node",
    "Run",
    "Tree",
    "bst_from",
    "capture",
    "capture_safely",
    "format_adjacency",
    "format_array",
    "graph_from_text",
    "heap_from",
    "ints_in",
    "make_array",
    "make_graph",
    "parse_adjacency",
    "parse_array",
    "whole_number",
]
