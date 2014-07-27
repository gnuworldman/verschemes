Overview
========

Concept
-------

Most versioned components have their own method of identifying their versions.
This method is often termed "versioning" or called a "version scheme".  The
method is simply a set of rules that dictate what is a valid version identifier
and is usually separated (often by delimiters, such as a dot) in a number of
segments to signify hierarchy among the versions.  The hierarchy determines
ordering along with the values of the segments within the hierarchy.

Implementation
--------------

In the `verschemes` library, a version scheme is a set of rules pertaining to
the identification of versions for a given scope or purpose.  Each version
contains a number of segments often separated by delimiters.  Each segment is
allowed to have multiple fields to identify portions of the segment, though
many segments have just one field.

Many version schemes are just integers separated by dots.  The base
`Version <http://gnuworldman.github.io/verschemes/api.html#verschemes.Version>`_
class works fine for generic version numbers that fit
this scheme, but the real power of this library is in defining version schemes
(`Version` subclasses) with segments that specifically describe the scheme and
automatically implement validation and normalized rendering of a version
identifier or a sequence of version segment values.  The
`SEGMENT_DEFINITIONS <http://gnuworldman.github.io/verschemes/api.html#verschemes.Version.SEGMENT_DEFINITIONS>`_
attribute of a `Version` subclass can be used to define the specific parameters
of the version scheme that is represented by that class.

The library also contains some implementations of specific version schemes
including
`Python <https://docs.python.org/3/faq/general.html#how-does-the-python-version-numbering-scheme-work>`_,
`PEP 440 <http://legacy.python.org/dev/peps/pep-0440/#local-version-identifiers>`_,
`PostgreSQL <http://www.postgresql.org/support/versioning/>`_, and
`X.org <http://www.x.org/wiki/Development/Documentation/VersionNumberScheme/>`_
versioning.  More are sure to be added, and submissions of version shemes for
popular, public projects/systems are welcome.  These implementations also serve
as examples for those wishing to subclass `Version` for their own (or
another's) version scheme.
