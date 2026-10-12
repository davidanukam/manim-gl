"""Meters, bar charts, timelines, heatmaps, and tick marks."""

import numpy as np
from manimlib import DOWN, LEFT, RIGHT, UP, VGroup

from .primitives import Panel, Rule
from .text import Body, Caption, Title
from .theme import DIM, LINE, MUTED, PURPLE, TEXT, mix_hex


def _hatch(width, height, gap=0.13, color="#3A3A3A", stroke_width=1.4, angle=0.7):
    """Diagonal lines clipped to a rectangle centered on the origin."""
    from manimlib import Line

    dx, dy = np.cos(angle), np.sin(angle)
    nx, ny = -dy, dx
    corners = (
        (-width / 2, -height / 2),
        (width / 2, -height / 2),
        (width / 2, height / 2),
        (-width / 2, height / 2),
    )
    projections = [nx * x + ny * y for x, y in corners]
    lo, hi = min(projections), max(projections)
    edges = (
        (corners[0], corners[1]),
        (corners[1], corners[2]),
        (corners[2], corners[3]),
        (corners[3], corners[0]),
    )
    lines = VGroup()
    offset = lo + gap * 0.5
    while offset <= hi:
        hits = []
        for (x1, y1), (x2, y2) in edges:
            ex, ey = x2 - x1, y2 - y1
            denom = nx * ex + ny * ey
            if abs(denom) < 1e-8:
                continue
            t = (offset - nx * x1 - ny * y1) / denom
            if -1e-4 <= t <= 1 + 1e-4:
                hits.append((x1 + t * ex, y1 + t * ey))
        unique = []
        for point in hits:
            if not any(
                abs(point[0] - kept[0]) < 1e-3 and abs(point[1] - kept[1]) < 1e-3
                for kept in unique
            ):
                unique.append(point)
        if len(unique) >= 2:
            lines.add(
                Line(
                    [unique[0][0], unique[0][1], 0],
                    [unique[1][0], unique[1][1], 0],
                    stroke_color=color,
                    stroke_width=stroke_width,
                )
            )
        offset += gap
    return lines


class Meter(VGroup):
    """A horizontal bar.

    ``Meter(1, eyebrow="RAM EXHAUSTED", value_text="10 GB", color="#FE4800")``
    is the full orange bar. ``value`` is a fraction from 0 to 1. ``left_label``
    and ``right_label`` sit above the ends (the half-written line). ``side_label``
    sits to the right of a short indicator.
    """

    def __init__(
        self,
        value=1.0,
        width=6.2,
        height=0.46,
        color=PURPLE,
        eyebrow=None,
        eyebrow_color=None,
        value_text=None,
        caption=None,
        caption_color=None,
        left_label=None,
        right_label=None,
        side_label=None,
        track="#2A2A2A",
        corner_radius=None,
    ):
        value = max(0.0, min(1.0, float(value)))
        radius = height / 2 if corner_radius is None else corner_radius
        self.track = Panel(
            width,
            height,
            fill=track,
            stroke_width=0,
            corner_radius=radius,
            state="ghost",
        )
        fill_w = max(height, width * value) if value > 0 else 0.0
        parts = [self.track]
        self.fill = None
        if fill_w > 0:
            self.fill = Panel(
                min(fill_w, width),
                height,
                fill=color,
                stroke_width=0,
                corner_radius=radius,
                state="accent",
            )
            self.fill.align_to(self.track, LEFT)
            self.fill.set_y(self.track.get_y())
            parts.append(self.fill)
        self.eyebrow = None
        if eyebrow:
            self.eyebrow = Title(eyebrow, color=eyebrow_color or MUTED, font_size=18)
            self.eyebrow.next_to(self.track, UP, buff=0.18)
            parts.append(self.eyebrow)
        self.value_label = None
        if value_text:
            self.value_label = Body(
                str(value_text), font_size=32, color=caption_color or color
            )
            self.value_label.next_to(self.track, DOWN, buff=0.16)
            parts.append(self.value_label)
        self.caption_text = None
        if caption:
            anchor = self.value_label or self.track
            self.caption_text = Caption(
                caption, font_size=24, color=caption_color or color
            )
            self.caption_text.next_to(anchor, DOWN, buff=0.12)
            parts.append(self.caption_text)
        if left_label or right_label:
            if left_label:
                left = Title(left_label, font_size=16, color=color)
                left.next_to(self.track, UP, buff=0.1).align_to(self.track, LEFT)
                parts.append(left)
                self.left_label = left
            if right_label:
                right = Title(right_label, font_size=16, color=MUTED)
                right.next_to(self.track, UP, buff=0.1).align_to(self.track, RIGHT)
                parts.append(right)
                self.right_label = right
        self.side = None
        if side_label:
            self.side = Body(str(side_label), font_size=22, color=color)
            self.side.next_to(self.track, RIGHT, buff=0.16)
            parts.append(self.side)
        super().__init__(*parts)


