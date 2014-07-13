# -*- coding: utf-8 -*-
"""versioning tests"""

from __future__ import absolute_import
from __future__ import unicode_literals

import unittest

from future.builtins import str

from verschemes.postgresql import *


class PgVersionTestCase(unittest.TestCase):

    def test_invalid_major_one_segment(self):
        self.assertRaises(ValueError, PgMajorVersion, 9)

    def test_valid_major(self):
        version = PgMajorVersion(8, 3)
        self.assertEqual("8.3", str(version))
        self.assertEqual("8.3", version.render(exclude_defaults=False))
        self.assertEqual(8, version[MAJOR1])
        self.assertEqual(3, version[MAJOR2])
        self.assertRaises(IndexError, version.__getitem__, 2)
        self.assertRaises(IndexError, version.__getitem__, 3)

    def test_valid_optional_with_default(self):
        version = PgVersion(8, 3)
        self.assertEqual("8.3", str(version))
        self.assertEqual("8.3.0", version.render(exclude_defaults=False))
        self.assertEqual(8, version[MAJOR1])
        self.assertEqual(3, version[MAJOR2])
        self.assertEqual(0, version[MINOR])
        self.assertRaises(IndexError, version.__getitem__, 3)

    def test_valid_optional_with_value_matching_default(self):
        version = PgVersion(8, 3, 0)
        self.assertEqual("8.3.0", str(version))
        self.assertEqual("8.3.0", version.render(exclude_defaults=False))
        self.assertEqual(8, version[MAJOR1])
        self.assertEqual(3, version[MAJOR2])
        self.assertEqual(0, version[MINOR])
        self.assertRaises(IndexError, version.__getitem__, 3)
        version[2] = None
        self.assertEqual(0, version[MINOR])
        self.assertEqual("8.3", str(version))
        self.assertEqual("8.3.0", version.render(exclude_defaults=False))

    def test_valid_minor(self):
        version = PgVersion(8, 3, 4)
        self.assertEqual("8.3.4", str(version))
        self.assertEqual("8.3.4", version.render(exclude_defaults=False))
        self.assertEqual(8, version[MAJOR1])
        self.assertEqual(3, version[MAJOR2])
        self.assertEqual(4, version[MINOR])
        self.assertRaises(IndexError, version.__getitem__, 3)

    def test_valid_minor_major_comparison(self):
        version = PgVersion(8, 3, 4)
        self.assertEqual(PgMajorVersion(8, 3), version.major_version)

    def test_invalid_minor_major_comparison(self):
        version = PgVersion(8, 3, 4)
        self.assertNotEqual(PgMajorVersion(8, 2), version.major_version)


if __name__ == '__main__':
    unittest.main()
