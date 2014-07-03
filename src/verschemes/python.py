# -*- coding: utf-8 -*-
"""verschemes.python module

The Python versioning module implements standard
`Python <https://www.python.org/>`_
`versioning <https://docs.python.org/3/faq/general.html#how-does-the-python-version-numbering-scheme-work>`__.

"""

from . import SegmentDefinition as _SegmentDefinition
from . import SegmentField as _SegmentField
from . import Version as _Version


SEGMENTS = (MAJOR, MINOR, MICRO, SUFFIX) = range(4)


class PythonMajorVersion(_Version):

    SEGMENT_DEFINITIONS = (
        _SegmentDefinition(),
    )

    @property
    def major_version(self):
        """Return a new `PythonMajorVersion` with the object's values.

        This is mainly useful in subclasses.

        """
        return PythonMajorVersion(self[MAJOR])


class PythonMinorVersion(PythonMajorVersion):

    SEGMENT_DEFINITIONS = PythonMajorVersion.SEGMENT_DEFINITIONS + (
        _SegmentDefinition(),
    )

    @property
    def minor_version(self):
        """Return a new `PythonMinorVersion` with the object's values.

        This is mainly useful in subclasses.

        """
        return PythonMinorVersion(self[MAJOR], self[MINOR])


class PythonMicroVersion(PythonMinorVersion):

    SEGMENT_DEFINITIONS = PythonMinorVersion.SEGMENT_DEFINITIONS + (
        _SegmentDefinition(
            optional=True
        ),
    )

    @property
    def micro_version(self):
        """Return a new `PythonMicroVersion` with the object's values.

        This is mainly useful in subclasses.

        """
        return PythonMicroVersion(self[MAJOR], self[MINOR], self[MICRO])


class PythonVersion(PythonMicroVersion):

    SEGMENT_DEFINITIONS = PythonMicroVersion.SEGMENT_DEFINITIONS + (
        _SegmentDefinition(
            optional=True,
            separator='',
            fields=(
                _SegmentField(
                    type=str,
                    name='releaselevel',
                    re_pattern='[+abc]',
                ),
                _SegmentField(
                    name='serial',
                    re_pattern='(?<=[+])|(?<![+])(?:0|[1-9][0-9]*)',
                    render=lambda x: "" if x is None else str(x),
                ),
            ),
        ),
    )

    @property
    def is_nondevelopment(self):
        """Whether this version represents a non-development release.

        This simply says whether it is equivalent to its `major_version`; that
        is, whether the `SUFFIX`-index value is `None`.

        """
        return self[SUFFIX] is None
