"""Run a generator-based algorithm and record its locals at every ``yield``.

An algorithm is a generator that mutates its input and yields at each step
worth showing. Each frame is a snapshot of the innermost active frame's
locals. No marimo import, so this runs in plain tests.
"""

from __future__ import annotations

import inspect
import random as _random
import textwrap
from typing import NamedTuple

MAX_FRAMES = 5000
DEFAULT_SEED = 0

_SCALARS = (bool, int, float, str, bytes, type(None))


class AlgorithmError(Exception):
    """A problem with the algorithm's source, worded for its author."""


class AlgorithmFailed(Exception):
    """The algorithm raised partway through; keeps the frames recorded so far."""

    def __init__(self, cause, frames):
        super().__init__(str(cause))
        self.cause = cause
        self.frames = frames


class _Opaque:
    """Marker for values that are not recorded, such as functions."""

    __slots__ = ()

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return "<opaque>"


OPAQUE = _Opaque()


def _simple(value) -> bool:
    """True for scalars and tuples of scalars."""
    if isinstance(value, _SCALARS):
        return True
    if isinstance(value, tuple):
        return all(_simple(v) for v in value)
    return False


def snapshot(value):
    """Copy ``value`` so later mutation does not change the recorded frame.

    Objects with a ``snapshot()`` method describe themselves (see
    :mod:`algoviz.structs`). Containers are copied element-wise; anything
    else that is not a scalar becomes :data:`OPAQUE`.
    """
    if hasattr(value, "snapshot") and callable(value.snapshot):
        return value.snapshot()
    if isinstance(value, list):
        return [snapshot(v) for v in value]
    if isinstance(value, tuple):
        return tuple(snapshot(v) for v in value)
    if isinstance(value, (set, frozenset)):
        return {v for v in value if _simple(v)}
    if isinstance(value, dict):
        return {k: snapshot(v) for k, v in value.items() if _simple(k)}
    if _simple(value):
        return value
    return OPAQUE


def frame_chain(gen):
    """Frames of a ``yield from`` delegation chain, outermost first."""
    chain = [gen.gi_frame]
    g = gen
    while True:
        nxt = getattr(g, "gi_yieldfrom", None)
        if nxt is None or getattr(nxt, "gi_frame", None) is None:
            break
        g = nxt
        chain.append(g.gi_frame)
    return chain


def record(gen):
    """Snapshot the innermost frame's locals, plus holders from outer frames.

    A recursive helper may only see a subtree, so objects in outer frames
    whose class sets ``is_holder`` (Tree, Graph) are added too, unless the
    inner frame already uses the name.
    """
    chain = frame_chain(gen)
    recorded = {}
    for name, value in chain[-1].f_locals.items():
        snap = snapshot(value)
        if snap is not OPAQUE:
            recorded[name] = snap
    for frame in reversed(chain[:-1]):
        for name, value in frame.f_locals.items():
            if name not in recorded and getattr(type(value), "is_holder", False):
                recorded[name] = snapshot(value)
    return recorded


def seed_everything(seed=DEFAULT_SEED):
    """Seed ``random`` and numpy so runs and graph layouts are repeatable."""
    if seed is None:
        return
    _random.seed(seed)
    try:
        import numpy as np
    except ImportError:
        return
    np.random.seed(seed)


def capture(source, entry="run", args=(), env=None, max_frames=MAX_FRAMES,
            seed=DEFAULT_SEED):
    """Execute ``source`` and record one frame per ``yield``.

    ``env`` provides names such as ``Graph`` or ``Tree`` to the source.
    ``seed=None`` leaves the RNGs unseeded.

    Returns ``(frames, truncated)``; each frame is
    ``{"locals": {name: snapshot}, "label": str | None}``.
    """
    seed_everything(seed)
    namespace = dict(env or {})
    try:
        exec(textwrap.dedent(source), namespace)  # noqa: S102
    except SyntaxError as exc:
        raise AlgorithmError(
            f"syntax error on line {exc.lineno}: {exc.msg}"
        ) from exc

    if entry not in namespace:
        raise AlgorithmError(f"define a function named `{entry}`")

    gen = namespace[entry](*args)
    if not inspect.isgenerator(gen):
        raise AlgorithmError(
            f"`{entry}` ran to completion instead of yielding, so there is "
            "nothing to animate. Add a bare `yield` at each point you want a "
            "frame, and mutate the input in place rather than returning a copy."
        )

    frames, truncated = [], False
    while True:
        try:
            label = next(gen)
        except StopIteration:
            break
        except Exception as exc:  # noqa: BLE001
            raise AlgorithmFailed(exc, frames) from exc
        if len(frames) >= max_frames:
            truncated = True
            break
        frames.append(
            {
                "locals": record(gen),
                "label": label if isinstance(label, str) else None,
            }
        )

    if not frames:
        # No yield was reached (e.g. sorting one element): show the arguments.
        try:
            bound = inspect.signature(namespace[entry]).bind(*args).arguments
        except TypeError:
            bound = {}
        frames.append({
            "locals": {k: s for k, s in
                       ((k, snapshot(v)) for k, v in bound.items())
                       if s is not OPAQUE},
            "label": "finished without reaching a yield",
        })
    return frames, truncated


class Run(NamedTuple):
    """Result of :func:`capture_safely`."""

    frames: list
    truncated: bool
    warning: str | None
    error: str | None


def capture_safely(source, entry="run", args=(), env=None, seed=DEFAULT_SEED,
                   diagnose=None, precondition=None):
    """:func:`capture`, returning errors in a :class:`Run` instead of raising.

    A truthy ``precondition`` is returned as the error without running.
    ``diagnose(frames, args)`` may return a warning string.
    """
    if precondition:
        return Run([], False, None, precondition)
    try:
        frames, truncated = capture(
            source, entry=entry, args=args, env=env, seed=seed
        )
    except AlgorithmError as exc:
        return Run([], False, None, str(exc))
    except AlgorithmFailed as exc:
        return Run(exc.frames, False, None, describe(exc.cause))
    except Exception as exc:  # noqa: BLE001
        return Run([], False, None, describe(exc))
    warning = None
    if diagnose is not None:
        try:
            warning = diagnose(frames, args)
        except Exception:  # noqa: BLE001
            warning = None
    return Run(frames, truncated, warning, None)


def describe(exc):
    """Format as ``"IndexError (line 12): list index out of range"``.

    The line is the deepest one inside the algorithm's source.
    """
    line = None
    tb = exc.__traceback__
    while tb is not None:
        if tb.tb_frame.f_code.co_filename == "<string>":
            line = tb.tb_lineno
        tb = tb.tb_next
    where = f" (line {line})" if line is not None else ""
    return f"{type(exc).__name__}{where}: {exc}"


def ints_in(frame, exclude=()):
    """Integer locals of a frame, excluding bools."""
    return {
        k: v
        for k, v in frame["locals"].items()
        if type(v) is int and k not in exclude
    }
