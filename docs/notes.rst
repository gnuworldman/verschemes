Release Notes
=============

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

A segment can now be given a name in the `~verschemes.SegmentDefinition`
constructor, which allows the segment value in a `~verschemes.Version` object
to be accessed via a property of that name and may also be identified by that
name as a keyword in the constructor and :meth:`~verschemes.Version.replace`.

Version 1.0
-----------

This is the initial release.
