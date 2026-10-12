"""Trees, flows, rings, and the links between nodes."""

import numpy as np
from manimlib import DOWN, LEFT, Line, Mobject, PI, RIGHT, UP, VGroup

from .primitives import Panel, TextCard, connect
from .text import Body, Headline, Title
from .theme import DIM, LINE, MUTED, PURPLE, TEXT


def _as_card(item, state="idle", width=2.0, height=0.72):
    if isinstance(item, Mobject):
        return item
    return TextCard(str(item), state=state, width=width, height=height, font_size=24)


class Flow(VGroup):
    """Nodes in a row or column, joined by lines.

    Items are strings or mobjects. ``direction`` is ``RIGHT`` or ``DOWN``.
    """

    def __init__(
        self,
        items,
        states=None,
        arrow=False,
        buff=0.7,
        direction=RIGHT,
        node_width=2.05,
        node_height=0.72,
        color=LINE,
    ):
        nodes = []
        for i, item in enumerate(items):
            state = "idle" if not states else states[i]
            nodes.append(
                _as_card(item, state=state, width=node_width, height=node_height)
            )
        row = VGroup(*nodes)
        if len(nodes):
            row.arrange(direction, buff=buff)
        links = VGroup()
        for left, right in zip(nodes, nodes[1:]):
            links.add(connect(left, right, arrow=arrow, color=color))
        super().__init__(links, row)
        self.nodes = nodes
        self.links = links


class StackFlow(Flow):
    """The same as :class:`Flow`, stacked downward. SQL → bytecode → pager."""

    def __init__(self, items, **kwargs):
        kwargs.setdefault("direction", DOWN)
        kwargs.setdefault("buff", 0.55)
        super().__init__(items, **kwargs)


class Fanout(VGroup):
    """One hub and several spokes.

    ``incoming=True`` draws the spokes on the left, pointing at the hub
    (producers into Kafka). Otherwise the hub feeds the spokes.
    """

    def __init__(
        self,
        hub,
        spokes,
        incoming=False,
        hub_state="filled",
        spoke_state="idle",
        gap=1.5,
        color=LINE,
    ):
        self.hub = _as_card(hub, state=hub_state, width=1.8, height=1.3)
        self.spokes = VGroup(
            *[_as_card(s, state=spoke_state, width=2.2, height=0.58) for s in spokes]
        )
        self.spokes.arrange(DOWN, buff=0.22)
        if incoming:
            self.spokes.next_to(self.hub, LEFT, buff=gap)
        else:
            self.spokes.next_to(self.hub, RIGHT, buff=gap)
        self.hub.set_y(self.spokes.get_y())
        links = VGroup()
        for spoke in self.spokes:
            links.add(
                connect(
                    spoke if incoming else self.hub,
                    self.hub if incoming else spoke,
                    color=color,
                )
            )
        super().__init__(links, self.hub, self.spokes)
        self.links = links


def _normalize(spec):
    if isinstance(spec, str):
        return {"label": spec}
    return dict(spec)


class Tree(VGroup):
    """An orthogonal tree.

    A node is a string or a dict::

        Tree({
            "label": "milo",
            "state": "outline",
            "children": ["finn", {"label": "sara", "children": ["tara", "vera"]}],
        })

    ``link`` on a child colors the drop-line from its parent.
    """

    def __init__(
        self, spec, level_gap=0.7, sibling_buff=0.35, title=None, line_color=LINE
    ):
        group = _layout(_normalize(spec), level_gap, sibling_buff, line_color)
        parts = [group]
        if title:
            heading = Title(title, font_size=20)
            heading.next_to(group, UP, buff=0.28)
            parts = [group, heading]
        super().__init__(*parts)
        self.root = group


