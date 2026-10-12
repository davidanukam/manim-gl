"""Line icons sized with ``height``. Every icon is drawn in a unit box, then scaled."""

import numpy as np
from manimlib import (
    Arc,
    Circle,
    DOWN,
    Ellipse,
    LEFT,
    Line,
    PI,
    Polygon,
    RIGHT,
    RoundedRectangle,
    Square,
    Triangle,
    UP,
    VGroup,
    VMobject,
)

from .theme import WHITE


def _line(a, b, color, width):
    return Line(
        np.array([a[0], a[1], 0]),
        np.array([b[0], b[1], 0]),
        stroke_color=color,
        stroke_width=width,
    )


def _style_stroke(mob, color, width):
    mob.set_stroke(color, width=width)
    mob.set_fill(opacity=0)
    return mob


def _database(color, width):
    top = Ellipse(
        width=0.78, height=0.24, stroke_color=color, stroke_width=width, fill_opacity=0
    )
    top.shift(UP * 0.28)
    bottom = Ellipse(
        width=0.78, height=0.24, stroke_color=color, stroke_width=width, fill_opacity=0
    )
    bottom.shift(DOWN * 0.28)
    left = _line(top.get_left(), bottom.get_left(), color, width)
    right = _line(top.get_right(), bottom.get_right(), color, width)
    return VGroup(bottom, left, right, top)


def _lock(color, width):
    body = RoundedRectangle(
        width=0.62,
        height=0.46,
        corner_radius=0.08,
        stroke_color=color,
        stroke_width=width,
        fill_opacity=0,
    ).shift(DOWN * 0.16)
    shackle = Arc(
        radius=0.18, start_angle=0, angle=PI, stroke_color=color, stroke_width=width
    )
    shackle.shift(UP * 0.08)
    return VGroup(body, shackle)


def _server(color, width):
    body = RoundedRectangle(
        width=0.78,
        height=0.9,
        corner_radius=0.08,
        stroke_color=color,
        stroke_width=width,
        fill_opacity=0,
    )
    lines = VGroup()
    for y in (0.22, 0.0, -0.22):
        lines.add(_line((-0.22, y), (0.28, y), color, width))
        dot = Circle(radius=0.035, stroke_width=0, fill_color=color, fill_opacity=1)
        dot.move_to([-0.28, y, 0])
        lines.add(dot)
    return VGroup(body, lines)


def _cloud(color, width):
    cloud = VMobject()
    cloud.set_points_smoothly(
        [
            [-0.48, -0.12, 0],
            [-0.36, 0.16, 0],
            [-0.12, 0.02, 0],
            [0.02, 0.32, 0],
            [0.28, 0.1, 0],
            [0.48, 0.16, 0],
            [0.5, -0.1, 0],
            [0.22, -0.24, 0],
            [-0.18, -0.24, 0],
            [-0.48, -0.12, 0],
        ]
    )
    return _style_stroke(cloud, color, width)


def _check(color, width):
    return VGroup(
        _line((-0.28, 0.0), (-0.08, -0.22), color, width + 0.6),
        _line((-0.08, -0.22), (0.34, 0.26), color, width + 0.6),
    )


def _cross(color, width):
    return VGroup(
        _line((-0.24, -0.24), (0.24, 0.24), color, width),
        _line((-0.24, 0.24), (0.24, -0.24), color, width),
    )


def _ban(color, width):
    ring = Circle(radius=0.4, stroke_color=color, stroke_width=width, fill_opacity=0)
    return VGroup(ring, _line((-0.26, -0.26), (0.26, 0.26), color, width))


def _plus(color, width):
    return VGroup(
        _line((-0.28, 0), (0.28, 0), color, width),
        _line((0, -0.28), (0, 0.28), color, width),
    )


def _minus(color, width):
    return _line((-0.28, 0), (0.28, 0), color, width)


def _key(color, width):
    head = Circle(
        radius=0.16, stroke_color=color, stroke_width=width, fill_opacity=0
    ).shift(LEFT * 0.18)
    shaft = _line((0.0, 0.0), (0.4, 0.0), color, width)
    tooth = _line((0.28, 0.0), (0.28, -0.14), color, width)
    tooth2 = _line((0.4, 0.0), (0.4, -0.14), color, width)
    return VGroup(head, shaft, tooth, tooth2)


def _shield(color, width):
    shape = Polygon(
        [0, 0.42, 0],
        [0.36, 0.24, 0],
        [0.32, -0.12, 0],
        [0, -0.42, 0],
        [-0.32, -0.12, 0],
        [-0.36, 0.24, 0],
        stroke_color=color,
        stroke_width=width,
        fill_opacity=0,
    )
    return shape


