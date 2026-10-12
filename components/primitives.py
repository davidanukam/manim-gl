"""Rounded panels, chips, slots, rules, and the lines that join them."""

import numpy as np
from manimlib import (
    DOWN,
    DashedLine,
    LEFT,
    Line,
    Mobject,
    RIGHT,
    RoundedRectangle,
    Text,
    UP,
    VGroup,
)

from .text import MonoText, Title
from .theme import LINE, MONO, MUTED, ORANGE, PURPLE, SANS, TEXT, clamp_radius, style_of


def apply_state(panel, state, label=None):
    """Recolor a panel (and an optional label) to a named state."""
    style = style_of(state)
    panel.set_fill(style["fill"], opacity=style["fill_opacity"])
    panel.set_stroke(style["stroke"], width=style["stroke_width"])
    if label is not None:
        label.set_color(style["text"])
    return style


class Panel(RoundedRectangle):
    """A rounded rectangle in one of the shared states.

    ``Panel(3, 1.2, state="outline")`` is the thin violet frame used around
    groups. ``state="accent"`` is a solid violet block. ``state="hot"`` is
    the solid orange meter fill.
    """

    def __init__(
        self,
        width=2.4,
        height=1.0,
        state="idle",
        corner_radius=0.14,
        fill=None,
        stroke=None,
        stroke_width=None,
        fill_opacity=None,
        **kwargs,
    ):
        style = style_of(state)
        if fill is not None:
            style["fill"] = fill
        if stroke is not None:
            style["stroke"] = stroke
        if stroke_width is not None:
            style["stroke_width"] = stroke_width
        if fill_opacity is not None:
            style["fill_opacity"] = fill_opacity
        width = max(float(width), 0.04)
        height = max(float(height), 0.04)
        super().__init__(
            width=width,
            height=height,
            corner_radius=clamp_radius(width, height, corner_radius),
            fill_color=style["fill"],
            fill_opacity=style["fill_opacity"],
            stroke_color=style["stroke"],
            stroke_width=style["stroke_width"],
            **kwargs,
        )
        self.state = state
        self.style = style


class TextCard(VGroup):
    """Centered label inside a rounded card.

    This is the basic box in every video (``AUTH``, ``YOU``, ``worker``).
    Pass ``subtitle`` for a second line and ``status`` for a short state
    word such as ``BLOCKED``. ``width=None`` hugs the text.
    """

    def __init__(
        self,
        label="",
        subtitle=None,
        status=None,
        width=2.3,
        height=0.82,
        state="idle",
        fill=None,
        stroke=None,
        text_color=None,
        status_color=ORANGE,
        font_size=28,
        subtitle_size=18,
        corner_radius=0.14,
        pad_x=0.28,
        pad_y=0.16,
        font=SANS,
        weight="NORMAL",
        strike=False,
        **kwargs,
    ):
        self.font = font
        self.weight = weight
        self.font_size = font_size
        self._state_name = state
        style = style_of(state)
        if text_color is not None:
            style["text"] = text_color

        pieces = VGroup()
        self.label = None
        self.subtitle = None
        self.status_text = None
        if label != "":
            self.label = Text(
                str(label),
                font=font,
                font_size=font_size,
                color=style["text"],
                weight=weight,
            )
            pieces.add(self.label)
        if subtitle:
            self.subtitle = Text(
                str(subtitle),
                font=MONO if font == MONO else SANS,
                font_size=subtitle_size,
                color=MUTED,
            )
            pieces.add(self.subtitle)
        if status:
            self.status_text = Text(
                str(status),
                font=SANS,
                font_size=max(14, subtitle_size),
                color=status_color,
                weight="BOLD",
            )
            pieces.add(self.status_text)
        if len(pieces):
            pieces.arrange(DOWN, buff=0.06)

        if width is None:
            width = (pieces.get_width() if len(pieces) else 0.4) + pad_x * 2
        if height is None:
            content_h = pieces.get_height() if len(pieces) else 0.2
            height = max(content_h + pad_y * 2, 0.48)

        self.panel = Panel(
            width,
            height,
            state=state,
            corner_radius=corner_radius,
            fill=fill,
            stroke=stroke,
        )
        if len(pieces):
            inner = max(self.panel.get_width() - pad_x, 0.1)
            if pieces.get_width() > inner:
                pieces.scale(inner / pieces.get_width())
            pieces.move_to(self.panel)

        parts = [self.panel]
        if len(pieces):
            parts.append(pieces)
        self.strike_line = None
        if strike and len(pieces):
            y = self.label.get_y() if self.label is not None else self.panel.get_y()
            x0 = pieces.get_left()[0]
            x1 = pieces.get_right()[0]
            self.strike_line = Line(
                [x0, y, 0],
                [x1, y, 0],
                stroke_color=style["text"],
                stroke_width=2,
            )
            parts.append(self.strike_line)
        super().__init__(*parts, **kwargs)
        self.pieces = pieces

    def set_state(self, state):
        """Recolor the card without rebuilding it."""
        self._state_name = state
        apply_state(self.panel, state, self.label)
        return self

    def set_label(self, text):
        """Replace the main label and keep it inside the card."""
        if self.label is None:
            return self
        color = self.label.get_color()
        new = Text(
            str(text),
            font=self.font,
            font_size=self.font_size,
            color=color,
            weight=self.weight,
        )
        limit = self.panel.get_width() - 0.24
        if new.get_width() > limit > 0:
            new.scale(limit / new.get_width())
        new.move_to(self.label)
        self.pieces.remove(self.label)
        self.label = new
        self.pieces.add(new)
        return self


