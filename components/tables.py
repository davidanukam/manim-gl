"""Rows, pages, and grids: logs, leaderboard-style tables, cursors, cells."""

from manimlib import DOWN, LEFT, RIGHT, Triangle, UP, VGroup

from .motion import animated
from .primitives import Callout, Panel, Slot, TextCard
from .text import Body, MonoText, Title
from .theme import DIM, MONO, MUTED, PURPLE, TEXT


class LogRow(VGroup):
    """A horizontal commit log.

    ``states`` lines up with ``labels``. Shorthand: ``filled=[1, 2]`` and
    ``active=3`` (drawn as an outline). ``pointer`` hangs under ``pointer_at``
    or under ``active``.

    Animate ``add("8")``, ``add("9", state="outline")``, ``set_cell(3, "filled")``,
    ``point_at(3, "APPEND")``, and ``pop()``. The row grows to the right.
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
        self._size = size
        self._font_size = font_size
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
        self._labels = [str(label) for label in labels]
        self._states = list(resolved)
        self._pointer = pointer
        self._pointer_at = pointer_at
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

    def _spawn(self, labels, states, pointer, pointer_at):
        return LogRow(
            labels,
            states=states,
            pointer=pointer,
            pointer_at=pointer_at,
            size=self._size,
            font_size=self._font_size,
        )

    @animated(
        "_labels", "_states", "_pointer", "_pointer_at", "_size", "_font_size",
        anchor="top_left", mobject_safe=True,
    )
    def add(self, label, state="idle"):
        """Append a cell."""
        return self._spawn(
            [*self._labels, str(label)],
            [*self._states, state],
            self._pointer,
            self._pointer_at,
        )

    @animated(
        "_labels", "_states", "_pointer", "_pointer_at", "_size", "_font_size",
        anchor="top_left",
    )
    def set_cell(self, index, state=None, label=None):
        """Change one cell's state, its label, or both."""
        labels = list(self._labels)
        states = list(self._states)
        if label is not None:
            labels[index] = str(label)
        if state is not None:
            states[index] = state
        return self._spawn(labels, states, self._pointer, self._pointer_at)

    @animated(
        "_labels", "_states", "_pointer", "_pointer_at", "_size", "_font_size",
        anchor="top_left",
    )
    def point_at(self, index, text):
        """Hang a callout under one cell."""
        return self._spawn(self._labels, self._states, text, index)

    @animated(
        "_labels", "_states", "_pointer", "_pointer_at", "_size", "_font_size",
        anchor="top_left",
    )
    def pop(self, index=-1):
        """Remove one cell."""
        labels = list(self._labels)
        states = list(self._states)
        labels.pop(index)
        states.pop(index)
        pointer_at = self._pointer_at
        if pointer_at is not None and pointer_at >= len(labels):
            pointer_at = len(labels) - 1 if labels else None
        return self._spawn(labels, states, self._pointer, pointer_at)


class LabeledRow(VGroup):
    """A row name beside a run of slots. ``LabeledRow("P1", ["", "1", "2", "3", ""])``.

    Animate ``set_cell(2, "1", state="filled")``. The row name stays put.
    """

    def __init__(self, label, cells, states=None, size=0.62):
        self._label = label
        self._cells = [str(cell) for cell in cells]
        self._states = list(states) if states is not None else ["ghost"] * len(cells)
        if len(self._states) < len(self._cells):
            self._states.extend(["ghost"] * (len(self._cells) - len(self._states)))
        self._size = size
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

    @animated("_label", "_cells", "_states", "_size", anchor="top_left")
    def set_cell(self, index, text, state=None):
        """Replace one slot's text and, optionally, its state."""
        cells = list(self._cells)
        states = list(self._states)
        cells[index] = str(text)
        if state is not None:
            states[index] = state
        return LabeledRow(self._label, cells, states=states, size=self._size)