def _layout(spec, level_gap, sibling_buff, line_color):
    label = spec.get("label", "")
    card = (
        TextCard(
            label,
            state=spec.get("state", "idle"),
            width=spec.get("width"),
            height=spec.get("height", 0.64),
            font_size=spec.get("font_size", 24),
            font=spec.get("font"),
        )
        if spec.get("font")
        else TextCard(
            label,
            state=spec.get("state", "idle"),
            width=spec.get("width"),
            height=spec.get("height", 0.64),
            font_size=spec.get("font_size", 24),
        )
    )
    children = [_normalize(child) for child in spec.get("children") or []]
    if not children:
        card.link_color = spec.get("link")
        return card

    kids = VGroup(
        *[_layout(child, level_gap, sibling_buff, line_color) for child in children]
    )
    kids.arrange(RIGHT, buff=sibling_buff, aligned_edge=UP)
    card.set_x(kids.get_x())
    card.set_y(kids.get_top()[1] + level_gap + card.get_height() / 2)

    lines = VGroup()
    parent_bottom = card.get_bottom()
    if len(kids) == 1:
        color = children[0].get("link", line_color)
        lines.add(
            Line(
                parent_bottom,
                [kids[0].get_x(), kids[0].get_top()[1], 0],
                stroke_color=color,
                stroke_width=2,
            )
        )
    else:
        bus_y = (parent_bottom[1] + kids.get_top()[1]) / 2
        lines.add(
            Line(
                parent_bottom,
                [card.get_x(), bus_y, 0],
                stroke_color=line_color,
                stroke_width=2,
            )
        )
        left_x = kids[0].get_x()
        right_x = kids[-1].get_x()
        lines.add(
            Line(
                [left_x, bus_y, 0],
                [right_x, bus_y, 0],
                stroke_color=line_color,
                stroke_width=2,
            )
        )
        for child, group in zip(children, kids):
            color = child.get("link", line_color)
            lines.add(
                Line(
                    [group.get_x(), bus_y, 0],
                    [group.get_x(), group.get_top()[1], 0],
                    stroke_color=color,
                    stroke_width=2.4 if color != line_color else 2,
                )
            )
    card.link_color = spec.get("link")
    return VGroup(lines, kids, card)


class HashRing(VGroup):
    """Shards around a circle. ``highlight`` is an index; ``center`` is the label inside."""

    def __init__(self, labels, highlight=None, center=None, caption=None, radius=2.15):
        from manimlib import Arc, Circle

        self.ring = Circle(
            radius=radius, stroke_color="#3A3A3A", stroke_width=3, fill_opacity=0
        )
        parts = [self.ring]
        count = max(len(labels), 1)
        step = 2 * np.pi / count
        self.ticks = []
        self.labels = []
        for i, label in enumerate(labels):
            angle = np.pi / 2 - i * step
            point = np.array([radius * np.cos(angle), radius * np.sin(angle), 0])
            picked = highlight == i
            tick = Panel(
                0.16, 0.16, state="accent" if picked else "ghost", corner_radius=0.04
            )
            tick.move_to(point)
            word = Body(str(label), font_size=18, color=PURPLE if picked else MUTED)
            outward = point / max(np.linalg.norm(point), 1e-6)
            word.move_to(point + outward * 0.38)
            parts.extend([tick, word])
            self.ticks.append(tick)
            self.labels.append(word)
        self.arc = None
        if highlight is not None and labels:
            angle = np.pi / 2 - highlight * step
            self.arc = Arc(
                start_angle=angle - step / 2,
                angle=step,
                radius=radius,
                stroke_color=PURPLE,
                stroke_width=7,
            )
            parts.append(self.arc)
        self.center_text = None
        self.caption_text = None
        if center:
            self.center_text = Headline(str(center), font_size=32)
            parts.append(self.center_text)
        if caption:
            self.caption_text = Title(caption, font_size=16)
            self.caption_text.next_to(self.ring, DOWN, buff=0.7)
            parts.append(self.caption_text)
        super().__init__(*parts)


class HashAxis(VGroup):
    """A consistent-hashing line. Nodes are ``(label, position)`` with position in 0..1."""

    def __init__(self, nodes, width=8.5, color=PURPLE):
        from manimlib import Dot

        self.rule = Line(
            LEFT * width / 2, RIGHT * width / 2, stroke_color="#3A3A3A", stroke_width=3
        )
        parts = [self.rule]
        self.nodes = []
        for label, position in nodes:
            x = -width / 2 + width * float(position)
            dot = Dot(point=[x, 0, 0], radius=0.07, fill_color=color, stroke_width=0)
            word = Body(str(label), font_size=18, color=TEXT)
            word.next_to(dot, UP, buff=0.14)
            parts.extend([dot, word])
            self.nodes.append(dot)
        super().__init__(*parts)
