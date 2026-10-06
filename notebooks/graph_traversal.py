import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", css_file="../algoviz/notebook.css")


@app.cell
def _(algoviz, mo, presets, set_step, ui):
    algo = ui.chooser(presets.PRESETS, "dfs", "algorithm", set_step)
    shape = ui.chooser(algoviz.GRAPH_SHAPES, "sparse", "shape", set_step)
    size = ui.slider(3, algoviz.MAX_NODES, 9, "n", set_step)
    start = mo.ui.text(value="A", label="start",
                       on_change=lambda _: set_step(0))
    return algo, shape, size, start


@app.cell
def _(set_step, shape, size, ui):
    adjacency, DIRECTED = ui.graph_source(shape, size, set_step)
    return DIRECTED, adjacency


@app.cell
def _(DIRECTED, adjacency, algoviz, start):
    GRAPH, START, graph_error = algoviz.graph_from_text(
        adjacency.value, directed=DIRECTED, start=start.value
    )
    return GRAPH, START, graph_error


@app.cell
def _(algo, presets, ui):
    editor = ui.editor(presets.PRESETS[algo.value])
    return (editor,)


@app.cell
def _(GRAPH, START, algoviz, editor, graph_error, presets):
    run = algoviz.capture_safely(
        editor.value,
        entry=presets.ENTRY,
        # A copy, because Kahn's algorithm removes edges.
        args=() if graph_error else (GRAPH.copy(), START),
        env=presets.ENV,
        precondition=graph_error,
    )
    return (run,)


@app.cell
def _(mo, ui):
    # The step counter and the buttons that move it.
    get_step, set_step = mo.state(0)
    play, speed, transport = ui.playback_controls(set_step)
    return get_step, play, set_step, speed, transport


@app.cell
def _(get_step, play, run, set_step, speed, ui):
    # The only cell that reads `speed`; each tick re-runs it.
    ui.heartbeat(play, speed, run.frames, get_step, set_step)
    return


@app.cell
def _(
    adjacency,
    algo,
    draw,
    editor,
    get_step,
    mo,
    presets,
    run,
    shape,
    size,
    start,
    transport,
    ui,
):
    left = mo.vstack([
        algo,
        ui.controls(shape, size, start),
        adjacency,
        editor,
    ])
    right = ui.viewport(
        run, get_step(), draw.renderer_for(presets, algo.value),
        transport,
        name=algo.value,
        extra=lambda f: ui.ordered_list(
            f["locals"].get("ordering"), label="visit order"
        ),
    )
    ui.two_pane(left, right)
    return


@app.cell
def _():
    import marimo as mo

    import algoviz
    from algoviz import draw, ui
    from algoviz.presets import traversal as presets

    return algoviz, draw, mo, presets, ui


if __name__ == "__main__":
    app.run()