class RangeBar(VGroup):
    """A label, a bar, and another label. ``A few hundred  ———  instant``."""

    def __init__(self, left, right, fill=0.75, width=3.6, height=0.42, color=PURPLE):
        self.left_text = Body(left, font_size=24, color=TEXT)
        self.bar = Meter(fill, width=width, height=height, color=color)
        self.right_text = Body(right, font_size=24, color=TEXT)
        super().__init__(self.left_text, self.bar, self.right_text)
        self.arrange(RIGHT, buff=0.28)


class BarChart(VGroup):
    """Vertical bars on a shared baseline, with an optional dashed ceiling.

    ``BarChart([1, 2, 2.2, 2.2], labels=["", "", "S3", ""], title="CAPACITY")``
    """

    def __init__(
        self,
        values,
        labels=None,
        title=None,
        color=PURPLE,
        bar_width=0.55,
        max_height=2.4,
        gap=0.22,
        show_ceiling=True,
    ):
        values = [float(v) for v in values]
        peak = max(values) if values else 1.0
        peak = peak or 1.0
        labels = list(labels) if labels is not None else [""] * len(values)
        cols = VGroup()
        self.bars = []
        self.labels = []
        for value, label in zip(values, labels):
            height = max(
                0.08, (value / peak) * max_height * (0.82 if show_ceiling else 1)
            )
            bar = Panel(
                bar_width,
                height,
                state="accent",
                fill=color,
                corner_radius=min(0.08, bar_width / 2),
            )
            text = Body(str(label), font_size=18, color=MUTED) if label else VGroup()
            if label:
                text.next_to(bar, DOWN, buff=0.1)
                col = VGroup(bar, text)
            else:
                col = VGroup(bar)
            cols.add(col)
            self.bars.append(bar)
            self.labels.append(text)
        # Align bars so their bottoms share a line. Each column's bar is its first item.
        cols.arrange(RIGHT, buff=gap, aligned_edge=DOWN)
        for col in cols:
            # Columns with labels are taller; shift so the bar bottoms match the
            # tallest bar's bottom by aligning every bar to a common y.
            pass
        bottoms = [bar.get_bottom()[1] for bar in self.bars]
        target = min(bottoms) if bottoms else 0
        for bar in self.bars:
            bar.shift(UP * (target - bar.get_bottom()[1]))
        for text in self.labels:
            if isinstance(text, VGroup) and len(text) == 0:
                continue
            if text is None or (isinstance(text, VGroup) and len(text) == 0):
                continue
        # Re-seat labels under their bars after the shift.
        for bar, text in zip(self.bars, self.labels):
            if isinstance(text, VGroup) and len(text) == 0:
                continue
            text.next_to(bar, DOWN, buff=0.1)
        parts = [cols]
        self.ceiling = None
        self.title = None
        if show_ceiling:
            top = max(bar.get_top()[1] for bar in self.bars) + 0.35
            width = cols.get_width() + 0.4
            self.ceiling = Rule(width, dashed=True, color=LINE, stroke_width=1.4)
            self.ceiling.set_y(top)
            self.ceiling.set_x(cols.get_x())
            parts.append(self.ceiling)
            if title:
                self.title = Title(title, font_size=18)
                self.title.next_to(self.ceiling, LEFT, buff=0.18)
                self.title.set_y(self.ceiling.get_y())
                parts.append(self.title)
        super().__init__(*parts)