def _user(color, width):
    head = Circle(
        radius=0.16, stroke_color=color, stroke_width=width, fill_opacity=0
    ).shift(UP * 0.2)
    shoulders = Arc(
        radius=0.28, start_angle=PI, angle=PI, stroke_color=color, stroke_width=width
    )
    shoulders.shift(DOWN * 0.18)
    return VGroup(head, shoulders)


def _document(color, width):
    page = RoundedRectangle(
        width=0.62,
        height=0.84,
        corner_radius=0.06,
        stroke_color=color,
        stroke_width=width,
        fill_opacity=0,
    )
    lines = VGroup(
        *[_line((-0.18, y), (0.18, y), color, width * 0.8) for y in (0.16, 0.0, -0.16)]
    )
    return VGroup(page, lines)


def _branch(color, width):
    a = Circle(radius=0.07, stroke_width=0, fill_color=color, fill_opacity=1).shift(
        LEFT * 0.22 + DOWN * 0.2
    )
    b = Circle(radius=0.07, stroke_width=0, fill_color=color, fill_opacity=1).shift(
        RIGHT * 0.22 + DOWN * 0.2
    )
    c = Circle(radius=0.07, stroke_width=0, fill_color=color, fill_opacity=1).shift(
        UP * 0.24
    )
    stem = _line((0, 0.16), (0, -0.05), color, width)
    arm = _line((-0.22, -0.05), (0.22, -0.05), color, width)
    left = _line((-0.22, -0.05), (-0.22, -0.12), color, width)
    right = _line((0.22, -0.05), (0.22, -0.12), color, width)
    return VGroup(stem, arm, left, right, a, b, c)


def _pin(color, width):
    head = Circle(radius=0.16, stroke_width=0, fill_color=color, fill_opacity=1).shift(
        UP * 0.16
    )
    needle = Polygon(
        [-0.14, 0.08, 0],
        [0.14, 0.08, 0],
        [0.0, -0.4, 0],
        stroke_width=0,
        fill_color=color,
        fill_opacity=1,
    )
    return VGroup(needle, head)


def _globe(color, width):
    ring = Circle(radius=0.4, stroke_color=color, stroke_width=width, fill_opacity=0)
    meridians = Ellipse(
        width=0.28, height=0.8, stroke_color=color, stroke_width=width, fill_opacity=0
    )
    equator = Ellipse(
        width=0.8, height=0.22, stroke_color=color, stroke_width=width, fill_opacity=0
    )
    return VGroup(ring, meridians, equator)


def _cpu(color, width):
    body = Square(
        side_length=0.5, stroke_color=color, stroke_width=width, fill_opacity=0
    )
    pins = VGroup()
    for x in (-0.16, 0.0, 0.16):
        pins.add(_line((x, 0.25), (x, 0.38), color, width))
        pins.add(_line((x, -0.25), (x, -0.38), color, width))
    for y in (-0.16, 0.0, 0.16):
        pins.add(_line((0.25, y), (0.38, y), color, width))
        pins.add(_line((-0.25, y), (-0.38, y), color, width))
    return VGroup(body, pins)


def _package(color, width):
    body = RoundedRectangle(
        width=0.78,
        height=0.7,
        corner_radius=0.06,
        stroke_color=color,
        stroke_width=width,
        fill_opacity=0,
    ).shift(DOWN * 0.06)
    lid = _line((-0.39, 0.12), (0.39, 0.12), color, width)
    tape = _line((0, 0.12), (0, -0.4), color, width)
    return VGroup(body, lid, tape)


def _layers(color, width):
    plates = VGroup()
    for i, y in enumerate((0.2, 0.0, -0.2)):
        plate = RoundedRectangle(
            width=0.8,
            height=0.28,
            corner_radius=0.06,
            stroke_color=color,
            stroke_width=width,
            fill_opacity=0,
        ).shift(UP * y)
        plates.add(plate)
    return plates


def _search(color, width):
    glass = Circle(
        radius=0.2, stroke_color=color, stroke_width=width, fill_opacity=0
    ).shift(LEFT * 0.08 + UP * 0.08)
    handle = _line((0.08, -0.08), (0.34, -0.34), color, width)
    return VGroup(glass, handle)


def _hash(color, width):
    return VGroup(
        _line((-0.28, 0.12), (0.32, 0.12), color, width),
        _line((-0.32, -0.12), (0.28, -0.12), color, width),
        _line((-0.08, 0.32), (-0.18, -0.32), color, width),
        _line((0.16, 0.32), (0.06, -0.32), color, width),
    )


def _clock(color, width):
    face = Circle(radius=0.4, stroke_color=color, stroke_width=width, fill_opacity=0)
    return VGroup(
        face,
        _line((0, 0), (0, 0.22), color, width),
        _line((0, 0), (0.16, -0.02), color, width),
    )


