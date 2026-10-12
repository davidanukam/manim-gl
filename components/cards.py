"""Cards with an internal layout: files, specs, machines, queues, columns."""

from manimlib import DOWN, LEFT, RIGHT, Rectangle, UP, VGroup

from .icons import icon
from .primitives import Badge, Panel, Surround, TextCard, apply_state
from .text import Body, Headline, MonoText, Title
from .theme import (
    BOLD,
    DIM,
    GREEN,
    MONO,
    MUTED,
    ORANGE,
    PURPLE,
    PURPLE_DEEP,
    SANS,
    TEXT,
    WHITE,
    style_of,
)


class FileCard(TextCard):
    """Filename over a secondary mono line (a hash or a hex dump)."""

    def __init__(self, name, detail="", state="idle", width=3.3, height=1.35, **kwargs):
        super().__init__(
            name,
            subtitle=detail or None,
            state=state,
            width=width,
            height=height,
            font_size=28,
            subtitle_size=18,
            **kwargs,
        )
        if self.subtitle is not None:
            self.subtitle.set_color(MUTED)


class StatusCard(TextCard):
    """A name with a status word under it. ``StatusCard("worker", "BLOCKED")``."""

    def __init__(
        self,
        name,
        status,
        status_color=ORANGE,
        width=2.4,
        height=1.25,
        state="idle",
        **kwargs,
    ):
        super().__init__(
            name,
            status=status,
            status_color=status_color,
            width=width,
            height=height,
            state=state,
            font_size=30,
            **kwargs,
        )


class SideCard(TextCard):
    """A card with a colored stripe on the left edge (primary / replica)."""

    def __init__(self, label, stripe=PURPLE, width=2.8, height=1.15, **kwargs):
        super().__init__(label, width=width, height=height, **kwargs)
        bar = Rectangle(
            width=0.055,
            height=self.panel.get_height() * 0.62,
            fill_color=stripe,
            fill_opacity=1,
            stroke_width=0,
        )
        bar.move_to(self.panel.get_left() + RIGHT * 0.14)
        self.add(bar)
        self.stripe_bar = bar


class ResourceTile(TextCard):
    """One resource inside a computer: ``vCPU``, ``vRAM``, ``Kernel``."""

    def __init__(
        self, label, state="idle", width=1.45, height=0.7, font_size=22, **kwargs
    ):
        super().__init__(
            label,
            state=state,
            width=width,
            height=height,
            font_size=font_size,
            corner_radius=0.1,
            **kwargs,
        )


class Computer(Surround):
    """A framed grid of resource tiles. One name can be ``accented``.

    ``Computer([["vCPU", "vRAM"], ["vDISK", "Kernel"]], accent="Kernel")``
    """

    def __init__(self, tiles, accent=None, tile_width=1.45, tile_height=0.68, **kwargs):
        rows = tiles
        if tiles and not isinstance(tiles[0], (list, tuple)):
            rows = [tiles]
        built = []
        for row in rows:
            cells = VGroup()
            for name in row:
                state = "filled" if accent is not None and name == accent else "idle"
                cells.add(
                    ResourceTile(
                        name, state=state, width=tile_width, height=tile_height
                    )
                )
            cells.arrange(RIGHT, buff=0.1)
            built.append(cells)
        grid = VGroup(*built).arrange(DOWN, buff=0.1)
        super().__init__(grid, buff=0.16, state="outline", corner_radius=0.14, **kwargs)
        self.tiles = grid


class LayerRow(VGroup):
    """One Dockerfile instruction. ``status`` is ``CACHED`` or ``REBUILD``."""

    def __init__(self, instruction, status=None, width=7.2, height=0.58):
        rebuild = str(status).upper() == "REBUILD" if status else False
        if rebuild:
            self.panel = Panel(width, height, state="warn", corner_radius=0.1)
            text_color = "#FFB088"
            status_color = "#FFB088"
        else:
            self.panel = Panel(width, height, state="idle", corner_radius=0.1)
            text_color = TEXT
            status_color = MUTED
        self.instruction = MonoText(instruction, font_size=22, color=text_color)
        self.instruction.align_to(self.panel, LEFT).shift(RIGHT * 0.28)
        self.instruction.set_y(self.panel.get_y())
        parts = [self.panel, self.instruction]
        self.status_text = None
        if status:
            self.status_text = MonoText(
                str(status).upper(), font_size=18, color=status_color
            )
            self.status_text.align_to(self.panel, RIGHT).shift(LEFT * 0.28)
            self.status_text.set_y(self.panel.get_y())
            parts.append(self.status_text)
        super().__init__(*parts)


