"""Monospace blocks with a small keyword highlighter."""

import re

from manimlib import DOWN, LEFT, RIGHT, VGroup

from .primitives import Panel
from .text import MonoText
from .theme import DIM, MONO, MUTED, ORANGE, PURPLE, TEXT

KEYWORDS = {
    "sql": {
        "select",
        "from",
        "where",
        "insert",
        "into",
        "update",
        "set",
        "delete",
        "create",
        "table",
        "index",
        "values",
        "and",
        "or",
        "not",
        "join",
        "left",
        "right",
        "inner",
        "on",
        "group",
        "by",
        "order",
        "limit",
        "like",
        "in",
        "is",
        "null",
        "primary",
        "key",
        "begin",
        "commit",
        "as",
        "distinct",
        "between",
        "having",
        "union",
        "all",
        "drop",
        "alter",
        "add",
    },
    "python": {
        "def",
        "class",
        "return",
        "import",
        "from",
        "if",
        "else",
        "elif",
        "for",
        "while",
        "in",
        "not",
        "and",
        "or",
        "none",
        "true",
        "false",
        "with",
        "as",
        "try",
        "except",
        "lambda",
        "yield",
        "pass",
        "break",
        "continue",
    },
    "hcl": {
        "resource",
        "variable",
        "provider",
        "module",
        "output",
        "locals",
        "data",
        "for",
        "in",
        "each",
        "if",
        "else",
        "true",
        "false",
    },
    "shell": set(),
    "plain": set(),
}

_TOKEN = re.compile(r"\".*?\"|'.*?'|\s+|\w+|[^\s]")


def _tokens(line, language, text_color, keyword_color):
    keys = KEYWORDS.get(language, set())
    stripped = line.lstrip()
    if (
        stripped.startswith("#")
        or stripped.startswith("--")
        or stripped.startswith("//")
    ):
        return [(line, DIM)]
    parts = []
    for token in _TOKEN.findall(line):
        if token.startswith(("'", '"')):
            parts.append((token, ORANGE))
        elif token.lower() in keys:
            parts.append((token, keyword_color))
        elif re.fullmatch(r"\d+", token):
            parts.append((token, keyword_color))
        else:
            parts.append((token, text_color))
    return parts or [(" ", text_color)]


_SPACE_WIDTH = {}


def _space_width(font_size):
    """Width of one Consolas space at this size. A space glyph has no ink, so measure it."""
    if font_size not in _SPACE_WIDTH:
        pair = MonoText("n n", font_size=font_size)
        tight = MonoText("nn", font_size=font_size)
        _SPACE_WIDTH[font_size] = max(pair.get_width() - tight.get_width(), 0.04)
    return _SPACE_WIDTH[font_size]


def _line_mobject(line, language, font_size, text_color, keyword_color):
    from manimlib import Rectangle

    pieces = VGroup()
    for token, color in _tokens(line, language, text_color, keyword_color):
        if token.strip() == "" and token != "":
            gap = Rectangle(
                width=_space_width(font_size) * len(token),
                height=0.04,
                stroke_width=0,
                fill_opacity=0,
            )
            pieces.add(gap)
            continue
        pieces.add(MonoText(token if token else " ", font_size=font_size, color=color))
    if len(pieces) == 0:
        pieces.add(MonoText(" ", font_size=font_size, color=text_color))
    pieces.arrange(RIGHT, buff=0)
    return pieces


class CodeBlock(VGroup):
    """A block of code. ``language`` is ``sql``, ``python``, ``hcl``, ``shell``, or ``plain``.

    ``boxed=False`` returns only the lines, so a :class:`CodeWindow` can supply the chrome.
    """

    def __init__(
        self,
        source,
        language="plain",
        width=6.2,
        font_size=22,
        boxed=True,
        text_color=TEXT,
        keyword_color=PURPLE,
        state="idle",
    ):
        if isinstance(source, str):
            lines = source.splitlines() or [""]
        else:
            lines = list(source)
        rendered = [
            _line_mobject(
                line if line else " ", language, font_size, text_color, keyword_color
            )
            for line in lines
        ]
        self.lines = VGroup(*rendered)
        self.lines.arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        if self.lines.get_width() > width:
            self.lines.scale(width / self.lines.get_width())
        if not boxed:
            super().__init__(self.lines)
            return
        self.panel = Panel(
            max(width, self.lines.get_width() + 0.5),
            self.lines.get_height() + 0.4,
            state=state,
            corner_radius=0.12,
        )
        self.lines.move_to(self.panel).align_to(self.panel, LEFT).shift(RIGHT * 0.24)
        super().__init__(self.panel, self.lines)


class Terminal(VGroup):
    """A prompt and a command, with optional output lines underneath.

    ``Terminal("terraform plan", prompt="$")``
    """

    def __init__(
        self, command, prompt="$", output=None, font_size=26, prompt_color=MUTED
    ):
        self.prompt_text = MonoText(prompt, font_size=font_size, color=prompt_color)
        self.command_text = MonoText(command, font_size=font_size, color=TEXT)
        self.command_text.next_to(self.prompt_text, RIGHT, buff=0.16)
        row = VGroup(self.prompt_text, self.command_text)
        parts = [row]
        self.output_lines = None
        if output:
            if isinstance(output, str):
                output = output.splitlines()
            self.output_lines = VGroup(
                *[
                    MonoText(line, font_size=font_size * 0.85, color=DIM)
                    for line in output
                ]
            )
            self.output_lines.arrange(DOWN, buff=0.06, aligned_edge=LEFT)
            self.output_lines.next_to(row, DOWN, buff=0.12).align_to(row, LEFT)
            parts.append(self.output_lines)
        super().__init__(*parts)
