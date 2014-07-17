# -*- coding: utf-8 -*-
"""verschemes.pep440 module

The PEP 440 verschemes module implements standard
`PEP 440 <http://legacy.python.org/dev/peps/pep-0440/>`_
`public <http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers>`_
versioning.  PEP 440
`local <http://legacy.python.org/dev/peps/pep-0440/#local-version-identifiers>`_
versions are not supported by this module; they are just public versions with a
hyphen and a numeric version (as implemented by the defaults in the base
`verschemes.Version` class) appended.

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from future.builtins import range
from future.builtins import super

from verschemes import SegmentDefinition as _SegmentDefinition
from verschemes import SegmentField as _SegmentField
from verschemes import Version as _Version


RELEASE_SEGMENTS = (
    EPOCH,
    RELEASE1,
    RELEASE2,
    RELEASE3,
    RELEASE4,
    RELEASE5,
    RELEASE6
) = tuple(range(7))

NONRELEASE_SEGMENTS = (
    PRE_RELEASE,
    POST_RELEASE,
    DEVELOPMENT
) = tuple(range(7, 10))

SEGMENTS = RELEASE_SEGMENTS + NONRELEASE_SEGMENTS


class Pep440Version(_Version):

    SEGMENT_DEFINITIONS = (
        _SegmentDefinition(
            name='epoch',
            optional=True,
            default=0,
        ),
        _SegmentDefinition(
            name='release1',
            default=0,
            separator=':',
        ),
        _SegmentDefinition(
            name='release2',
            optional=True,
            default=0,
        ),
        _SegmentDefinition(
            name='release3',
            optional=True,
            default=0,
        ),
        _SegmentDefinition(
            name='release4',
            optional=True,
            default=0,
        ),
        _SegmentDefinition(
            name='release5',
            optional=True,
            default=0,
        ),
        _SegmentDefinition(
            name='release6',
            optional=True,
            default=0,
        ),
        _SegmentDefinition(
            name='pre_release',
            optional=True,
            separator='',
            fields=(
                _SegmentField(
                    type=str,
                    name='level',
                    re_pattern='[abc]|rc',
                ),
                _SegmentField(
                    name='serial',
                ),
            ),
        ),
        _SegmentDefinition(
            name='post_release',
            optional=True,
            separator='.post',
        ),
        _SegmentDefinition(
            name='development',
            optional=True,
            separator='.dev',
        ),
    )

    @property
    def is_release(self):
        """Whether all of the non-release segments have no value.

        The non-release segments are named 'pre_release', 'post_release', and
        'development'.

        """
        return all(self[x] is None for x in NONRELEASE_SEGMENTS)

    def _render_exclude_defaults_callback(self, index, scope=None):
        if scope is None:
            scope = list(RELEASE_SEGMENTS)
            scope.remove(EPOCH)
        return super()._render_exclude_defaults_callback(index, scope)

    def _render_include_min_release_callback(self, index,
                                             min_release_segments):
        return RELEASE1 <= index < RELEASE1 + min_release_segments

    def render(self, exclude_defaults=True, include_callbacks=(),
               exclude_callbacks=(), min_release_segments=1):
        """Override to provide the `min_release_segments` option."""
        include_callbacks = list(include_callbacks)
        include_callbacks.append(
            (type(self)._render_include_min_release_callback,
             min_release_segments))
        return super().render(exclude_defaults, include_callbacks,
                              exclude_callbacks)
