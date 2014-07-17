# -*- coding: utf-8 -*-
"""verschemes.xorg module

The X.org verschemes module implements the standard
`X.org <http://www.x.org/>`_ `version number scheme
<http://www.x.org/wiki/Development/Documentation/VersionNumberScheme/>`_.

An added rule is to extend the patch number's pre-full-release value (99) to
the minor number as well when preparing for a [major].0 full release.

"""

from verschemes import SegmentDefinition as _SegmentDefinition
from verschemes import Version as _Version


SEGMENTS = (
    MAJOR,
    MINOR,
    PATCH,
    SNAPSHOT,
) = tuple(range(4))

PRE_FULL_RELEASE = 99
BRANCH_START_SNAPSHOT = 900


class XorgVersion(_Version):

    SEGMENT_DEFINITIONS = (
        _SegmentDefinition(
            name='major',
        ),
        _SegmentDefinition(
            name='minor',
            default=0,
        ),
        _SegmentDefinition(
            name='patch',
            default=0,
        ),
        _SegmentDefinition(
            name='snapshot',
            optional=True,
            default=0,
        ),
    )

    def validate(self):
        """Override for version scheme validations."""
        if self.is_pre_full_release:
            if self.is_release:
                raise ValueError(
                    "Pre-full-release versions (patch = {}) must have a "
                    "snapshot > 0."
                    .format(PRE_FULL_RELEASE))
        elif self.is_development:
            raise ValueError(
                "Development versions (0 < snapshot < {}) are only valid for "
                "development branches (patch = {})."
                .format(BRANCH_START_SNAPSHOT, PRE_FULL_RELEASE))

    @property
    def is_release(self):
        """Whether the version identifies a release."""
        return (self[SNAPSHOT] or 0) == 0

    @property
    def is_full_release(self):
        """Whether the version identifies a full release."""
        return self.is_release and self[PATCH] == 0

    @property
    def is_pre_full_release(self):
        """Whether the version is between feature freeze and a full release."""
        return self[PATCH] == PRE_FULL_RELEASE

    @property
    def is_bugfix_release(self):
        """Whether the version identifies a bug-fix release."""
        return self.is_release and not self.is_full_release

    @property
    def is_development(self):
        """Whether the version is a non-release prior to feature freeze."""
        return 0 < self[SNAPSHOT] < BRANCH_START_SNAPSHOT

    @property
    def is_branch_start(self):
        """Whether the version is the start of a release branch."""
        return self[SNAPSHOT] == BRANCH_START_SNAPSHOT

    @property
    def is_release_candidate(self):
        """Whether the version identifies a release candidate."""
        return self[SNAPSHOT] > BRANCH_START_SNAPSHOT

    @property
    def release_candidate(self):
        """The release candidate number if it is a release candidate."""
        return ((self[SNAPSHOT] - BRANCH_START_SNAPSHOT)
                if self.is_release_candidate else None)

    @property
    def stable_branch_suffix(self):
        """The suffix of the stable branch name if not in development."""
        if self.is_development:
            return
        major, minor = self[MAJOR], self[MINOR]
        if self.is_pre_full_release:
            if minor == PRE_FULL_RELEASE:
                minor = 0
                major += 1
            else:
                minor += 1
        return '-{}.{}-branch'.format(major, minor)
