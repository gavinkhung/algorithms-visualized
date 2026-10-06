"""Every sorting algorithm runs, sorts, and its last step draws."""

import algoviz
from algoviz import draw
from algoviz.presets import sorting as presets


def test_sorting_presets_sort_and_draw():
    for name, source in presets.PRESETS.items():
        run = algoviz.capture_safely(source, entry=presets.ENTRY, args=([3, 1, 2],))
        assert run.error is None, f"{name}: {run.error}"
        last = run.frames[-1]
        assert last["locals"]["A"] == [1, 2, 3], name
        draw.renderer_for(presets, name)(last)
