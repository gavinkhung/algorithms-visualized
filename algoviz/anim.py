"""Turn captured frames into an animated GIF.

Each frame is rendered to its own image, then the images are joined with
Pillow.
"""

from __future__ import annotations

import io

from PIL import Image

from . import draw

# Longer runs are sampled down to this many frames.
MAX_GIF_FRAMES = 120


def thin(frames, limit=MAX_GIF_FRAMES):
    """Evenly sample ``frames`` down to ``limit``, keeping the last frame."""
    total = len(frames)
    if total <= limit:
        return list(frames)
    step = total / float(limit)
    picked = [frames[int(i * step)] for i in range(limit)]
    if picked[-1] is not frames[-1]:
        picked[-1] = frames[-1]
    return picked


def to_gif(frames, path, kind="array", fps=6, limit=MAX_GIF_FRAMES,
           renderer=None):
    """Write ``frames`` to ``path`` as an animated GIF.

    ``kind`` picks the renderer unless ``renderer`` is given. Returns the
    number of frames written.
    """
    renderer = renderer or draw.RENDERERS[kind]
    data, count = gif_bytes(frames, renderer, fps, limit)
    with open(path, "wb") as fh:
        fh.write(data)
    return count


def gif_bytes(frames, renderer, fps=6, limit=MAX_GIF_FRAMES):
    """Return ``(gif_bytes, frame_count)``.

    ``renderer`` takes a frame and returns a matplotlib figure.
    """
    if not frames:
        raise ValueError("no frames to animate")
    picked = thin(frames, limit)

    images = []
    for frame in picked:
        fig = renderer(frame)
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=fig.dpi)
        buf.seek(0)
        images.append(Image.open(buf).convert("RGB"))

    # A run can change figure size (merge sort's scratch row appears with
    # its first merge), and a GIF needs one canvas: pad every frame to it.
    width = max(im.width for im in images)
    height = max(im.height for im in images)
    canvas = []
    for im in images:
        page = Image.new("RGB", (width, height), "white")
        page.paste(im, (0, 0))
        canvas.append(page)
    out = io.BytesIO()
    canvas[0].save(out, format="GIF", save_all=True,
                   append_images=canvas[1:], duration=int(1000 / fps), loop=0)
    return out.getvalue(), len(picked)
