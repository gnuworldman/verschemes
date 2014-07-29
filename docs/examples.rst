Examples
========

Importing
---------

>>> from verschemes import Version
>>> from verschemes.python import PythonVersion, PythonMinorVersion
>>> from verschemes.pep440 import Pep440Version

Instantiation from a string
---------------------------

>>> Version("3.1.4")
verschemes.Version(3, 1, 4)
>>> Pep440Version("3.1.4")
verschemes.pep440.Pep440Version(None, 3, 1, 4, None, None, None, None, None, None)

Instantiation from segment values
---------------------------------

>>> Version(3, 1, 4)
verschemes.Version(3, 1, 4)
>>> PythonVersion(3, 1, 4, ["b", 5])
verschemes.python.PythonVersion(3, 1, 4, Segment(releaselevel='b', serial=5))
>>> Pep440Version(None, 3, 1, 4)
verschemes.pep440.Pep440Version(None, 3, 1, 4, None, None, None, None, None, None)

Instantiation from named segment values
---------------------------------------

>>> PythonVersion(major=3, minor=1, micro=4)
verschemes.python.PythonVersion(3, 1, 4, None)
>>> Pep440Version(release1=3, release2=1, release3=4)
verschemes.pep440.Pep440Version(None, 3, 1, 4, None, None, None, None, None, None)
>>> Pep440Version(epoch=2, release1=3, release2=1, release3=4, post_release=7)
verschemes.pep440.Pep440Version(2, 3, 1, 4, None, None, None, None, 7, None)

Rendering
---------

>>> version = Version(3, 1, 4)
>>> str(version)
'3.1.4'
>>> version.render()
'3.1.4'
>>> version = Pep440Version("3.1.4b5", epoch=2)
>>> str(version)
'2!3.1.4b5'
>>> version.render(min_release_segments=4)
'2!3.1.4.0b5'

Comparison
----------

>>> Version("3.1.4") == Version(3, 1, 4)
True
>>> Version("3.1.10") > Version("3.1.4")
True
>>> PythonVersion(3, 1, 4, ["b", 5]).minor_version == PythonMinorVersion(3, 1)
True

Normalization
-------------

>>> str(Version("3.01.0004"))
'3.1.4'
>>> str(Pep440Version("3.1.4-dev5"))
'3.1.4.dev5'
>>> str(Pep440Version("3.1.4post6"))
'3.1.4.post6'
>>> str(Pep440Version("3.1.4.RC7"))
'3.1.4c7'

Properties
----------

>>> version = PythonVersion(3, 1, 4, ["b", 5])
>>> version.major
3
>>> version.minor
1
>>> version.micro
4
>>> version.suffix.releaselevel
'b'
>>> version.suffix.serial
5
>>> version.is_release
True
>>> version.is_nondevelopment
False
>>> Pep440Version("3.1.4").is_release
True
>>> Pep440Version("3.1.4a2").is_release
False

Replacement
-----------

>>> version = Version(3, 1, 4)
>>> new_version = version.replace(_0=2)
>>> str(new_version)
'2.1.4'
>>> version = PythonVersion(3, 1, 4)
>>> new_version = version.replace(major=2)
>>> str(new_version)
'2.1.4'
