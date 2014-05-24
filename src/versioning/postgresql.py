# -*- coding: utf-8 -*-
"""versioning.postgresql module

The PostgreSQL versioning module implements standard
`PostgreSQL <http://www.postgresql.org/>`_
`versioning <http://www.postgresql.org/support/versioning/>`__.

"""

from . import SegmentDefinition as _SegmentDefinition
from . import Version as _Version


SEGMENTS = (MAJOR1, MAJOR2, MINOR) = range(3)


class PgMajorVersion(_Version):

    SEGMENT_DEFINITIONS = (
        _SegmentDefinition(),
        _SegmentDefinition(),
    )

    @property
    def major_version(self):
        """Return a new `PgMajorVersion` with the object's values.

        This is mainly useful in subclasses.

        """
        return PgMajorVersion(self[MAJOR1], self[MAJOR2])


class PgVersion(PgMajorVersion):

    SEGMENT_DEFINITIONS = PgMajorVersion.SEGMENT_DEFINITIONS + (
        _SegmentDefinition(optional=True, default=0),
    )