def _queue(color, width):
    bars = VGroup()
    for i, y in enumerate((0.22, 0.0, -0.22)):
        length = 0.7 - i * 0.12
        bar = RoundedRectangle(
            width=length,
            height=0.12,
            corner_radius=0.05,
            stroke_width=0,
            fill_color=color,
            fill_opacity=1,
        ).shift(UP * y)
        bars.add(bar)
    return bars


def _warning(color, width):
    tri = Triangle(stroke_color=color, stroke_width=width, fill_opacity=0)
    tri.scale(0.45)
    bang = _line((0, 0.08), (0, -0.08), color, width)
    point = Circle(radius=0.03, stroke_width=0, fill_color=color, fill_opacity=1).shift(
        DOWN * 0.18
    )
    return VGroup(tri, bang, point)


def _play(color, width):
    shape = Triangle(stroke_width=0, fill_color=color, fill_opacity=1)
    shape.scale(0.4)
    shape.rotate(-PI / 2)
    return shape


def _bolt(color, width):
    shape = Polygon(
        [0.08, 0.42, 0],
        [-0.22, 0.02, 0],
        [-0.02, 0.02, 0],
        [-0.1, -0.42, 0],
        [0.24, -0.04, 0],
        [0.02, -0.04, 0],
        stroke_width=0,
        fill_color=color,
        fill_opacity=1,
    )
    return shape


def _folder(color, width):
    tab = RoundedRectangle(
        width=0.36,
        height=0.18,
        corner_radius=0.04,
        stroke_color=color,
        stroke_width=width,
        fill_opacity=0,
    ).shift(LEFT * 0.18 + UP * 0.28)
    body = RoundedRectangle(
        width=0.84,
        height=0.56,
        corner_radius=0.06,
        stroke_color=color,
        stroke_width=width,
        fill_opacity=0,
    ).shift(DOWN * 0.06)
    return VGroup(body, tab)


def _dot(color, width):
    return Circle(radius=0.16, stroke_width=0, fill_color=color, fill_opacity=1)


def _circle(color, width):
    return Circle(radius=0.28, stroke_color=color, stroke_width=width, fill_opacity=0)


def _replica(color, width):
    back = RoundedRectangle(
        width=0.55,
        height=0.7,
        corner_radius=0.06,
        stroke_color=color,
        stroke_width=width,
        fill_opacity=0,
    ).shift(LEFT * 0.1 + UP * 0.08)
    front = RoundedRectangle(
        width=0.55,
        height=0.7,
        corner_radius=0.06,
        stroke_color=color,
        stroke_width=width,
        fill_opacity=0,
    ).shift(RIGHT * 0.12 + DOWN * 0.08)
    return VGroup(back, front)


def _expand(color, width):
    """Four corner arrows around a cylinder — the RDS-style mark."""
    db = _database(color, width)
    db.scale(0.55)
    arrows = VGroup()
    for dx, dy in ((-1, 1), (1, 1), (-1, -1), (1, -1)):
        tip = np.array([dx * 0.42, dy * 0.42, 0])
        tail = tip * 0.45
        arrows.add(_line(tail[:2], tip[:2], color, width))
    return VGroup(db, arrows)


ICONS = {
    "database": _database,
    "lock": _lock,
    "server": _server,
    "cloud": _cloud,
    "check": _check,
    "cross": _cross,
    "ban": _ban,
    "plus": _plus,
    "minus": _minus,
    "key": _key,
    "shield": _shield,
    "user": _user,
    "document": _document,
    "branch": _branch,
    "pin": _pin,
    "globe": _globe,
    "cpu": _cpu,
    "package": _package,
    "layers": _layers,
    "search": _search,
    "hash": _hash,
    "clock": _clock,
    "queue": _queue,
    "warning": _warning,
    "play": _play,
    "bolt": _bolt,
    "folder": _folder,
    "dot": _dot,
    "circle": _circle,
    "replica": _replica,
    "expand": _expand,
}


def icon(name, color=WHITE, height=0.5, stroke_width=2.4):
    """Build a named icon and scale it to ``height``.

    Names: database, lock, server, cloud, check, cross, ban, plus, minus,
    key, shield, user, document, branch, pin, globe, cpu, package, layers,
    search, hash, clock, queue, warning, play, bolt, folder, dot, circle,
    replica, expand.
    """
    try:
        factory = ICONS[name]
    except KeyError as exc:
        known = ", ".join(sorted(ICONS))
        raise KeyError(f"Unknown icon {name!r}. Use one of: {known}") from exc
    glyph = factory(color, stroke_width)
    if glyph.get_height() > 0.05:
        glyph.set_height(height)
    elif glyph.get_width() > 0:
        glyph.set_width(height)
    glyph.center()
    return glyph


def icon_names():
    return tuple(sorted(ICONS))
