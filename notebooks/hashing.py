import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", css_file="../algoviz/notebook.css")


@app.cell
def _(algoviz, presets, set_step, ui):
    algo = ui.chooser(presets.PRESETS, "separate chaining", "strategy", set_step)
    pattern = ui.chooser(algoviz.ARRAY_PATTERNS, "random", "input", set_step)
    size = ui.slider(3, 24, 10, "items", set_step)
    buckets = ui.slider(2, 24, 7, "buckets", set_step)
    target = ui.number(7, "search v", set_step)
    return algo, buckets, pattern, size, target


@app.cell
def _(pattern, set_step, size, ui):
    array_field = ui.array_source(pattern, size, set_step, label="values")
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
def _(SAMPLE, algo, buckets, input_error):
    # Linear probing needs a slot per distinct value.
    if input_error:
        table_error = input_error
    elif any(not isinstance(x, int) for x in SAMPLE):
        table_error = "The hash function is `value % buckets`: use integers."
    elif "probing" in algo.value and len(set(SAMPLE)) > buckets.value:
        table_error = (
            f"Linear probing needs at least as many buckets as items: "
            f"{len(set(SAMPLE))} distinct items into {buckets.value} buckets "
            f"cannot fit."
        )
    else:
        table_error = None
    load = (len(SAMPLE or []) / buckets.value) if buckets.value else 0
    return load, table_error


@app.cell
def _(SAMPLE, algoviz, buckets, editor, presets, table_error, target):
    TARGET, target_error = algoviz.whole_number(target.value)
    run = algoviz.capture_safely(
        editor.value,
        entry=presets.ENTRY,
        args=(list(SAMPLE or []), TARGET, int(buckets.value)),
        precondition=table_error or target_error,
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
    array_field,
    buckets,
    draw,
    editor,
    get_step,
    load,
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
        ui.controls(pattern, size, buckets, target),
        array_field,
        editor,
    ])
    right = ui.viewport(
        run, get_step(), draw.renderer_for(presets, algo.value),
        transport,
        name=algo.value,
        extra=lambda _f: mo.md(f"load factor **{load:.2f}**"),
    )
    ui.two_pane(left, right)
    return


@app.cell
def _():
    import marimo as mo

    import algoviz
    from algoviz import draw, ui
    from algoviz.presets import hashing as presets

    return algoviz, draw, mo, presets, ui


if __name__ == "__main__":
    app.run()