class Chip(TextCard):
    """A card that hugs its label. The small tags such as ``CACHED`` live here."""

    def __init__(
        self,
        label,
        font_size=22,
        pad_x=0.22,
        pad_y=0.12,
        height=None,
        width=None,
        **kwargs,
    ):
        super().__init__(
            label,
            font_size=font_size,
            pad_x=pad_x,
            pad_y=pad_y,
            height=height,
            width=width,
            **kwargs,
        )


class Pill(Chip):
    """A chip with fully rounded ends."""

    def __init__(self, label, **kwargs):
        super().__init__(label, corner_radius=2, **kwargs)


class Badge(Pill):
    """Tiny status word: ``CACHED``, ``VALID``, ``REBUILD``."""

    def __init__(self, label, state="muted", font_size=16, **kwargs):
        super().__init__(str(label).upper(), state=state, font_size=font_size, **kwargs)


class Slot(VGroup):
    """One square cell in a log, page, or partition row."""

    def __init__(
        self,
        label="",
        state="idle",
        size=0.78,
        font_size=24,
        font=MONO,
        corner_radius=None,
        **kwargs,
    ):
        radius = size * 0.18 if corner_radius is None else corner_radius
        self.panel = Panel(size, size, state=state, corner_radius=radius)
        style = style_of(state)
        self.label = None
        if str(label) != "":
            self.label = Text(
                str(label), font=font, font_size=font_size, color=style["text"]
            )
            limit = size * 0.78
            if self.label.get_width() > limit:
                self.label.scale(limit / self.label.get_width())
            self.label.move_to(self.panel)
        parts = [self.panel]
        if self.label is not None:
            parts.append(self.label)
        super().__init__(*parts, **kwargs)
        self.font = font
        self.font_size = font_size

    def set_state(self, state):
        apply_state(self.panel, state, self.label)
        return self


class Surround(VGroup):
    """A frame drawn around mobjects that are already positioned.

    Children are not rearranged. Build the group, then wrap it.
    """

    def __init__(
        self,
        *mobs,
        buff=0.22,
        state="muted",
        corner_radius=0.16,
        fill_opacity=None,
        **kwargs,
    ):
        self.content = VGroup(*mobs)
        width = max(self.content.get_width() + buff * 2, 0.4)
        height = max(self.content.get_height() + buff * 2, 0.4)
        self.panel = Panel(
            width,
            height,
            state=state,
            corner_radius=corner_radius,
            fill_opacity=fill_opacity,
        )
        self.panel.move_to(self.content)
        super().__init__(self.panel, self.content, **kwargs)


class Rule(VGroup):
    """A horizontal hairline. ``dashed=True`` is the capacity baseline."""

    def __init__(self, width=4, dashed=False, color=LINE, stroke_width=1.5, **kwargs):
        start = LEFT * width / 2
        end = RIGHT * width / 2
        if dashed:
            line = DashedLine(
                start,
                end,
                dash_length=0.08,
                positive_space_ratio=0.45,
                stroke_color=color,
                stroke_width=stroke_width,
            )
        else:
            line = Line(start, end, stroke_color=color, stroke_width=stroke_width)
        super().__init__(line, **kwargs)
        self.line = line


