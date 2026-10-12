"""Type styles. Titles are tracked small-caps; headlines are large and light."""

from manimlib import DOWN, LEFT, ORIGIN, Rectangle, RIGHT, Text, VGroup

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
    """Small tracked label, uppercased. The section headings above diagrams."""

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


class Eyebrow(Title):
    """Alias of :class:`Title` with a slightly smaller default size."""

    def __init__(self, text, font_size=18, **kwargs):
        super().__init__(text, font_size=font_size, **kwargs)


class Headline(Text):
    """Large wordmark or statement. ``git``, ``SQLite``, ``NO LOCKS``."""

    def __init__(
        self, text, font_size=72, color=TEXT, weight=LIGHT, font=SANS, **kwargs
    ):
        super().__init__(
            str(text),
            font=font,
            font_size=font_size,
            color=color,
            weight=weight,
            **kwargs,
        )


class Body(Text):
    """Sentence-case copy under or inside a diagram."""

    def __init__(
        self, text, font_size=30, color=TEXT, weight=NORMAL, font=SANS, **kwargs
    ):
        super().__init__(
            str(text),
            font=font,
            font_size=font_size,
            color=color,
            weight=weight,
            **kwargs,
        )


class Caption(Body):
    """Secondary sentence. Defaults to the muted gray used under diagrams."""

    def __init__(self, text, font_size=28, color=MUTED, **kwargs):
        super().__init__(text, font_size=font_size, color=color, **kwargs)


class MonoText(Text):
    """Consolas line for code, hashes, offsets, and big figures."""

    def __init__(self, text, font_size=26, color=TEXT, weight=NORMAL, **kwargs):
        super().__init__(
            str(text),
            font=MONO,
            font_size=font_size,
            color=color,
            weight=weight,
            **kwargs,
        )


class Stat(MonoText):
    """A large figure such as ``10,400,000`` or ``4,096``."""

    def __init__(self, text, font_size=78, color=TEXT, **kwargs):
        super().__init__(str(text), font_size=font_size, color=color, **kwargs)


class Note(Text):
    """A sentence with one substring picked out in violet (or another color)."""

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
        mapping = {highlight: highlight_color} if highlight else {}
        super().__init__(
            str(text),
            font=font,
            font_size=font_size,
            color=color,
            t2c=mapping,
            **kwargs,
        )


class StatBlock(VGroup):
    """Eyebrow, big number, and an optional unit line.

    ``StatBlock("10,400,000", eyebrow="TRADITIONAL DATABASE")``
    ``StatBlock("4,096", unit="IDS PER MS")``
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


class Formula(VGroup):
    """Left-aligned mono lines. Pass ``accent`` to tint one line violet."""

    def __init__(self, lines, accent=None, font_size=28, color=TEXT):
        rows = []
        for i, line in enumerate(lines):
            tint = PURPLE if accent is not None and i == accent else color
            rows.append(MonoText(line, font_size=font_size, color=tint))
        super().__init__(*rows)
        if len(rows):
            self.arrange(DOWN, buff=0.12, aligned_edge=LEFT)


class DiffStat(VGroup):
    """``+2  -1`` in green and red, the git diff summary."""

    def __init__(self, added=0, removed=0, font_size=28):
        from .theme import GREEN, RED

        self.added_text = MonoText(f"+{added}", font_size=font_size, color=GREEN)
        self.removed_text = MonoText(f"-{removed}", font_size=font_size, color=RED)
        super().__init__(self.added_text, self.removed_text)
        self.arrange(RIGHT, buff=0.22)


class TermWeight(VGroup):
    """A scoring term and its weight: ``"data"  ×  0.1``."""

    def __init__(self, term, weight, font_size=26):
        word = MonoText(f'"{term}"', font_size=font_size, color=TEXT)
        times = Body("×", font_size=font_size, color=DIM)
        value = MonoText(str(weight), font_size=font_size, color=PURPLE)
        super().__init__(word, times, value)
        self.arrange(RIGHT, buff=0.2)


class FractionCallout(VGroup):
    """``14`` over ``out of 20``, with an optional caption."""

    def __init__(self, numerator, denominator, caption=None, color=TEXT):
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
