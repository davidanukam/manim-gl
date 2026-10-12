"""Turn a component method into an animation.

``mobject.animate.scale(2)`` already works, because scale only moves points.
Methods that add a row or change a label build a new component and transform
into it. After the animation, the same Python object holds the new contents,
so a later ``animate.add`` sees the row that just appeared.

One of these methods per ``self.play`` call. Scale, shift, and ``set_color``
still chain with each other::

    self.play(card.animate.scale(1.2).shift(LEFT))
    self.play(checklist.animate.add(("Domain matches", "VALID")), run_time=1.5)
"""

import numpy as np
from manimlib import Mobject, Transform, UL, VGroup


_SKIP_ATTRS = {
    "submobjects",
    "parents",
    "family",
    "target",
    "saved_state",
    "updaters",
    "shader_wrapper",
    "data",
    "uniforms",
    "bounding_box",
    "points",
    "locked_data_keys",
    "locked_uniform_keys",
    "const_data_keys",
}


def copy_plain(value):
    """Copy lists, dicts, and arrays. Leave strings and numbers as they are."""
    if isinstance(value, np.ndarray):
        return value.copy()
    if isinstance(value, list):
        return [copy_plain(item) for item in value]
    if isinstance(value, tuple):
        return tuple(copy_plain(item) for item in value)
    if isinstance(value, set):
        return {copy_plain(item) for item in value}
    if isinstance(value, dict):
        return {copy_plain(key): copy_plain(item) for key, item in value.items()}
    return value


def _all_mobjects(items):
    return bool(items) and all(isinstance(item, Mobject) for item in items)


def place(fresh, mob, anchor):
    """Line ``fresh`` up with ``mob`` so the part that should stay put does."""
    if anchor == "top":
        fresh.shift(mob.get_top() - fresh.get_top())
    elif anchor == "top_left":
        fresh.shift(mob.get_corner(UL) - fresh.get_corner(UL))
    elif anchor == "left":
        fresh.shift(mob.get_left() - fresh.get_left())
        fresh.shift(np.array([0.0, mob.get_center()[1] - fresh.get_center()[1], 0.0]))
    elif anchor == "bottom":
        fresh.shift(mob.get_bottom() - fresh.get_bottom())
        fresh.set_x(mob.get_x())
    else:
        fresh.move_to(mob.get_center())
    return fresh


def _unlock(mob):
    for part in mob.get_family():
        part.locked_data_keys = set()
        part.locked_uniform_keys = set()
        if hasattr(part, "const_data_keys"):
            part.const_data_keys = set()


def _contains_family(value, family):
    if isinstance(value, Mobject):
        return value in family
    if isinstance(value, (list, tuple)):
        return any(_contains_family(item, family) for item in value)
    if isinstance(value, dict):
        return any(_contains_family(item, family) for item in value.values())
    return False


def _remap(value, source, family_from, family_to):
    if isinstance(value, Mobject):
        if value is source:
            return family_to[0]
        if value in family_from:
            return family_to[family_from.index(value)]
        return value
    if isinstance(value, list):
        return [_remap(item, source, family_from, family_to) for item in value]
    if isinstance(value, tuple):
        return tuple(_remap(item, source, family_from, family_to) for item in value)
    if isinstance(value, dict):
        return {
            _remap(key, source, family_from, family_to): _remap(
                item, source, family_from, family_to
            )
            for key, item in value.items()
        }
    return value


def _take_root(dest, source):
    if dest.get_num_points() != source.get_num_points():
        dest.resize_points(source.get_num_points())
    if source.get_num_points():
        dest.set_data(source.data)
    dest.set_uniforms(source.uniforms)
    dest.bounding_box[:] = source.bounding_box
    dest.shader_folder = source.shader_folder
    dest.texture_paths = source.texture_paths
    dest.depth_test = source.depth_test
    if hasattr(source, "render_primitive"):
        dest.render_primitive = source.render_primitive
    dest.shader_wrapper = None
    dest._needs_new_bounding_box = True


def install(dest, fresh):
    """Give ``dest`` the same drawn pieces as ``fresh``, without padding blanks."""
    _unlock(dest)
    source = fresh.copy()
    _take_root(dest, source)
    children = [child.copy() for child in source.submobjects]
    dest.clear()
    Mobject.add(dest, *children)
    family_from = source.get_family()
    family_to = dest.get_family()
    if len(family_from) != len(family_to):
        return dest
    for name, value in list(source.__dict__.items()):
        if name in _SKIP_ATTRS or name.startswith("_data"):
            continue
        if not _contains_family(value, family_from):
            continue
        setattr(dest, name, _remap(value, source, family_from, family_to))
    dest.refresh_bounding_box()
    return dest


class StateTransform(Transform):
    """Transform into ``fresh``, then keep its plain fields on the original."""

    def __init__(self, mobject, fresh, state, **kwargs):
        self._clean = fresh.copy()
        self._state = state
        super().__init__(mobject, fresh, **kwargs)

    def finish(self):
        super().finish()
        for key, value in self._state.items():
            setattr(self.mobject, key, copy_plain(value))
        install(self.mobject, self._clean)


def _state_from(fresh, keys):
    return {key: copy_plain(getattr(fresh, key)) for key in keys}


def adopt(mobject, fresh, keys, anchor):
    place(fresh, mobject, anchor)
    for key, value in _state_from(fresh, keys).items():
        setattr(mobject, key, value)
    install(mobject, fresh)
    return mobject


def spawn(mobject, fresh, keys, anchor):
    place(fresh, mobject, anchor)
    return StateTransform(mobject, fresh, _state_from(fresh, keys))


def _during_init(mobject, args):
    return _all_mobjects(args) and len(mobject.submobjects) == 0


def animated(*keys, anchor="center", mobject_safe=False):
    """Decorator for a method that returns a new component.

    The body builds the next version and returns it. Calling the method
    updates the component immediately. ``animate.method(...)`` plays the
    change. ``mobject_safe=True`` is for methods named ``add``, so the
    group can still be constructed from mobjects.
    """

    def decorate(builder):
        def method(self, *args, **kwargs):
            if mobject_safe and _during_init(self, args):
                return VGroup.add(self, *args)
            fresh = builder(self, *args, **kwargs)
            return adopt(self, fresh, keys, anchor)

        def override(mobject, *args, **kwargs):
            if mobject_safe and _during_init(mobject, args):
                fresh = mobject.copy()
                VGroup.add(fresh, *args)
                return StateTransform(mobject, fresh, {})
            fresh = builder(mobject, *args, **kwargs)
            return spawn(mobject, fresh, keys, anchor)

        method._override_animate = override
        method.__name__ = builder.__name__
        method.__doc__ = builder.__doc__
        return method

    return decorate


def inplace(*keys):
    """Decorator for a method that edits this component's own pieces.

    ``animate.method(...)`` copies the component, runs the method on the
    copy, and transforms into that copy.
    """

    def decorate(fn):
        def override(mobject, *args, **kwargs):
            target = mobject.copy()
            fn(target, *args, **kwargs)
            return StateTransform(mobject, target, _state_from(target, keys))

        fn._override_animate = override
        return fn

    return decorate
