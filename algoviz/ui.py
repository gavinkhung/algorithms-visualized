"""marimo widgets and layout shared by the notebooks.

The only module in the package that imports marimo.
"""

from __future__ import annotations

import html
import io
import re

import marimo as mo
from matplotlib.figure import Figure

from .capture import ints_in
from .draw import color_for

SPEEDS = ["0.1s", "0.25s", "0.5s", "1s"]


def playback_controls(set_step, speeds=SPEEDS, default="0.25s"):
    """Return ``play, speed, transport``.

    ``play`` and ``speed`` must be bound to notebook variables because other
    cells read them. ``transport`` is the row of step controls; it holds the
    buttons, which keeps them alive.
    """
    play = mo.ui.switch(label="auto-play")
    restart = mo.ui.button(label="restart", on_change=lambda _: set_step(0))
    prev = mo.ui.button(
        label="< step", on_change=lambda _: set_step(lambda v: max(v - 1, 0))
    )
    nxt = mo.ui.button(
        label="step >", on_change=lambda _: set_step(lambda v: v + 1)
    )
    speed = mo.ui.refresh(
        options=speeds, default_interval=default, label="speed"
    )
    transport = mo.hstack([play, restart, prev, nxt], justify="start", gap=1)
    return play, speed, transport


def heartbeat(play, speed, frames, get_step, set_step):
    """Advance one frame per tick while playing; return the timer widget.

    Call this from its own cell, the only one that reads ``speed``; every
    tick re-runs the cells that read it. The step is only set when it
    changes, because marimo's setter always triggers an update.
    A step past the last frame is clamped back.
    """
    if frames:
        current, last = get_step(), len(frames) - 1
        if current > last:
            set_step(last)
        elif play.value and current < last:
            set_step(current + 1)
    return speed


def variables(ints):
    """Integer locals as one line, coloured like their pointers."""
    return " &nbsp; ".join(
        f"<b style='color:{color_for(k)}'>{k}</b>={v}" for k, v in ints.items()
    )


def _fixed_png(figure, alt):
    """``(image, png_bytes)`` for a figure saved at its full canvas size.

    Not cropped to its contents, so every frame of a run has the same size.
    """
    if not isinstance(figure, Figure):
        return figure, None
    buf = io.BytesIO()
    figure.savefig(buf, format="png", bbox_inches=None, dpi=figure.dpi)
    data = buf.getvalue()
    return mo.image(
        io.BytesIO(data),
        alt=alt,
        width="100%",
        style={"display": "block", "max-width": "100%", "height": "auto"},
    ), data


# Most frames in a downloaded GIF; longer runs are sampled. The notebooks'
# size controls stay within it (tests/test_frame_budget.py).
DOWNLOAD_GIF_FRAMES = 80


def downloads(png, frames, renderer, step, name):
    """"Download frame (PNG)" and "Download animation (GIF)" buttons.

    The GIF is built when its button is clicked.
    """
    from .anim import gif_bytes

    slug = re.sub(r"[^a-z0-9]+", "-", str(name).lower()).strip("-") or "visualization"
    buttons = []
    if png is not None:
        buttons.append(mo.download(
            data=png, filename=f"{slug}-step-{step}.png",
            mimetype="image/png", label="Download frame (PNG)"))
    buttons.append(mo.download(
        data=lambda: gif_bytes(frames, renderer, limit=DOWNLOAD_GIF_FRAMES)[0],
        filename=f"{slug}.gif",
        mimetype="image/gif", label="Download animation (GIF)"))
    return mo.hstack(buttons, justify="start", wrap=True, gap=1)


def stage(controls, figure, step, total, label=None, ints=None,
          truncated=False, warning=None, extra=None, error=None,
          frames=None, renderer=None, name="visualization"):
    """Right-hand pane: controls, figure, step counter, readout, warnings.

    ``label`` is HTML-escaped and shown as typed.
    """
    suffix = " _(truncated)_" if truncated else ""
    caption = f"<b>{html.escape(label)}</b> &nbsp;&nbsp; " if label else ""
    image, png = _fixed_png(figure, html.escape(
        f"Step {step} of {total}" + (f": {label}" if label else "")))
    panel = [
        controls,
        image,
        mo.md(f"**Step {step} / {total}**{suffix}"),
        # Wrapped in one <p> so the readout stays on one line.
        mo.Html(f"<p style='margin:0'>{caption}{variables(ints or {})}</p>"),
    ]
    if extra is not None:
        panel.append(extra)
    if frames:
        panel.append(downloads(png, frames, renderer, step, name))
    if error:
        panel.append(mo.callout(
            mo.vstack([
                mo.md(f"**Your code stopped after step {total}.** The last "
                      "frame shows the state just before."),
                _message(error),
            ]),
            kind="danger",
        ))
    if warning:
        panel.append(mo.callout(mo.md(warning), kind="warn"))
    return mo.vstack(panel).style({"overflow": "hidden"})