class Stem(Line):
    """A short vertical tick hanging from a node (the worker's blocked stem)."""

    def __init__(self, length=0.45, color=ORANGE, stroke_width=2.5, **kwargs):
        super().__init__(
            UP * length / 2,
            DOWN * length / 2,
            stroke_color=color,
            stroke_width=stroke_width,
            **kwargs,
        )
        self.length = length


class Callout(VGroup):
    """A stem plus a tracked label, such as ``RE-READING`` under a log cell."""

    def __init__(self, text, color=PURPLE, length=0.38, font_size=18, **kwargs):
        self.stem = Stem(length=length, color=color, stroke_width=2)
        self.label = Title(text, color=color, font_size=font_size)
        self.label.next_to(self.stem, DOWN, buff=0.08)
        super().__init__(self.stem, self.label, **kwargs)


class EqualsSign(MonoText):
    """The ``=`` drawn between two file cards."""

    def __init__(self, color=MUTED, font_size=36, **kwargs):
        super().__init__("=", color=color, font_size=font_size, **kwargs)


def border_point(mob, direction, gap=0.0):
    """Point on ``mob``'s bounding box where a ray from the center exits."""
    direction = np.array(direction, dtype=float)
    norm = np.linalg.norm(direction[:2])
    if norm < 1e-8:
        return mob.get_center()
    direction = direction / norm
    center = mob.get_center()
    half_w = mob.get_width() / 2
    half_h = mob.get_height() / 2
    times = []
    if abs(direction[0]) > 1e-8:
        times.append(half_w / abs(direction[0]))
    if abs(direction[1]) > 1e-8:
        times.append(half_h / abs(direction[1]))
    distance = min(times) if times else 0.0
    return center + direction * (distance + gap)


def connect(a, b, mode="straight", arrow=False, color=LINE, gap=0.06, stroke_width=2.0):
    """A line or elbow between two mobjects.

    ``mode`` is ``straight``, ``elbow`` (one bend), or ``bus`` is not here —
    trees draw their own bus. ``arrow=True`` adds a small head on straight links.
    """
    if not isinstance(a, Mobject) or not isinstance(b, Mobject):
        raise TypeError("connect() expects two mobjects that are already placed")
    if mode == "elbow":
        return _elbow(a, b, color=color, stroke_width=stroke_width)
    start = a.get_center()
    end = b.get_center()
    direction = end - start
    p1 = border_point(a, direction, gap=gap)
    p2 = border_point(b, -direction, gap=gap)
    if arrow:
        from manimlib import Arrow

        return Arrow(
            p1,
            p2,
            buff=0,
            fill_color=color,
            thickness=max(stroke_width, 2),
            stroke_width=0,
        )
    return Line(p1, p2, stroke_color=color, stroke_width=stroke_width)


def _elbow(a, b, color=LINE, stroke_width=2.0):
    ac = a.get_center()
    bc = b.get_center()
    lines = []
    if abs(ac[0] - bc[0]) >= abs(ac[1] - bc[1]):
        p1 = a.get_right() if bc[0] >= ac[0] else a.get_left()
        p2 = b.get_left() if bc[0] >= ac[0] else b.get_right()
        mid_x = (p1[0] + p2[0]) / 2
        points = (p1, [mid_x, p1[1], 0], [mid_x, p2[1], 0], p2)
    else:
        p1 = a.get_top() if bc[1] >= ac[1] else a.get_bottom()
        p2 = b.get_bottom() if bc[1] >= ac[1] else b.get_top()
        mid_y = (p1[1] + p2[1]) / 2
        points = (p1, [p1[0], mid_y, 0], [p2[0], mid_y, 0], p2)
    for left, right in zip(points, points[1:]):
        lines.append(Line(left, right, stroke_color=color, stroke_width=stroke_width))
    return VGroup(*lines)


class FlowArrow(VGroup):
    """Straight arrow from one placed mobject to another."""

    def __init__(self, start, end, color=LINE, stroke_width=2.0, **kwargs):
        link = connect(start, end, arrow=True, color=color, stroke_width=stroke_width)
        super().__init__(link, **kwargs)
