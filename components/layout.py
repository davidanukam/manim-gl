"""Arrange helpers. Manim's ``arrange`` does the work; these name the intent."""

from manimlib import DOWN, LEFT, RIGHT, UP, VGroup


def hstack(*mobs, buff=0.3, aligned_edge=DOWN):
    """Place mobjects in a row. ``aligned_edge`` is ``UP``, ``DOWN``, or ``ORIGIN``."""
    group = VGroup(*mobs)
    group.arrange(RIGHT, buff=buff, aligned_edge=aligned_edge)
    return group


def vstack(*mobs, buff=0.28, aligned_edge=LEFT):
    """Place mobjects in a column."""
    group = VGroup(*mobs)
    group.arrange(DOWN, buff=buff, aligned_edge=aligned_edge)
    return group


def fit(mob, max_width=13.2, max_height=7.2):
    """Scale ``mob`` down so it sits inside a 16:9 frame with a small margin."""
    if mob.get_width() > max_width:
        mob.scale(max_width / mob.get_width())
    if mob.get_height() > max_height:
        mob.scale(max_height / mob.get_height())
    return mob


def card_row(labels, state="ghost", width=1.35, height=0.9, buff=0.14, **card_kwargs):
    """A horizontal run of text cards. Empty strings become blank plates."""
    from .primitives import TextCard

    cards = VGroup(
        *[
            TextCard(label, state=state, width=width, height=height, **card_kwargs)
            for label in labels
        ]
    )
    cards.arrange(RIGHT, buff=buff)
    return cards
