"""Algorithm presets, one module per notebook.

Used by the notebooks and utils/make_gifs.py. Each module defines:

``PRESETS``  display name -> source, from files under ``pseudocode/``
``ENTRY``    the function to call
``ENV``      helper types the source expects in scope (``Node``, ``Graph``...)
``VIEW``     renderer kind (see ``draw.RENDERERS``): one for the module, or a
             dict per preset name
``driver``   optional: wraps a preset's source before it runs
"""

from algoviz.structs import Edge, Graph, Node, Tree

TREE_ENV = {"Node": Node, "Tree": Tree}
GRAPH_ENV = {"Graph": Graph, "Edge": Edge}


def view(module, name):
    """Renderer kind for preset ``name`` of ``module``."""
    return module.VIEW if isinstance(module.VIEW, str) else module.VIEW[name]


def runnable(module, source):
    """``source`` ready to capture: through the module's driver, if any."""
    driver = getattr(module, "driver", None)
    return driver(source) if driver else source
