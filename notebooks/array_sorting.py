import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", css_file="../algoviz/notebook.css")


@app.cell
def _(algoviz, presets, set_step, ui):
    algo = ui.chooser(
        presets.PRESETS, "selection", "algorithm", set_step
    )
    pattern = ui.chooser(algoviz.ARRAY_PATTERNS, "random", "input", set_step)
    size = ui.slider(4, 11, 10, "n", set_step)
    return algo, pattern, size


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
    # Changing the algorithm reloads the preset and discards edits.
    editor = ui.editor(presets.PRESETS[algo.value])
    return (editor,)


@app.cell
def _(SAMPLE, algoviz, draw, editor, input_error, presets):
    run = algoviz.capture_safely(
        editor.value,
        entry=presets.ENTRY,
        args=(list(SAMPLE or []),),
        diagnose=lambda fr, args: draw.array_never_changed(fr, args[0]),
        precondition=input_error,
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
    algo,
    algoviz,
    array_field,
    draw,
    editor,
    get_step,
    mo,
    pattern,
    presets,
    run,
    size,
    transport,
    ui,
):
    left = mo.vstack([
        algo,
        ui.controls(pattern, size),
        array_field,
        editor,
    ])

    # Shows the array at the current step. Writing it back into the input
    # field would make a dependency cycle.
    def echo(frame):
        live = frame["locals"].get("A")
        if live is None:
            return None
        return mo.md(f"`A = [{algoviz.format_array(live)}]`")

    right = ui.viewport(
        run, get_step(), draw.renderer_for(presets, algo.value),
        transport,
        name=algo.value,
        extra=echo,
    )
    ui.two_pane(left, right)
    return


@app.cell
def _():
    import marimo as mo

    import algoviz
    # Imported by name: after an auto-reload, `algoviz.ui` may not be set.
    from algoviz import draw, ui
    from algoviz.presets import sorting as presets

    return algoviz, draw, mo, presets, ui


if __name__ == "__main__":
    app.run()