class Timeline(VGroup):
    """A hatched track with event markers.

    ``markers`` is a list of ``(position, label)`` with position in 0..1.
    """

    def __init__(
        self,
        markers,
        start="OPEN",
        end="CLOSE",
        title=None,
        width=10,
        height=0.42,
        color=PURPLE,
    ):
        self.track = Panel(
            width, height, state="ghost", fill="#2A2A2A", corner_radius=0.06
        )
        hatch = _hatch(
            width * 0.98, height * 0.7, gap=0.11, color="#4A4A4A", stroke_width=1.3
        )
        hatch.move_to(self.track)
        parts = [self.track, hatch]
        self.markers = []
        for position, label in markers:
            x = self.track.get_left()[0] + width * float(position)
            mark = Panel(
                0.16, height + 0.28, state="accent", fill=color, corner_radius=0.04
            )
            mark.set_x(x)
            mark.set_y(self.track.get_y())
            words = Title(label, font_size=16, color=color)
            words.next_to(mark, DOWN, buff=0.16)
            parts.extend([mark, words])
            self.markers.append(mark)
        self.start_label = Body(start, font_size=16, color=DIM)
        self.end_label = Body(end, font_size=16, color=DIM)
        self.start_label.next_to(self.track, DOWN, buff=0.72).align_to(self.track, LEFT)
        self.end_label.next_to(self.track, DOWN, buff=0.72).align_to(self.track, RIGHT)
        parts.extend([self.start_label, self.end_label])
        self.title = None
        if title:
            self.title = Title(title, font_size=20)
            self.title.next_to(self.track, UP, buff=0.35)
            parts.append(self.title)
        super().__init__(*parts)


class Heatmap(VGroup):
    """A grid of cells tinted by values in 0..1.

    ``tint`` is ``gray`` or ``purple``. Pass a 2D list, or ``rows`` and ``cols``
    plus a ``pattern`` callable ``(r, c) -> float``.
    """

    def __init__(
        self,
        values=None,
        rows=6,
        cols=14,
        tint="gray",
        cell=0.28,
        gap=0.05,
        pattern=None,
    ):
        if values is None:
            values = [
                [pattern(r, c) if pattern else 0.15 for c in range(cols)]
                for r in range(rows)
            ]
        dark = "#1A1A1A"
        light = "#E4E4E4" if tint == "gray" else PURPLE
        cells = VGroup()
        for r, row in enumerate(values):
            for c, raw in enumerate(row):
                shade = mix_hex(dark, light, raw)
                square = Panel(
                    cell,
                    cell,
                    fill=shade,
                    stroke_width=0,
                    corner_radius=cell * 0.12,
                    state="idle",
                )
                square.move_to([c * (cell + gap), -r * (cell + gap), 0])
                cells.add(square)
        super().__init__(cells)
        self.cells = cells


class TickLine(VGroup):
    """A line with numbered ticks. The "no history" graphic."""

    def __init__(self, labels=None, caption=None, width=5.5):
        labels = list(labels) if labels is not None else ["1", "2", "3", "4", "5"]
        self.rule = Rule(width, color=LINE, stroke_width=1.6)
        ticks = VGroup()
        if len(labels) == 1:
            xs = [0.0]
        else:
            xs = np.linspace(-width / 2, width / 2, len(labels))
        for x, label in zip(xs, labels):
            tick = Rule(0.16, color=LINE, stroke_width=1.6)
            tick.rotate(np.pi / 2)
            tick.move_to([x, 0.08, 0])
            word = Body(str(label), font_size=18, color=MUTED)
            word.next_to(tick, UP, buff=0.08)
            ticks.add(VGroup(tick, word))
        parts = [self.rule, ticks]
        self.caption_text = None
        if caption:
            self.caption_text = Caption(caption, font_size=22)
            self.caption_text.next_to(self.rule, DOWN, buff=0.28)
            parts.append(self.caption_text)
        super().__init__(*parts)