class LayerStack(VGroup):
    """A vertical list of :class:`LayerRow` items.

    ``layers`` is a list of ``(instruction, status)`` pairs.
    """

    def __init__(self, layers, width=7.2, buff=0.1):
        rows = [LayerRow(instr, status, width=width) for instr, status in layers]
        super().__init__(*rows)
        self.arrange(DOWN, buff=buff)
        self.rows = rows


class LeaderboardRow(VGroup):
    """``01   phoenix                                   9,501``."""

    def __init__(self, rank, name, score, state="idle", width=6.4, height=0.52):
        self.panel = Panel(width, height, state=state, corner_radius=0.1)
        style = style_of(state)
        rank_color = PURPLE if state == "selected" else DIM
        self.rank_text = MonoText(str(rank), font_size=20, color=rank_color)
        self.name_text = Body(str(name), font_size=24, color=style["text"])
        self.score_text = MonoText(str(score), font_size=20, color=style["text"])
        self.rank_text.align_to(self.panel, LEFT).shift(RIGHT * 0.24)
        self.name_text.next_to(self.rank_text, RIGHT, buff=0.32)
        self.score_text.align_to(self.panel, RIGHT).shift(LEFT * 0.24)
        for mob in (self.rank_text, self.name_text, self.score_text):
            mob.set_y(self.panel.get_y())
        super().__init__(self.panel, self.rank_text, self.name_text, self.score_text)


class Leaderboard(VGroup):
    """A ranked list. ``highlight`` is a row index or a rank string.

    Optional ``title`` and ``subtitle`` sit to the left, as in the Redis video.
    """

    def __init__(self, rows, highlight=None, title=None, subtitle=None, width=6.4):
        lines = VGroup()
        built = []
        for i, (rank, name, score) in enumerate(rows):
            picked = highlight == i or str(highlight) == str(rank)
            row = LeaderboardRow(
                rank, name, score, state="selected" if picked else "idle", width=width
            )
            built.append(row)
            lines.add(row)
        lines.arrange(DOWN, buff=0.08)
        self.rows = built
        parts = []
        self.heading = None
        if title:
            bits = [Headline(title, font_size=46, color=PURPLE)]
            if subtitle:
                bits.append(Title(subtitle, font_size=18))
            self.heading = VGroup(*bits).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
            self.heading.next_to(lines, LEFT, buff=0.55)
            self.heading.align_to(lines, UP)
            parts.append(self.heading)
        parts.append(lines)
        super().__init__(*parts)
        self.lines = lines


