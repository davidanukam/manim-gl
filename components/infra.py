"""Maps, zones, tokens, policies, and the small infrastructure lockups."""

import numpy as np
from manimlib import DOWN, Dot, LEFT, RIGHT, UP, VGroup

from .cards import SideCard
from .icons import icon
from .primitives import Panel, Surround, TextCard
from .text import Body, Headline, MonoText, Title
from .theme import DIM, GREEN, LINE, MUTED, ORANGE, PINK, PURPLE, RED, TEXT

# Simplified continent outlines as (longitude, latitude) polygons.
_CONTINENTS = [
    # North America
    [
        (-168, 66),
        (-140, 70),
        (-100, 74),
        (-82, 72),
        (-68, 60),
        (-56, 52),
        (-64, 46),
        (-70, 42),
        (-74, 35),
        (-81, 25),
        (-90, 22),
        (-97, 16),
        (-105, 22),
        (-112, 24),
        (-115, 32),
        (-124, 40),
        (-124, 48),
        (-130, 54),
        (-152, 60),
        (-166, 64),
    ],
    # South America
    [
        (-78, 8),
        (-70, 12),
        (-60, 8),
        (-50, 2),
        (-35, -5),
        (-38, -16),
        (-40, -22),
        (-48, -28),
        (-58, -38),
        (-68, -52),
        (-74, -50),
        (-76, -42),
        (-72, -18),
        (-70, -8),
        (-78, -2),
        (-80, 4),
    ],
    # Europe
    [
        (-10, 36),
        (-9, 43),
        (-8, 52),
        (-5, 58),
        (5, 62),
        (10, 58),
        (12, 66),
        (24, 68),
        (30, 62),
        (28, 55),
        (22, 42),
        (16, 38),
        (10, 38),
        (-2, 36),
    ],
    # Africa
    [
        (-16, 22),
        (-12, 32),
        (-6, 35),
        (10, 37),
        (25, 32),
        (32, 31),
        (43, 12),
        (50, 10),
        (42, -12),
        (35, -26),
        (28, -33),
        (18, -34),
        (14, -22),
        (10, -6),
        (8, 4),
        (-4, 6),
        (-14, 12),
        (-16, 20),
    ],
    # Asia
    [
        (32, 36),
        (44, 40),
        (52, 36),
        (60, 45),
        (72, 42),
        (88, 26),
        (98, 16),
        (104, 8),
        (108, 14),
        (120, 22),
        (122, 32),
        (128, 36),
        (140, 42),
        (142, 52),
        (135, 58),
        (160, 64),
        (180, 66),
        (180, 70),
        (100, 72),
        (70, 74),
        (60, 68),
        (42, 68),
        (36, 56),
        (32, 44),
    ],
    # Australia
    [
        (114, -22),
        (124, -16),
        (136, -14),
        (142, -12),
        (146, -18),
        (153, -26),
        (150, -36),
        (146, -39),
        (138, -36),
        (130, -32),
        (116, -34),
        (114, -28),
    ],
    # Greenland
    [
        (-62, 68),
        (-48, 62),
        (-42, 70),
        (-22, 74),
        (-20, 80),
        (-40, 83),
        (-55, 78),
        (-68, 76),
        (-64, 70),
    ],
]


def _inside(x, y, poly):
    inside = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and (
            x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-9) + xi
        ):
            inside = not inside
        j = i
    return inside


def _on_land(lon, lat):
    return any(_inside(lon, lat, poly) for poly in _CONTINENTS)


class WorldMap(VGroup):
    """A dotted world map. ``pins`` is a list of ``(name, longitude, latitude)``.

    ``WorldMap([("Sydney", 151, -34), ("Virginia", -77, 39)])``
    """

    def __init__(self, pins=None, width=10.5, height=4.6):
        self.map_width = width
        self.map_height = height
        dots = VGroup()
        for lat in range(72, -58, -7):
            for lon in range(-176, 180, 8):
                if not _on_land(lon, lat):
                    continue
                dot = Panel(
                    0.055,
                    0.055,
                    fill="#3A3A3A",
                    stroke_width=0,
                    corner_radius=0.02,
                    state="ghost",
                )
                dot.move_to(self.project(lon, lat))
                dots.add(dot)
        parts = [dots]
        self.pins = []
        for pin in pins or []:
            name, lon, lat = pin[0], pin[1], pin[2]
            point = self.project(lon, lat)
            mark = Dot(point=point, radius=0.055, fill_color=PURPLE, stroke_width=0)
            label = Body(str(name), font_size=16, color=TEXT)
            label.next_to(mark, UP, buff=0.06)
            parts.extend([mark, label])
            self.pins.append(mark)
        super().__init__(*parts)
        self.dots = dots

    def project(self, lon, lat):
        """Equirectangular projection into the map's width and height."""
        lat_top, lat_bot = 78, -58
        x = (lon / 180.0) * (self.map_width / 2)
        y = ((lat - (lat_top + lat_bot) / 2) / (lat_top - lat_bot)) * self.map_height
        return np.array([x, y, 0.0])


