Release Notes
=============

Version 1.2
-----------

This is no longer a need for Python 2 clients to use the `future` library in
client code nor to pass `unicode` objects for strings.  They are still allowed
of course, but Python 2 str objects are now accepted as input into the library
without causing bugs.  The library's internal stored values are still Unicode.

Segments whose definitions contain multiple fields now have
`~collections.namedtuple`-based values, from which one can access the field
values by the fields' names.  See the `~verschemes.python.PythonVersion`
(`suffix` segment) :ref:`properties examples <properties_examples>`.

Version 1.1
-----------

All `~verschemes.Version`\s are now immutable; setting segment values with
indexing and slicing is no longer supported.  One should now make new version
objects with different segment values via the `~verschemes.Version.replace`
method.  This follows the paradigm of the `datetime` classes.  For example with
an object named 'version', ``version[2] = 8`` can no longer replace the third
segment in place, but ``version.replace(_2=8)`` can be used to create a new
object of the same type with the new segment value and all other segment values
same as the original object.

The default for the `re_pattern` attribute of `~verschemes.SegmentField` has
been changed to allow field input with leading zeros.  By default when the
value is rendered, it is normalized to not contain unnecessary leading zeros.

A segment can now be given a name in the `~verschemes.SegmentDefinition`
constructor, which allows the segment value in a `~verschemes.Version` object
to be accessed via a property of that name and may also be identified by that
name as a keyword in the constructor and :meth:`~verschemes.Version.replace`.

`~verschemes.SegmentDefinition` now also accepts an optional
`separator_re_pattern` attribute that can be used to accept (during string
initialization) more than the literal `separator`, which is the normal form
(output when rendered) for the separator prior to the segment.

The `separator` prior to the `release1` segment of
`~verschemes.pep440.Pep440Version` has been fixed (was a colon) so that if an
`epoch` is specified, it will be followed by the proper exclamation mark when
the version is rendered.

An implementation of the `X.org <http://www.x.org/>`_ `version number scheme
<http://www.x.org/wiki/Development/Documentation/VersionNumberScheme/>`_ is now
included in the `~verschemes.xorg` module.

Version 1.0
-----------

This is the initial release.