class Checklist(VGroup):
    """A verification panel.

    ``items`` is a list of ``(label, status)`` with status ``VALID``,
    ``PENDING``, or ``FAIL``.
    """

    def __init__(self, title, subject, items, width=7.6):
        header = VGroup(
            Title(title, font_size=18),
            Body(subject, font_size=28, color=TEXT),
        ).arrange(RIGHT, buff=0.16)
        inner_w = max(width - 0.72, header.get_width() + 0.2)
        blocks = []
        self.item_rows = []
        for label, status in items:
            key = str(status).upper()
            if key == "VALID":
                dot = icon("dot", color=PURPLE, height=0.16)
                status_color = PURPLE
            elif key == "FAIL":
                dot = icon("cross", color=ORANGE, height=0.16)
                status_color = ORANGE
            else:
                dot = icon("circle", color=DIM, height=0.16)
                status_color = DIM
            words = Body(label, font_size=24)
            words.next_to(dot, RIGHT, buff=0.16)
            line = VGroup(dot, words)
            flag = MonoText(key, font_size=18, color=status_color)
            rule = Rectangle(
                width=inner_w,
                height=0.012,
                fill_color="#333333",
                fill_opacity=1,
                stroke_width=0,
            )
            line.next_to(rule, DOWN, buff=0.12).align_to(rule, LEFT)
            flag.next_to(rule, DOWN, buff=0.12).align_to(rule, RIGHT)
            flag.set_y(line.get_y())
            block = VGroup(rule, line, flag)
            blocks.append(block)
            self.item_rows.append(block)
        rows = VGroup(*blocks) if blocks else VGroup()
        if len(blocks):
            rows.arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        everything = VGroup(header, rows).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        self.panel = Panel(
            everything.get_width() + 0.64,
            everything.get_height() + 0.5,
            state="muted",
            corner_radius=0.14,
        )
        self.panel.move_to(everything)
        super().__init__(self.panel, everything)


class KeyValueList(VGroup):
    """``copies: 3`` style lines, values in a brighter color."""

    def __init__(
        self, pairs, font_size=26, value_color=TEXT, key_color=MUTED, buff=0.12
    ):
        lines = []
        for key, value in pairs:
            row = VGroup(
                Body(f"{key}:", font_size=font_size, color=key_color),
                Body(str(value), font_size=font_size, color=value_color),
            ).arrange(RIGHT, buff=0.14)
            lines.append(row)
        super().__init__(*lines)
        self.arrange(DOWN, buff=buff, aligned_edge=LEFT)


class SpecCard(VGroup):
    """A header band plus key/value body. The Deployment card in the Kubernetes video.

    ``SpecCard("Deployment", "/registry/deployments/web", [("copies", "3")])``
    """

    def __init__(self, kind, path="", fields=None, kind_label="kind:", width=5.4):
        fields = fields or []
        kind_line = VGroup(
            Body(kind_label, font_size=26, color=MUTED),
            Body(kind, font_size=28, color=PURPLE, weight=BOLD),
        ).arrange(RIGHT, buff=0.12)
        path_text = MonoText(path, font_size=18, color=MUTED) if path else VGroup()
        header_bits = [kind_line]
        if path:
            header_bits.append(path_text)
        header = VGroup(*header_bits).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        body = KeyValueList(fields, font_size=26) if fields else VGroup()

        pad = 0.42
        width = max(width, header.get_width() + pad * 2, body.get_width() + pad * 2)
        header_h = header.get_height() + 0.4
        body_h = max(body.get_height() + 0.46, 0.4)
        self.header_panel = Panel(width, header_h, state="filled", corner_radius=0.14)
        self.body_panel = Panel(width, body_h, state="idle", corner_radius=0.0)
        self.body_panel.next_to(self.header_panel, DOWN, buff=-0.02)
        total = VGroup(self.header_panel, self.body_panel)
        self.stroke = Panel(
            width,
            total.get_height(),
            state="outline",
            corner_radius=0.14,
            fill_opacity=0,
        )
        self.stroke.move_to(total)
        header.move_to(self.header_panel).align_to(self.header_panel, LEFT).shift(
            RIGHT * pad
        )
        if len(body):
            body.move_to(self.body_panel).align_to(self.header_panel, LEFT).shift(
                RIGHT * pad
            )
        parts = [self.body_panel, self.header_panel, self.stroke, header]
        if len(body):
            parts.append(body)
        super().__init__(*parts)
        self.fields = body


class QuestionCard(VGroup):
    """A numbered prompt: ``01`` and a question, used as a row of three."""

    def __init__(self, number, question, width=3.15, height=2.05):
        self.panel = Panel(width, height, state="idle", corner_radius=0.12)
        self.number = MonoText(f"{int(number):02d}", font_size=32, color=PURPLE)
        self.question = Body(question, font_size=22, color=TEXT)
        if self.question.get_width() > width - 0.4:
            self.question.scale((width - 0.4) / self.question.get_width())
        text = VGroup(self.number, self.question).arrange(
            DOWN, buff=0.18, aligned_edge=LEFT
        )
        text.move_to(self.panel).align_to(self.panel, LEFT).shift(RIGHT * 0.24)
        super().__init__(self.panel, text)


