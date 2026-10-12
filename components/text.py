"""Type styles. Titles are tracked small-caps; headlines are large and light."""

from manimlib import DOWN, LEFT, ORIGIN, Rectangle, RIGHT, Text, VGroup

from .motion import animated
from .theme import BOLD, DIM, LIGHT, MONO, MUTED, NORMAL, PURPLE, SANS, TEXT


def _spacer(width, height=0.08):
    box = Rectangle(
        width=max(width, 0.001),
        height=height,
        stroke_width=0,
        fill_opacity=0,
    )
    box.move_to(ORIGIN)
    return box


def tracked(
    text,
    font_size=28,
    color=MUTED,
    tracking=0.045,
    font=SANS,
    weight=NORMAL,
):
    """One line of letters with extra space between them.

    Section labels in the videos ("CAPACITY", "HOST CPU") use this tracking.
    """
    gap = tracking * (font_size / 32)
    space = gap * 3.4 + font_size * 0.004
    parts = VGroup()
    for ch in str(text):
        if ch == " ":
            parts.add(_spacer(space, font_size * 0.004))
            continue
        glyph = Text(ch, font=font, font_size=font_size, color=color, weight=weight)
        parts.add(glyph)
    if len(parts) == 0:
        parts.add(_spacer(0.02))
    else:
        parts.arrange(RIGHT, buff=gap)
    return parts


class Title(VGroup):
    """Small tracked label, uppercased. The section headings above diagrams.

    Animate ``set_text("HOST CPU")``. :class:`Eyebrow` uses the same method.
    Scale and shift work like any other mobject.
    """

    def __init__(
        self,
        text,
        font_size=22,
        color=MUTED,
        tracking=0.05,
        weight=NORMAL,
        font=SANS,
        **kwargs,
    ):
        self._font_size = font_size
        self._color = color
        self._tracking = tracking
        self._weight = weight
        self._font = font
        letters = tracked(
            str(text).upper(),
            font_size=font_size,
            color=color,
            tracking=tracking,
            font=font,
            weight=weight,
        )
        super().__init__(*letters.submobjects, **kwargs)
        self.source = str(text)

    @animated("source", "_font_size", "_color", "_tracking", "_weight", "_font", anchor="center")
    def set_text(self, text):
        """Replace the tracked label."""
        return type(self)(
            str(text),
            font_size=self._font_size,
            color=self._color,
            tracking=self._tracking,
            weight=self._weight,
            font=self._font,
        )


class Eyebrow(Title):
    """Alias of :class:`Title` with a slightly smaller default size."""

    def __init__(self, text, font_size=18, **kwargs):
        super().__init__(text, font_size=font_size, **kwargs)


class Headline(Text):
    """Large wordmark or statement. ``git``, ``SQLite``, ``NO LOCKS``.

    Animate ``set_text("SQLite")``. The word stays centered. Scale and shift
    work like any other mobject.
    """

    def __init__(
        self, text, font_size=72, color=TEXT, weight=LIGHT, font=SANS, **kwargs
    ):
        self._ink = color
        super().__init__(
            str(text),
            font=font,
            font_size=font_size,
            color=color,
            weight=weight,
            **kwargs,
        )

    @animated("text", "font", "font_size", "weight", "_ink", anchor="center")
    def set_text(self, text):
        """Replace the wordmark."""
        return type(self)(
            str(text),
            font_size=self.font_size,
            color=self._ink,
            weight=self.weight,
            font=self.font,
        )


class Body(Text):
    """Sentence-case copy under or inside a diagram.

    Animate ``set_text("A new sentence")``. :class:`Caption` uses the same
    method. The line stays centered.
    """

    def __init__(
        self, text, font_size=30, color=TEXT, weight=NORMAL, font=SANS, **kwargs
    ):
        self._ink = color
        super().__init__(
            str(text),
            font=font,
            font_size=font_size,
            color=color,
            weight=weight,
            **kwargs,
        )

    @animated("text", "font", "font_size", "weight", "_ink", anchor="center")
    def set_text(self, text):
        """Replace the sentence."""
        return type(self)(
            str(text),
            font_size=self.font_size,
            color=self._ink,
            weight=self.weight,
            font=self.font,
        )