def _message(text):
    """An error message, monospaced and wrapping."""
    return mo.Html(
        "<pre style='white-space:pre-wrap;overflow-wrap:anywhere;margin:0'>"
        f"{html.escape(text)}</pre>"
    )


def error_panel(message):
    return mo.vstack([mo.md("**Couldn't run your code:**"), _message(message)])


def controls(*items):
    """A row of inputs that wraps in a narrow pane."""
    return mo.hstack(list(items), justify="start", wrap=True, gap=1)


def two_pane(left, right):
    """Controls beside the figure; stacked when the page is narrow."""
    pane = {"flex": "1 1 340px", "min-width": "0"}
    return mo.hstack(
        [mo.as_html(left).style(pane), mo.as_html(right).style(pane)],
        wrap=True, gap=2, align="start",
    )


def editor(source, label="Edit the algorithm"):
    return mo.ui.code_editor(
        value=source.strip() + "\n", language="python", label=label
    )


def chooser(options, value, label, set_step):
    """A dropdown that rewinds playback whenever the selection changes."""
    return mo.ui.dropdown(
        options=list(options),
        value=value,
        label=label,
        on_change=lambda _: set_step(0),
    )


def slider(start, stop, value, label, set_step):
    return mo.ui.slider(start, stop, value=value, label=label,
                        on_change=lambda _: set_step(0))


def number(value, label, set_step, start=-999, stop=999):
    """A whole-number box; read it through :func:`algoviz.whole_number`."""
    return mo.ui.number(value=value, start=start, stop=stop, step=1,
                        label=label, on_change=lambda _: set_step(0))


def array_source(pattern, size, set_step, label="array"):
    """Editable array, filled from the pattern and size controls.

    Build it in a cell that reads ``pattern`` and ``size`` so changing them
    replaces the text.
    """
    from .inputs import format_array, make_array

    return mo.ui.text(
        value=format_array(make_array(pattern.value, size.value)),
        label=label,
        full_width=True,
        on_change=lambda _: set_step(0),
    )


def ordered_list(items, label="output", arrow=" &rarr; "):
    """A sequence in the order it was produced, such as a visit order."""
    items = list(items or [])
    if not items:
        return mo.md(f"**{label}:** _(empty)_")
    body = arrow.join(f"`{item}`" for item in items)
    return mo.md(f"**{label}** ({len(items)}): {body}")


def mapping(pairs, label="dist", missing="&infin;"):
    """A node-to-value table on one line, showing infinity as ∞."""
    pairs = pairs or {}
    if not pairs:
        return mo.md(f"**{label}:** _(empty)_")
    cells = []
    for key in sorted(pairs, key=str):
        value = pairs[key]
        if value == float("inf"):
            shown = missing
        elif isinstance(value, float) and value.is_integer():
            shown = str(int(value))
        else:
            shown = str(value)
        cells.append(f"`{key}`={shown}")
    return mo.md(f"**{label}:** " + " &nbsp; ".join(cells))


def graph_source(shape, size, set_step, label="adjacency list", rows=9):
    """Editable adjacency list, filled from the shape and size controls.

    Returns ``(field, directed)``; the shape decides whether it is directed.
    """
    from .inputs import format_adjacency, make_graph

    nodes, edges, directed = make_graph(shape.value, size.value)
    field = mo.ui.text_area(
        value=format_adjacency(nodes, edges, directed),
        label=label,
        rows=rows,
        full_width=True,
        on_change=lambda _: set_step(0),
    )
    return field, directed


def viewport(run, step, renderer, transport, name, extra=None,
             ints=ints_in):
    """The right-hand pane: an error, or the current frame and its controls.

    ``run`` comes from ``capture_safely``. ``renderer``, ``ints`` and
    ``extra`` take the current frame. ``name`` names the downloaded files.
    """
    frames = run.frames
    if run.error and not frames:
        return error_panel(run.error)
    if not frames:
        return mo.md("_No frames captured._")
    idx = min(max(step, 0), len(frames) - 1)
    frame = frames[idx]
    try:
        figure = renderer(frame)
    except Exception as exc:  # noqa: BLE001
        return error_panel(f"Nothing to draw at step {idx + 1}: {exc}")
    return stage(
        transport,
        figure,
        idx + 1,
        len(frames),
        label=frame["label"],
        ints=ints(frame) if ints else None,
        truncated=run.truncated,
        warning=run.warning,
        extra=extra(frame) if extra else None,
        error=run.error,
        frames=frames,
        renderer=renderer,
        name=name,
    )