class ServiceLogo(VGroup):
    """Colored tile, icon, name, and subtitle. The RDS-style lockup."""

    def __init__(
        self, name, icon_name="database", subtitle="", color="#2563EB", tile=0.95
    ):
        plate = Panel(tile, tile, state="accent", fill=color, corner_radius=tile * 0.22)
        glyph = icon(icon_name, color=WHITE, height=tile * 0.52)
        glyph.move_to(plate)
        mark = VGroup(plate, glyph)
        title = Headline(name, font_size=56, color=MUTED, weight="NORMAL")
        parts = [mark, title]
        self.subtitle = None
        if subtitle:
            self.subtitle = Body(subtitle, font_size=24, color=DIM)
            parts.append(self.subtitle)
        super().__init__(*parts)
        self.arrange(DOWN, buff=0.22)
        self.mark = mark


class InstanceCard(VGroup):
    """A cloud instance: name, type, address, and a footer such as ``running``."""

    def __init__(self, name, kind, address="", footer="", width=2.7, height=1.7):
        self.panel = Panel(width, height, state="idle", corner_radius=0.12)
        self.name_text = Title(name, font_size=16)
        self.kind_text = Body(kind, font_size=26)
        bits = [self.name_text, self.kind_text]
        self.address_text = None
        if address:
            self.address_text = MonoText(address, font_size=16, color=MUTED)
            bits.append(self.address_text)
        self.footer_text = None
        if footer:
            color = (
                GREEN
                if str(footer).lower() in {"running", "healthy", "active", "ready"}
                else MUTED
            )
            self.footer_text = Body(footer, font_size=18, color=color)
            bits.append(self.footer_text)
        stack = VGroup(*bits).arrange(DOWN, buff=0.08)
        if stack.get_width() > width - 0.3:
            stack.scale((width - 0.3) / stack.get_width())
        stack.move_to(self.panel)
        super().__init__(self.panel, stack)


class LabeledColumn(VGroup):
    """A heading over a stack of small cards, optional mono footer."""

    def __init__(self, title, items, footer=None, item_state="idle", width=2.5):
        self.title = Title(title, font_size=16)
        cards = VGroup(
            *[
                TextCard(
                    str(item), state=item_state, width=width, height=0.48, font_size=20
                )
                for item in items
            ]
        )
        cards.arrange(DOWN, buff=0.08)
        parts = [self.title, cards]
        self.footer_text = None
        if footer:
            self.footer_text = MonoText(footer, font_size=16, color=MUTED)
            parts.append(self.footer_text)
        super().__init__(*parts)
        self.arrange(DOWN, buff=0.14)
        self.cards = cards


class Comparison(VGroup):
    """Side-by-side columns. Each entry is ``(title, items, state)``."""

    def __init__(self, columns, buff=0.7):
        built = [
            LabeledColumn(title, items, item_state=state)
            for title, items, state in columns
        ]
        super().__init__(*built)
        self.arrange(RIGHT, buff=buff, aligned_edge=UP)


class JobQueue(VGroup):
    """A titled list of jobs. ``highlight`` paints one row violet."""

    def __init__(self, jobs, title="QUEUE", highlight=None, width=4.2):
        self.title = Title(title, font_size=16)
        rows = []
        for i, job in enumerate(jobs):
            state = "selected" if highlight == i else "ghost"
            row = TextCard(
                str(job), state=state, width=width, height=0.42, font_size=18, font=MONO
            )
            rows.append(row)
        self.rows = VGroup(*rows).arrange(DOWN, buff=0.06)
        super().__init__(self.title, self.rows)
        self.arrange(DOWN, buff=0.12, aligned_edge=LEFT)