class Caption(Body):
    """Secondary sentence. Defaults to the muted gray used under diagrams."""

    def __init__(self, text, font_size=28, color=MUTED, **kwargs):
        super().__init__(text, font_size=font_size, color=color, **kwargs)


class MonoText(Text):
    """Consolas line for code, hashes, offsets, and big figures.

    Animate ``set_text("4,096")``. :class:`Stat` uses the same method.
    """

    def __init__(self, text, font_size=26, color=TEXT, weight=NORMAL, **kwargs):
        self._ink = color
        super().__init__(
            str(text),
            font=MONO,
            font_size=font_size,
            color=color,
            weight=weight,
            **kwargs,
        )

    @animated("text", "font", "font_size", "weight", "_ink", anchor="center")
    def set_text(self, text):
        """Replace the mono line."""
        return type(self)(
            str(text),
            font_size=self.font_size,
            color=self._ink,
            weight=self.weight,
        )


class Stat(MonoText):
    """A large figure such as ``10,400,000`` or ``4,096``."""

    def __init__(self, text, font_size=78, color=TEXT, **kwargs):
        super().__init__(str(text), font_size=font_size, color=color, **kwargs)


class Note(Text):
    """A sentence with one substring picked out in violet (or another color).

    Animate ``set_text("The new sentence", highlight="new")``. If the highlight
    word is left out, the previous highlight is kept when it still appears.
    """

    def __init__(
        self,
        text,
        highlight=None,
        highlight_color=PURPLE,
        font_size=28,
        color=MUTED,
        font=SANS,
        **kwargs,
    ):
        self._highlight = highlight
        self._highlight_color = highlight_color
        self._ink = color
        self._font = font
        mapping = {highlight: highlight_color} if highlight else {}
        super().__init__(
            str(text),
            font=font,
            font_size=font_size,
            color=color,
            t2c=mapping,
            **kwargs,
        )

    @animated(
        "text", "font", "font_size", "weight", "_ink", "_highlight",
        "_highlight_color", "_font", anchor="center",
    )
    def set_text(self, text, highlight=None):
        """Replace the sentence. Pass ``highlight`` to pick out a new word."""
        word = self._highlight if highlight is None else highlight
        if word and word not in str(text):
            word = None
        return Note(
            str(text),
            highlight=word,
            highlight_color=self._highlight_color,
            font_size=self.font_size,
            color=self._ink,
            font=self._font,
        )


class StatBlock(VGroup):
    """Eyebrow, big number, and an optional unit line.

    ``StatBlock("10,400,000", eyebrow="TRADITIONAL DATABASE")``
    ``StatBlock("4,096", unit="IDS PER MS")``

    Animate ``set_value("10,400,001")``. The block stays centered.
    """

    def __init__(
        self,
        value,
        eyebrow=None,
        unit=None,
        color=TEXT,
        eyebrow_color=MUTED,
        unit_color=MUTED,
    ):
        self._value = value
        self._eyebrow = eyebrow
        self._unit = unit
        self._color = color
        self._eyebrow_color = eyebrow_color
        self._unit_color = unit_color
        self.value_text = Stat(str(value), color=color)
        parts = []
        self.eyebrow = None
        self.unit_text = None
        if eyebrow:
            self.eyebrow = Title(eyebrow, color=eyebrow_color, font_size=20)
            parts.append(self.eyebrow)
        parts.append(self.value_text)
        if unit:
            self.unit_text = Title(unit, color=unit_color, font_size=18)
            parts.append(self.unit_text)
        super().__init__(*parts)
        self.arrange(DOWN, buff=0.16)

    @animated(
        "_value", "_eyebrow", "_unit", "_color", "_eyebrow_color", "_unit_color",
        anchor="center",
    )
    def set_value(self, value):
        """Replace the big number."""
        return StatBlock(
            value,
            eyebrow=self._eyebrow,
            unit=self._unit,
            color=self._color,
            eyebrow_color=self._eyebrow_color,
            unit_color=self._unit_color,
        )


