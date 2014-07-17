Purpose of the verschemes library
=================================

Most versioned components have their own method of identifying their versions.
This method is often termed "versioning" or called a "version scheme".  The
method is simply a set of rules that dictate what is a valid version identifier
and is usually separated in a number of segments to signify hierarchy among the
versions.  The hierarchy determines ordering along with the values of the
segments within the hierarchy.

For example, the following is an ordered list of common version identifiers:

* 0.1
* 0.2
* 0.9
* 0.10
* 0.11
* 1.0
* 1.0.1
* 1.1
* 2.0
* 10.0

The most common version identifiers are simply an ordered set of integers
separated by dots.  The default implementation in the `~verschemes.Version`
class provides this common use case with any number of segments.  To create an
instance of "version 1.4.2", one can write ``Version(1, 4, 2)`` or
``Version('1.4.2')`` (after ``from verschemes import Version``, of course).

Some version schemes are more involved and require using subclasses of
`Version` to represent them.  Each subclass of `Version` represents a specific
version scheme, whereas each instance of a `Version` subclass represents a
specific version that follows the class's scheme.

There are several version schemes implemented in the verschemes library, and
more are sure to be added (submissions are welcome).  These implementations
also work as examples for those wishing to subclass `Version` for their own
(or another's) version scheme.
