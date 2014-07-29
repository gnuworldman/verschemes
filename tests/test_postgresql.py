# -*- coding: utf-8 -*-
"""PostgreSQL verschemes tests"""

import unittest

from verschemes.postgresql import PgMajorVersion, PgVersion


class PgVersionTestCase(unittest.TestCase):

    def test_invalid_major_one_segment(self):
        self.assertRaises(ValueError, PgMajorVersion, 9)

    def test_valid_major(self):
        version = PgMajorVersion(8, 3)
        self.assertEqual("8.3", str(version))
        self.assertEqual("8.3", version.render(exclude_defaults=False))
        self.assertEqual(8, version.major1)
        self.assertEqual(3, version.major2)
        self.assertRaises(IndexError, version.__getitem__, 2)
        self.assertRaises(IndexError, version.__getitem__, 3)

    def test_valid_optional_with_default(self):
        version = PgVersion(8, 3)
        self.assertEqual("8.3", str(version))
        self.assertEqual("8.3.0", version.render(exclude_defaults=False))
        self.assertEqual(8, version.major1)
        self.assertEqual(3, version.major2)
        self.assertEqual(0, version.minor)
        self.assertRaises(IndexError, version.__getitem__, 3)

    def test_valid_optional_with_value_matching_default(self):
        version = PgVersion(8, 3, 0)
        self.assertEqual("8.3.0", str(version))
        self.assertEqual("8.3.0", version.render(exclude_defaults=False))
        self.assertEqual(8, version.major1)
        self.assertEqual(3, version.major2)
        self.assertEqual(0, version.minor)
        self.assertRaises(IndexError, version.__getitem__, 3)
        version = version.replace(minor=None)
        self.assertEqual(0, version.minor)
        self.assertEqual("8.3", str(version))
        self.assertEqual("8.3.0", version.render(exclude_defaults=False))

    def test_valid_minor(self):
        version = PgVersion(8, 3, 4)
        self.assertEqual("8.3.4", str(version))
        self.assertEqual("8.3.4", version.render(exclude_defaults=False))
        self.assertEqual(8, version.major1)
        self.assertEqual(3, version.major2)
        self.assertEqual(4, version.minor)
        self.assertRaises(IndexError, version.__getitem__, 3)

    def test_valid_string_optional_with_default(self):
        version = PgVersion('8.3')
        self.assertEqual("8.3", str(version))
        self.assertEqual("8.3.0", version.render(exclude_defaults=False))
        self.assertEqual(8, version.major1)
        self.assertEqual(3, version.major2)
        self.assertEqual(0, version.minor)
        self.assertRaises(IndexError, version.__getitem__, 3)

    def test_valid_string_optional_with_value_matching_default(self):
        version = PgVersion('8.3.0')
        self.assertEqual("8.3.0", str(version))
        self.assertEqual("8.3.0", version.render(exclude_defaults=False))
        self.assertEqual(8, version.major1)
        self.assertEqual(3, version.major2)
        self.assertEqual(0, version.minor)
        self.assertRaises(IndexError, version.__getitem__, 3)
        version = version.replace(minor=None)
        self.assertEqual(0, version.minor)
        self.assertEqual("8.3", str(version))
        self.assertEqual("8.3.0", version.render(exclude_defaults=False))

    def test_valid_minor_major_comparison(self):
        version = PgVersion(8, 3, 4)
        self.assertEqual(PgMajorVersion(8, 3), version.major_version)

    def test_invalid_minor_major_comparison(self):
        version = PgVersion(8, 3, 4)
        self.assertNotEqual(PgMajorVersion(8, 2), version.major_version)