class Formula(VGroup):
    """Left-aligned mono lines. Pass ``accent`` to tint one line violet.

    Animate ``add_line("y = mx")``, ``set_accent(1)``, and ``pop()``.
    """

    def __init__(self, lines, accent=None, font_size=28, color=TEXT):
        self._lines = [str(line) for line in lines]
        self._accent = accent
        self._font_size = font_size
        self._color = color
        rows = []
        for i, line in enumerate(lines):
            tint = PURPLE if accent is not None and i == accent else color
            rows.append(MonoText(line, font_size=font_size, color=tint))
        super().__init__(*rows)
        if len(rows):
            self.arrange(DOWN, buff=0.12, aligned_edge=LEFT)

    def _spawn(self, lines, accent):
        return Formula(
            lines, accent=accent, font_size=self._font_size, color=self._color
        )

    @animated("_lines", "_accent", "_font_size", "_color", anchor="top_left", mobject_safe=True)
    def add_line(self, line):
        """Append a mono line."""
        return self._spawn([*self._lines, str(line)], self._accent)

    @animated("_lines", "_accent", "_font_size", "_color", anchor="top_left")
    def set_accent(self, index):
        """Tint one line violet. ``None`` clears it."""
        return self._spawn(self._lines, index)

    @animated("_lines", "_accent", "_font_size", "_color", anchor="top_left")
    def pop(self, index=-1):
        """Remove one line."""
        lines = list(self._lines)
        lines.pop(index)
        accent = self._accent
        if accent is not None and accent >= len(lines):
            accent = None
        return self._spawn(lines, accent)


class DiffStat(VGroup):
    """``+2  -1`` in green and red, the git diff summary.

    Animate ``set_counts(3, 1)``.
    """

    def __init__(self, added=0, removed=0, font_size=28):
        self._added = added
        self._removed = removed
        self._font_size = font_size
        from .theme import GREEN, RED

        self.added_text = MonoText(f"+{added}", font_size=font_size, color=GREEN)
        self.removed_text = MonoText(f"-{removed}", font_size=font_size, color=RED)
        super().__init__(self.added_text, self.removed_text)
        self.arrange(RIGHT, buff=0.22)

    @animated("_added", "_removed", "_font_size", anchor="center")
    def set_counts(self, added, removed):
        """Replace the added and removed counts."""
        return DiffStat(added, removed, font_size=self._font_size)


class TermWeight(VGroup):
    """A scoring term and its weight: ``"data"  ×  0.1``.

    Animate ``set_weight(0.4)`` or ``set_term("title")``.
    """

    def __init__(self, term, weight, font_size=26):
        self._term = term
        self._weight = weight
        self._font_size = font_size
        word = MonoText(f'"{term}"', font_size=font_size, color=TEXT)
        times = Body("×", font_size=font_size, color=DIM)
        value = MonoText(str(weight), font_size=font_size, color=PURPLE)
        super().__init__(word, times, value)
        self.arrange(RIGHT, buff=0.2)

    def _spawn(self, term, weight):
        return TermWeight(term, weight, font_size=self._font_size)

    @animated("_term", "_weight", "_font_size", anchor="center")
    def set_weight(self, weight):
        """Replace the weight."""
        return self._spawn(self._term, weight)

    @animated("_term", "_weight", "_font_size", anchor="center")
    def set_term(self, term):
        """Replace the quoted term."""
        return self._spawn(term, self._weight)


class FractionCallout(VGroup):
    """``14`` over ``out of 20``, with an optional caption.

    Animate ``set_fraction(15, 20)``. The callout stays centered.
    """

    def __init__(self, numerator, denominator, caption=None, color=TEXT):
        self._numerator = numerator
        self._denominator = denominator
        self._caption = caption
        self._color = color
        num = Stat(str(numerator), font_size=64, color=color)
        den = Caption(f"out of {denominator}", font_size=22)
        block = VGroup(num, den).arrange(DOWN, buff=0.06)
        parts = [block]
        self.caption = None
        if caption:
            self.caption = Caption(caption, font_size=20)
            parts.append(self.caption)
        super().__init__(*parts)
        self.arrange(DOWN, buff=0.12)

    @animated("_numerator", "_denominator", "_caption", "_color", anchor="center")
    def set_fraction(self, numerator, denominator=None, caption=None):
        """Replace the fraction. Leave ``denominator`` out to keep it."""
        return FractionCallout(
            numerator,
            self._denominator if denominator is None else denominator,
            caption=self._caption if caption is None else caption,
            color=self._color,
        )