class CounterStack(VGroup):
    """Stacked integers with one of them full-size. The single-counter graphic."""

    def __init__(self, values, active=None, font_size=42):
        if active is None and values:
            active = len(values) // 2
        mobs = []
        for i, value in enumerate(values):
            picked = i == active
            mobs.append(
                MonoText(
                    str(value),
                    font_size=font_size if picked else font_size * 0.62,
                    color=TEXT if picked else DIM,
                )
            )
        super().__init__(*mobs)
        self.arrange(DOWN, buff=0.08)


class PlanList(VGroup):
    """Terraform-style actions. Each item is ``(mark, text)`` with mark ``+``, ``~``, or ``-``."""

    def __init__(self, items, font_size=24):
        colors = {"+": GREEN, "~": PURPLE, "-": ORANGE, "!": ORANGE}
        rows = []
        for mark, text in items:
            tint = colors.get(mark, MUTED)
            flag = MonoText(str(mark), font_size=font_size, color=tint)
            words = MonoText(str(text), font_size=font_size, color=TEXT)
            words.next_to(flag, RIGHT, buff=0.16)
            rows.append(VGroup(flag, words))
        super().__init__(*rows)
        self.arrange(DOWN, buff=0.1, aligned_edge=LEFT)


class SplitPanel(VGroup):
    """Two adjacent plates, such as ``PLAIN TEXT`` beside ``ENCRYPTED``."""

    def __init__(
        self,
        left,
        right,
        left_state="ghost",
        right_state="filled",
        width=2.8,
        height=1.5,
    ):
        self.left_card = TextCard(left, state=left_state, width=width, height=height)
        self.right_card = TextCard(right, state=right_state, width=width, height=height)
        super().__init__(self.left_card, self.right_card)
        self.arrange(RIGHT, buff=0.12)


class CodeWindow(VGroup):
    """A window chrome around a code block: three dots, optional title, then the code."""

    def __init__(
        self, code, language="plain", title=None, theme="dark", width=6.6, font_size=22
    ):
        from .codeblocks import CodeBlock

        colors = {
            "dark": {
                "fill": "#1E1E1E",
                "bar": "#2A2A2A",
                "text": "#EDEDED",
                "keyword": PURPLE,
            },
            "light": {
                "fill": "#F6F3EC",
                "bar": "#E6E1D6",
                "text": "#1C1C1C",
                "keyword": "#6C4CFF",
            },
        }[theme]
        self.code = CodeBlock(
            code,
            language=language,
            width=width - 0.55,
            font_size=font_size,
            boxed=False,
            text_color=colors["text"],
            keyword_color=colors["keyword"],
        )
        bar_h = 0.42
        body_h = self.code.get_height() + 0.4
        self.bar = Panel(
            width,
            bar_h,
            fill=colors["bar"],
            state="idle",
            stroke_width=0,
            corner_radius=0.12,
        )
        self.body = Panel(
            width,
            body_h,
            fill=colors["fill"],
            state="idle",
            stroke_width=0,
            corner_radius=0.12,
        )
        self.body.next_to(self.bar, DOWN, buff=-0.08)
        dots = VGroup(
            icon("dot", color="#FF5F57", height=0.13),
            icon("dot", color="#FEBC2E", height=0.13),
            icon("dot", color="#28C840", height=0.13),
        ).arrange(RIGHT, buff=0.08)
        dots.align_to(self.bar, LEFT).shift(RIGHT * 0.2)
        dots.set_y(self.bar.get_y())
        parts = [self.body, self.bar, dots, self.code]
        self.title_text = None
        if title:
            self.title_text = Body(title, font_size=16, color=MUTED)
            self.title_text.move_to(self.bar)
            parts.append(self.title_text)
        self.code.next_to(self.bar, DOWN, buff=0.16)
        self.code.align_to(self.body, LEFT).shift(RIGHT * 0.28)
        stroke = Panel(
            width,
            VGroup(self.bar, self.body).get_height() - 0.06,
            state="muted",
            fill_opacity=0,
            corner_radius=0.12,
        )
        stroke.move_to(VGroup(self.bar, self.body))
        parts.append(stroke)
        super().__init__(*parts)
        self.stroke = stroke
