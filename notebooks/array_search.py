import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", css_file="../algoviz/notebook.css")


@app.cell
def _(algoviz, presets, set_step, ui):
    algo = ui.chooser(presets.PRESETS, "binary search", "algorithm", set_step)
    pattern = ui.chooser(algoviz.ARRAY_PATTERNS, "sorted", "input", set_step)
    size = ui.slider(4, 14, 12, "n", set_step)
    target = ui.number(7, "target v", set_step)
    return algo, pattern, size, target


@app.cell
def _(pattern, set_step, size, ui):
    array_field = ui.array_source(pattern, size, set_step)
    return (array_field,)


@app.cell
def _(algoviz, array_field):
    SAMPLE, input_error = algoviz.parse_array(array_field.value)
    return SAMPLE, input_error


@app.cell
def _(algo, presets, ui):
    editor = ui.editor(presets.PRESETS[algo.value])
    return (editor,)


@app.cell
def _(SAMPLE, algoviz, editor, input_error, presets, target):
    TARGET, target_error = algoviz.whole_number(target.value)
    run = algoviz.capture_safely(
        editor.value,
        entry=presets.ENTRY,
        args=(list(SAMPLE or []), TARGET),
        precondition=input_error or target_error,
    )
    return (run,)


@app.cell
def _(mo, ui):
    # The step counter, whether it is playing, and the buttons that move it.
    get_step, set_step = mo.state(0)
    get_playing, set_playing = mo.state(False)
    speed, steps = ui.playback_controls(set_step, get_playing, set_playing)
    return get_playing, get_step, set_playing, set_step, speed, steps


@app.cell
def _(get_playing, set_playing, steps, ui):
    # Re-runs when stepping pauses, so the switch shows as off.
    transport = ui.transport(get_playing, set_playing, steps)
    return (transport,)


@app.cell
def _(get_playing, get_step, run, set_step, speed, ui):
    # The only cell that reads `speed`; each tick re-runs it.
    ui.heartbeat(get_playing(), speed, run.frames, get_step, set_step)
    return


@app.cell
def _(
    algo,
    array_field,
    draw,
    editor,
    get_step,
    mo,
    pattern,
    presets,
    run,
    size,
    target,
    transport,
    ui,
):
    left = mo.vstack([
        algo,
        ui.controls(pattern, size, target),
        array_field,
        editor,
    ])
    right = ui.viewport(
        run, get_step(), draw.renderer_for(presets, algo.value),
        transport,
        name=algo.value,
    )
    ui.two_pane(left, right)
    return


@app.cell
def _():
    import marimo as mo

    import algoviz
    from algoviz import draw, ui
    from algoviz.presets import array_search as presets

    return algoviz, draw, mo, presets, ui


if __name__ == "__main__":
    app.run()