class ChipRow(VGroup):
    """A row of small labels. ``accent`` is a list of indexes to fill.

    Animate ``add("token")``, ``add("hot", accent=True)``, ``set_accent([0, 2])``,
    and ``pop()``.
    """

    def __init__(self, labels, accent=None, state="idle", font_size=20):
        self._labels = [str(label) for label in labels]
        self._accent = tuple(accent or [])
        self._state = state
        self._font_size = font_size
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

    def _spawn(self, labels, accent):
        return ChipRow(
            labels, accent=accent, state=self._state, font_size=self._font_size
        )

    @animated(
        "_labels", "_accent", "_state", "_font_size",
        anchor="top_left", mobject_safe=True,
    )
    def add(self, label, accent=False):
        """Append a chip. ``accent=True`` fills it."""
        marks = list(self._accent)
        if accent:
            marks.append(len(self._labels))
        return self._spawn([*self._labels, str(label)], marks)

    @animated("_labels", "_accent", "_state", "_font_size", anchor="top_left")
    def set_accent(self, indexes):
        """Fill the chips at these indexes."""
        return self._spawn(self._labels, list(indexes))

    @animated("_labels", "_accent", "_state", "_font_size", anchor="top_left")
    def pop(self, index=-1):
        """Remove one chip."""
        labels = list(self._labels)
        labels.pop(index)
        if index < 0:
            index = len(self._labels) + index
        marks = [i if i < index else i - 1 for i in self._accent if i != index]
        return self._spawn(labels, marks)


class GridTable(VGroup):
    """A compact table. ``highlight`` is a body-row index.

    ``GridTable(["TERM", "DOCS"], [["fox", "1, 12"], ["brown", "1"]], highlight=0)``

    Animate ``set_highlight(1)`` to move the violet bar. ``None`` clears it.
    """

    def __init__(
        self, headers, rows, highlight=None, font_size=22,         row_height=0.46, col_gap=0.55
    ):
        self._headers = list(headers)
        self._rows = [list(row) for row in rows]
        self._highlight = highlight
        self._font_size = font_size
        self._row_height = row_height
        self._col_gap = col_gap
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

    @animated(
        "_headers", "_rows", "_highlight", "_font_size", "_row_height", "_col_gap",
        anchor="top_left",
    )
    def set_highlight(self, index):
        """Move the highlight bar to a body row. ``None`` clears it."""
        return GridTable(
            self._headers,
            self._rows,
            highlight=index,
            font_size=self._font_size,
            row_height=self._row_height,
            col_gap=self._col_gap,
        )


class DataPage(VGroup):
    """A small table with an optional cursor beside one row.

    Animate ``set_cursor(2)`` to move the triangle. ``None`` hides it.
    """

    def __init__(
        self, rows, headers=None, cursor=None,         cursor_label="CURSOR", font_size=20
    ):
        self._rows = [list(row) for row in rows]
        self._headers = list(headers) if headers else []
        self._cursor = cursor
        self._cursor_label = cursor_label
        self._font_size = font_size
        headers = self._headers
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

    @animated(
        "_rows", "_headers", "_cursor", "_cursor_label", "_font_size",
        anchor="top_left",
    )
    def set_cursor(self, index, label=None):
        """Point the cursor at a body row. ``None`` hides it."""
        return DataPage(
            self._rows,
            headers=self._headers or None,
            cursor=index,
            cursor_label=self._cursor_label if label is None else label,
            font_size=self._font_size,
        )


class CellGrid(VGroup):
    """A matrix of slots.

    ``marks`` maps ``(row, col)`` to a state name. Used for byte grids,
    hypervisor slices, and shard maps.

    Animate ``set_mark(1, 2, "accent")``. The grid stays centered.
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
        self._rows = rows
        self._cols = cols
        self._marks = dict(marks or {})
        self._size = size
        self._gap = gap
        self._default = default
        self._caption = caption
        marks = self._marks
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

    @animated(
        "_rows", "_cols", "_marks", "_size", "_gap", "_default", "_caption",
        anchor="center",
    )
    def set_mark(self, row, col, state):
        """Color one cell. ``state=None`` clears that mark."""
        marks = dict(self._marks)
        if state is None:
            marks.pop((row, col), None)
        else:
            marks[(row, col)] = state
        return CellGrid(
            rows=self._rows,
            cols=self._cols,
            marks=marks,
            size=self._size,
            gap=self._gap,
            default=self._default,
            caption=self._caption,
        )
