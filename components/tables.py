"""Rows, pages, and grids: logs, leaderboard-style tables, cursors, cells."""

from manimlib import DOWN, LEFT, RIGHT, Triangle, UP, VGroup

from .primitives import Callout, Panel, Slot, TextCard
from .text import Body, MonoText, Title
from .theme import DIM, MONO, MUTED, PURPLE, TEXT


class LogRow(VGroup):
    """A horizontal commit log.

    ``states`` lines up with ``labels``. Shorthand: ``filled=[1, 2]`` and
    ``active=3`` (drawn as an outline). ``pointer`` hangs under ``pointer_at``
    or under ``active``.
    """

    def __init__(
        self,
        labels,
        states=None,
        filled=None,
        active=None,
        pointer=None,
        pointer_at=None,
        size=0.78,
        font_size=22,
    ):
        resolved = list(states) if states is not None else ["idle"] * len(labels)
        if len(resolved) < len(labels):
            resolved.extend(["idle"] * (len(labels) - len(resolved)))
        if filled:
            for index in filled:
                resolved[index] = "filled"
        if active is not None:
            resolved[active] = "outline"
            if pointer_at is None:
                pointer_at = active
        self.cells = VGroup(
            *[
                Slot(
                    label, state=resolved[i], size=size, font_size=font_size, font=MONO
                )
                for i, label in enumerate(labels)
            ]
        )
        self.cells.arrange(RIGHT, buff=0.1)
        parts = [self.cells]
        self.pointer = None
        if pointer and pointer_at is not None:
            self.pointer = Callout(pointer)
            self.pointer.next_to(self.cells[pointer_at], DOWN, buff=0.08)
            parts.append(self.pointer)
        super().__init__(*parts)


class LabeledRow(VGroup):
    """A row name beside a run of slots. ``LabeledRow("P1", ["", "1", "2", "3", ""])``."""

    def __init__(self, label, cells, states=None, size=0.62):
        self.row_label = Title(label, font_size=20)
        resolved = list(states) if states is not None else ["ghost"] * len(cells)
        self.cells = VGroup(
            *[
                Slot(
                    cell,
                    state=resolved[i] if i < len(resolved) else "ghost",
                    size=size,
                    font_size=20,
                    font=MONO,
                )
                for i, cell in enumerate(cells)
            ]
        )
        self.cells.arrange(RIGHT, buff=0.08)
        self.row_label.next_to(self.cells, LEFT, buff=0.22)
        super().__init__(self.row_label, self.cells)


class ChipRow(VGroup):
    """A row of small labels. ``accent`` is a list of indexes to fill."""

    def __init__(self, labels, accent=None, state="idle", font_size=20):
        accent = set(accent or [])
        chips = []
        for i, label in enumerate(labels):
            chips.append(
                TextCard(
                    str(label),
                    state="filled" if i in accent else state,
                    width=None,
                    height=0.5,
                    font_size=font_size,
                )
            )
        super().__init__(*chips)
        self.arrange(RIGHT, buff=0.12)
        self.chips = chips


class GridTable(VGroup):
    """A compact table. ``highlight`` is a body-row index.

    ``GridTable(["TERM", "DOCS"], [["fox", "1, 12"], ["brown", "1"]], highlight=0)``
    """

    def __init__(
        self, headers, rows, highlight=None, font_size=22, row_height=0.46, col_gap=0.55
    ):
        body = []
        header_mobs = [Title(str(h), font_size=max(14, font_size - 6)) for h in headers]
        row_mobs = []
        for row in rows:
            cells = [Body(str(cell), font_size=font_size) for cell in row]
            row_mobs.append(cells)
        columns = max(len(headers), max((len(r) for r in rows), default=0))
        widths = []
        for c in range(columns):
            widths.append(0.6)
            if c < len(header_mobs):
                widths[c] = max(widths[c], header_mobs[c].get_width())
            for cells in row_mobs:
                if c < len(cells):
                    widths[c] = max(widths[c], cells[c].get_width())
            widths[c] += col_gap

        def _place(cells, y):
            x = 0
            for c, mob in enumerate(cells):
                mob.move_to([x + widths[c] / 2, y, 0])
                x += widths[c]

        total_w = sum(widths) + 0.45
        header_y = 0
        _place(header_mobs, header_y)
        placed_rows = []
        y = header_y - row_height
        bars = []
        for i, cells in enumerate(row_mobs):
            if highlight == i:
                bar = Panel(
                    total_w, row_height * 0.92, state="selected", corner_radius=0.08
                )
                bar.move_to([total_w / 2, y, 0])
                bars.append(bar)
            _place(cells, y)
            placed_rows.append(cells)
            y -= row_height
        all_text = VGroup(
            *header_mobs, *[mob for cells in placed_rows for mob in cells]
        )
        content_height = header_y - y
        self.panel = Panel(
            total_w,
            content_height + 0.2,
            state="muted",
            corner_radius=0.12,
        )
        # Texts were laid out from y=0 downward starting at x centered on columns
        # whose origin is the left of the first column. Shift the whole text block
        # into the panel.
        block = VGroup(*bars, all_text)
        block.move_to(self.panel)
        super().__init__(self.panel, block)


