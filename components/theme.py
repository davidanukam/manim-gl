"""Colors, type, and card states shared by every component.

The palette is sampled from the explainer frames: background ``#171717``,
bright violet bars, deep-violet filled cells, and orange alarm fills.
"""

BG = "#171717"
TEXT = "#F4F4F4"
MUTED = "#9A9A9A"
DIM = "#6A6A6A"
WHITE = "#FFFFFF"

PURPLE = "#8D6AFD"
PURPLE_DEEP = "#3A2C64"
PURPLE_SOFT = "#241E38"
ORANGE = "#FE4800"
ORANGE_DEEP = "#6E2C0E"
RED = "#FF4B4B"
GREEN = "#3DDC97"
PINK = "#FF4D8D"
BLUE = "#3B82F6"
YELLOW = "#F5C451"

LINE = "#8D8D8D"
CARD = "#242424"
CARD_RAISED = "#2C2C2C"
STROKE = "#3C3C3C"
STROKE_SOFT = "#2E2E2E"

SANS = "Segoe UI"
MONO = "Consolas"

LIGHT = "LIGHT"
NORMAL = "NORMAL"
BOLD = "BOLD"

# fill, stroke, stroke_width, text, fill_opacity
STATES = {
    "idle": {
        "fill": "#242424",
        "stroke": "#3A3A3A",
        "stroke_width": 1.5,
        "text": TEXT,
        "fill_opacity": 1.0,
    },
    "ghost": {
        "fill": "#1E1E1E",
        "stroke": "#2C2C2C",
        "stroke_width": 1.25,
        "text": DIM,
        "fill_opacity": 1.0,
    },
    "muted": {
        "fill": "#1C1C1C",
        "stroke": "#4A4A4A",
        "stroke_width": 1.5,
        "text": MUTED,
        "fill_opacity": 1.0,
    },
    "filled": {
        "fill": PURPLE_DEEP,
        "stroke": "#4A3C78",
        "stroke_width": 1.5,
        "text": WHITE,
        "fill_opacity": 1.0,
    },
    "selected": {
        "fill": "#2A2158",
        "stroke": PURPLE,
        "stroke_width": 2.4,
        "text": WHITE,
        "fill_opacity": 1.0,
    },
    "outline": {
        "fill": "#1A1A1A",
        "stroke": PURPLE,
        "stroke_width": 2.4,
        "text": WHITE,
        "fill_opacity": 1.0,
    },
    "accent": {
        "fill": PURPLE,
        "stroke": PURPLE,
        "stroke_width": 0.0,
        "text": WHITE,
        "fill_opacity": 1.0,
    },
    "hot": {
        "fill": ORANGE,
        "stroke": ORANGE,
        "stroke_width": 0.0,
        "text": WHITE,
        "fill_opacity": 1.0,
    },
    "pink": {
        "fill": PINK,
        "stroke": PINK,
        "stroke_width": 0.0,
        "text": WHITE,
        "fill_opacity": 1.0,
    },
    "danger": {
        "fill": "#2A1616",
        "stroke": RED,
        "stroke_width": 2.2,
        "text": WHITE,
        "fill_opacity": 1.0,
    },
    "warn": {
        "fill": ORANGE_DEEP,
        "stroke": ORANGE,
        "stroke_width": 1.6,
        "text": "#FFB088",
        "fill_opacity": 1.0,
    },
    "ok": {
        "fill": "#143028",
        "stroke": GREEN,
        "stroke_width": 2.0,
        "text": WHITE,
        "fill_opacity": 1.0,
    },
    "plain": {
        "fill": BG,
        "stroke": BG,
        "stroke_width": 0.0,
        "text": TEXT,
        "fill_opacity": 0.0,
    },
}


def style_of(state):
    """Return a copy of a named state, or a custom state dict merged over ``idle``."""
    if isinstance(state, dict):
        merged = dict(STATES["idle"])
        merged.update(state)
        return merged
    if state not in STATES:
        known = ", ".join(STATES)
        raise KeyError(f"Unknown state {state!r}. Use one of: {known}")
    return dict(STATES[state])


def clamp_radius(width, height, radius):
    limit = min(width, height) * 0.5 - 1e-3
    if limit <= 0:
        return 0.0
    return max(0.0, min(radius, limit))


def mix_hex(a, b, t):
    """Blend two ``#RRGGBB`` colors. ``t`` is 0 at ``a`` and 1 at ``b``."""
    t = max(0.0, min(1.0, float(t)))

    def _rgb(h):
        h = h.lstrip("#")
        return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))

    ar, ag, ab = _rgb(a)
    br, bg, bb = _rgb(b)
    r = int(ar + (br - ar) * t)
    g = int(ag + (bg - ag) * t)
    bch = int(ab + (bb - ab) * t)
    return f"#{r:02x}{g:02x}{bch:02x}"


def use_background(scene):
    """Paint a scene with the same near-black used in the videos."""
    scene.camera.background_rgba = [23 / 255, 23 / 255, 23 / 255, 1.0]
    return scene