class Zone(VGroup):
    """A titled frame. Children are arranged in a row unless you pass one group."""

    def __init__(self, title, *contents, buff=0.28, arrange=True):
        body = VGroup(*contents)
        if arrange and len(contents) > 1:
            body.arrange(RIGHT, buff=0.28)
        self.frame = Surround(body, buff=buff, state="outline", corner_radius=0.14)
        self.title = Title(title, font_size=16)
        self.title.next_to(self.frame, UP, buff=0.1).align_to(self.frame, LEFT)
        super().__init__(self.frame, self.title)
        self.body = body


class AccessToken(VGroup):
    """A token string with a violet underline on its tail and an expiry caption."""

    def __init__(self, token, expires=None, font_size=22):
        from manimlib import Line

        self.token_text = MonoText(token, font_size=font_size, color=TEXT)
        underline_w = max(self.token_text.get_width() * 0.38, 0.4)
        self.underline = Line(
            np.array([0, 0, 0]),
            np.array([underline_w, 0, 0]),
            stroke_color=PURPLE,
            stroke_width=3,
        )
        self.underline.next_to(self.token_text, DOWN, buff=0.08).align_to(
            self.token_text, RIGHT
        )
        parts = [self.token_text, self.underline]
        self.expires_text = None
        if expires:
            self.expires_text = Title(expires, font_size=14, color=MUTED)
            self.expires_text.next_to(self.underline, DOWN, buff=0.1).align_to(
                self.token_text, RIGHT
            )
            parts.append(self.expires_text)
        super().__init__(*parts)


class PolicyLine(VGroup):
    """``who``  is allowed to  ``what``. Set ``denied=True`` to add a deny mark."""

    def __init__(self, who, what, action="is allowed to", denied=False):
        self.who_card = TextCard(
            who, state="outline", width=None, height=0.7, font_size=22
        )
        self.action_text = Body(action, font_size=24, color=MUTED)
        self.what_card = TextCard(
            what, state="filled", width=None, height=0.7, font_size=22
        )
        row = VGroup(self.who_card, self.action_text, self.what_card).arrange(
            RIGHT, buff=0.22
        )
        parts = [row]
        self.deny = None
        if denied:
            self.deny = DenyStamp()
            self.deny.scale(0.45).next_to(row, DOWN, buff=0.25)
            parts.append(self.deny)
        super().__init__(*parts)


class DenyStamp(VGroup):
    """A large DENY with a ban icon."""

    def __init__(self, text="Deny"):
        self.mark = icon("ban", color=RED, height=0.55)
        self.word = Headline(text, font_size=64, color=TEXT, weight="NORMAL")
        self.mark.next_to(self.word, UP, buff=0.12)
        super().__init__(self.mark, self.word)


class ReplicaPair(VGroup):
    """Two striped cards, the primary/replica (or failed/promoted) pair."""

    def __init__(
        self,
        left,
        right,
        left_color=None,
        right_color=None,
        left_state="idle",
        right_state="idle",
    ):
        from .theme import BLUE

        self.left_card = SideCard(
            left, stripe=left_color or BLUE, state=left_state, width=2.6, height=1.2
        )
        self.right_card = SideCard(
            right, stripe=right_color or RED, state=right_state, width=2.6, height=1.2
        )
        super().__init__(self.left_card, self.right_card)
        self.arrange(RIGHT, buff=0.8)


class ClusterMark(VGroup):
    """Three overlapping hexagons in green, pink, and violet."""

    def __init__(self, height=0.9):
        from manimlib import RegularPolygon

        colors = (GREEN, PINK, PURPLE)
        tiles = VGroup()
        for i, color in enumerate(colors):
            tile = RegularPolygon(
                n=6,
                radius=0.34,
                start_angle=np.pi / 6,
                fill_color=color,
                fill_opacity=1,
                stroke_width=0,
            )
            angle = i * 2 * np.pi / 3 - np.pi / 2
            tile.shift(0.2 * np.array([np.cos(angle), np.sin(angle), 0]))
            tiles.add(tile)
        super().__init__(tiles)
        self.set_height(height)


class LogoLockup(VGroup):
    """A mark beside a word, with an optional tracked subtitle."""

    def __init__(self, word, mark=None, subtitle=None):
        self.mark = mark if mark is not None else ClusterMark()
        self.word = Headline(word, font_size=64, weight="NORMAL")
        row = VGroup(self.mark, self.word).arrange(RIGHT, buff=0.18)
        parts = [row]
        self.subtitle = None
        if subtitle:
            self.subtitle = Title(subtitle, font_size=16)
            self.subtitle.next_to(row, DOWN, buff=0.12)
            parts.append(self.subtitle)
        super().__init__(*parts)