class DataPage(VGroup):
    """A small table with an optional cursor beside one row."""

    def __init__(
        self, rows, headers=None, cursor=None, cursor_label="CURSOR", font_size=20
    ):
        headers = headers or []
        table_rows = []
        if headers:
            table_rows.append(
                [Title(str(h), font_size=max(14, font_size - 4)) for h in headers]
            )
        for row in rows:
            table_rows.append(
                [MonoText(str(cell), font_size=font_size) for cell in row]
            )
        columns = max(len(r) for r in table_rows)
        widths = [0.4] * columns
        for row in table_rows:
            for c, mob in enumerate(row):
                widths[c] = max(widths[c], mob.get_width() + 0.45)
        row_h = 0.42
        bars = []
        y = 0
        for i, row in enumerate(table_rows):
            body_index = i - (1 if headers else 0)
            if cursor is not None and body_index == cursor:
                bar = Panel(
                    sum(widths) + 0.2, row_h * 0.9, state="selected", corner_radius=0.06
                )
                bar.move_to([sum(widths) / 2, y, 0])
                bars.append(bar)
            x = 0
            for c, mob in enumerate(row):
                mob.move_to([x + 0.18 + mob.get_width() / 2, y, 0])
                x += widths[c]
            y -= row_h
        text = VGroup(*[mob for row in table_rows for mob in row])
        block = VGroup(*bars, text)
        self.panel = Panel(
            sum(widths) + 0.35, abs(y) + 0.28, state="idle", corner_radius=0.1
        )
        block.move_to(self.panel)
        parts = [self.panel, block]
        self.cursor_mark = None
        self.cursor_text = None
        if cursor is not None:
            # The highlighted bar, if present, is the first bar and has been moved
            # into the panel. Place the marker to the panel's left, aligned to that row.
            target_y = (
                self.panel.get_top()[1]
                - 0.14
                - row_h * ((cursor + (1 if headers else 0)) + 0.5)
            )
            marker = Triangle(fill_color=PURPLE, fill_opacity=1, stroke_width=0)
            marker.scale(0.08)
            marker.rotate(-3.14159 / 2)
            marker.move_to([self.panel.get_left()[0] - 0.2, target_y, 0])
            label = Title(cursor_label, font_size=14, color=PURPLE)
            label.next_to(marker, LEFT, buff=0.1)
            parts.extend([marker, label])
            self.cursor_mark = marker
            self.cursor_text = label
        super().__init__(*parts)


class CellGrid(VGroup):
    """A matrix of slots.

    ``marks`` maps ``(row, col)`` to a state name. Used for byte grids,
    hypervisor slices, and shard maps.
    """

    def __init__(
        self,
        rows=4,
        cols=8,
        marks=None,
        size=0.38,
        gap=0.07,
        default="ghost",
        caption=None,
    ):
        marks = marks or {}
        cells = VGroup()
        for r in range(rows):
            for c in range(cols):
                cell = Panel(
                    size,
                    size,
                    state=marks.get((r, c), default),
                    corner_radius=size * 0.18,
                )
                cell.move_to([c * (size + gap), -r * (size + gap), 0])
                cells.add(cell)
        parts = [cells]
        self.caption_text = None
        if caption:
            self.caption_text = Title(caption, font_size=16)
            self.caption_text.next_to(cells, DOWN, buff=0.2)
            parts.append(self.caption_text)
        super().__init__(*parts)
        self.cells = cells
