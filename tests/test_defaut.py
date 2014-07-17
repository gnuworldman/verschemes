# -*- coding: utf-8 -*-
"""default implementation verschemes tests"""

from __future__ import absolute_import
from __future__ import unicode_literals

import unittest

from future.builtins import str

from verschemes import Version


class DefaultVersionTestCase(unittest.TestCase):

    def test_valid_one_segment(self):
        for version in (Version(4), Version('4')):
            self.assertEqual("4", str(version))
            self.assertEqual(4, version[0])
            self.assertRaises(IndexError, version.__getitem__, 1)
            self.assertRaises(IndexError, version.__getitem__, 2)

    def test_valid_two_segments(self):
        for version in (Version(8, 2), Version('8.2')):
            self.assertEqual("8.2", str(version))
            self.assertEqual(8, version[0])
            self.assertEqual(2, version[1])
            self.assertRaises(IndexError, version.__getitem__, 2)

    def test_valid_three_segments(self):
        for version in (Version(3, 11, 8), Version('3.11.8')):
            self.assertEqual("3.11.8", str(version))
            self.assertEqual(3, version[0])
            self.assertEqual(11, version[1])
            self.assertEqual(8, version[2])
            self.assertRaises(IndexError, version.__getitem__, 3)

    def test_valid_four_segments(self):
        for version in (Version(7, 1, 26, 5), Version('7.1.26.5')):
            self.assertEqual("7.1.26.5", str(version))
            self.assertEqual(7, version[0])
            self.assertEqual(1, version[1])
            self.assertEqual(26, version[2])
            self.assertEqual(5, version[3])
            self.assertRaises(IndexError, version.__getitem__, 4)

    def test_valid_replacement(self):
        version = Version(3, 11, 8)
        self.assertEqual("3.11.8", str(version))
        version = version.replace(_0=4, _1=735, _2=29)
        self.assertEqual("4.735.29", str(version))

    def test_valid_replacement_partial(self):
        version = Version(3, 11, 8)
        self.assertEqual("3.11.8", str(version))
        version = version.replace(_1=735)
        self.assertEqual("3.735.8", str(version))

    def test_invalid_replacement_extra(self):
        version = Version(1, 2, 3)
        self.assertRaises(IndexError, version.replace, _0=5, _1=6, _2=7, _3=8)
        self.assertEqual(1, version[0])
        self.assertEqual(2, version[1])
        self.assertEqual(3, version[2])
        self.assertRaises(IndexError, version.__getitem__, 3)

    def test_invalid_replacement_nonexistent(self):
        version = Version(1, 2, 3)
        self.assertRaises(KeyError, version.replace, something=8)
        self.assertEqual(1, version[0])
        self.assertEqual(2, version[1])
        self.assertEqual(3, version[2])
        self.assertRaises(IndexError, version.__getitem__, 3)

    def test_invalid_version_init(self):
        self.assertRaises(ValueError, Version, "a")

    def test_invalid_extra_segment_values(self):
        self.assertRaises(ValueError, Version, (2, 8))


if __name__ == '__main__':
    unittest.main()
