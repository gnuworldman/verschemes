# -*- coding: utf-8 -*-
"""Python verschemes tests"""

import unittest

from verschemes.python import (PythonMajorVersion, PythonMicroVersion,
                               PythonMinorVersion, PythonVersion)


class PythonVersionTestCase(unittest.TestCase):

    def test_valid_major(self):
        version = PythonMajorVersion(8)
        self.assertEqual("8", str(version))
        self.assertEqual("8", version.render(exclude_defaults=False))
        self.assertEqual(8, version.major)
        self.assertRaises(IndexError, version.__getitem__,
                          len(PythonMajorVersion.SEGMENT_DEFINITIONS))

    def test_valid_minor(self):
        version = PythonMinorVersion(5, 2)
        self.assertEqual("5.2", str(version))
        self.assertEqual("5.2", version.render(exclude_defaults=False))
        self.assertEqual(5, version.major)
        self.assertEqual(2, version.minor)
        self.assertRaises(IndexError, version.__getitem__,
                          len(PythonMinorVersion.SEGMENT_DEFINITIONS))

    def test_valid_micro(self):
        version = PythonMicroVersion(5, 2, 7)
        self.assertEqual("5.2.7", str(version))
        self.assertEqual("5.2.7", version.render(exclude_defaults=False))
        self.assertEqual(5, version.major)
        self.assertEqual(2, version.minor)
        self.assertEqual(7, version.micro)
        self.assertRaises(IndexError, version.__getitem__,
                          len(PythonMicroVersion.SEGMENT_DEFINITIONS))

    def test_valid_nondevelopment(self):
        version = PythonVersion(2, 7, 9)
        self.assertEqual("2.7.9", str(version))
        self.assertEqual("2.7.9", version.render(exclude_defaults=False))
        self.assertEqual(2, version.major)
        self.assertEqual(7, version.minor)
        self.assertEqual(9, version.micro)
        self.assertEqual(None, version.suffix)
        self.assertRaises(IndexError, version.__getitem__,
                          len(PythonVersion.SEGMENT_DEFINITIONS))

    def test_valid_development(self):
        version = PythonVersion(2, 7, 8, '+')
        self.assertEqual("2.7.8+", str(version))
        self.assertEqual("2.7.8+", version.render(exclude_defaults=False))
        self.assertEqual(2, version.major)
        self.assertEqual(7, version.minor)
        self.assertEqual(8, version.micro)
        self.assertEqual(('+', None), version.suffix)
        self.assertRaises(IndexError, version.__getitem__,
                          len(PythonVersion.SEGMENT_DEFINITIONS))
        self.assertEqual(version, PythonVersion('2.7.8+'))

    def test_valid_alpha(self):
        version = PythonVersion(2, 7, 9, ('a', 4))
        self.assertEqual("2.7.9a4", str(version))
        self.assertEqual("2.7.9a4", version.render(exclude_defaults=False))
        self.assertEqual(2, version.major)
        self.assertEqual(7, version.minor)
        self.assertEqual(9, version.micro)
        self.assertEqual(('a', 4), version.suffix)
        self.assertRaises(IndexError, version.__getitem__,
                          len(PythonVersion.SEGMENT_DEFINITIONS))

    def test_valid_beta(self):
        version = PythonVersion(2, 7, 12, ('b', 6))
        self.assertEqual("2.7.12b6", str(version))
        self.assertEqual("2.7.12b6", version.render(exclude_defaults=False))
        self.assertEqual(2, version.major)
        self.assertEqual(7, version.minor)
        self.assertEqual(12, version.micro)
        self.assertEqual(('b', 6), version.suffix)
        self.assertRaises(IndexError, version.__getitem__,
                          len(PythonVersion.SEGMENT_DEFINITIONS))

    def test_valid_release_candidate(self):
        version = PythonVersion(2, 7, 7, ('c', 1))
        self.assertEqual("2.7.7c1", str(version))
        self.assertEqual("2.7.7c1", version.render(exclude_defaults=False))
        self.assertEqual(2, version.major)
        self.assertEqual(7, version.minor)
        self.assertEqual(7, version.micro)
        self.assertEqual(('c', 1), version.suffix)
        self.assertRaises(IndexError, version.__getitem__,
                          len(PythonVersion.SEGMENT_DEFINITIONS))

    def test_valid_minor_major_equal(self):
        version = PythonMinorVersion(5, 2)
        self.assertEqual("5.2", str(version))
        self.assertEqual(PythonMajorVersion(5), version.major_version)

    def test_valid_micro_major_equal(self):
        self.assertEqual(PythonMajorVersion(5),
                         PythonMicroVersion(5, 2, 7).major_version)

    def test_valid_micro_minor_equal(self):
        self.assertEqual(PythonMinorVersion(5, 2),
                         PythonMicroVersion(5, 2, 7).minor_version)

    def test_valid_beta_micro_equal(self):
        self.assertEqual(PythonMicroVersion(2, 7, 12),
                         PythonVersion(2, 7, 12, ('b', 6)).micro_version)

    def test_valid_beta_micro_comparison(self):
        self.assertGreater(PythonMicroVersion(2, 7, 22),
                           PythonVersion(2, 7, 12, ('b', 6)).micro_version)

    def test_valid_string_minor(self):
        version = PythonVersion('3.4')
        self.assertEqual(3, version.major)
        self.assertEqual(4, version.minor)
        self.assertEqual(None, version.micro)
        self.assertEqual(None, version.suffix)

    def test_valid_string_micro(self):
        version = PythonVersion('3.4.1')
        self.assertEqual(3, version.major)
        self.assertEqual(4, version.minor)
        self.assertEqual(1, version.micro)
        self.assertEqual(None, version.suffix)

    def test_valid_string_development(self):
        version = PythonVersion('3.4.1c1')
        self.assertEqual(3, version.major)
        self.assertEqual(4, version.minor)
        self.assertEqual(1, version.micro)
        self.assertEqual(('c', 1), version.suffix)

    def test_valid_string_nonrelease(self):
        version = PythonVersion('3.4.1+')
        self.assertEqual(3, version.major)
        self.assertEqual(4, version.minor)
        self.assertEqual(1, version.micro)
        self.assertEqual(('+', None), version.suffix)

    def test_valid_development_minor_equal(self):
        self.assertEqual(PythonMinorVersion(2, 3),
                         PythonVersion(2, 3, 4, '+').minor_version)

    def test_eq(self):
        version = PythonVersion(3, 4, 2, 'a2')
        self.assertEqual(version, PythonVersion(3, 4, 2, 'a2'))

    def test_is_nondevelopment_release(self):
        version = PythonVersion(2, 3)
        self.assertTrue(version.is_nondevelopment)

    def test_is_nondevelopment_dev(self):
        version = PythonVersion(2, 3, 4, '+')
        self.assertFalse(version.is_nondevelopment)

    def test_is_nondevelopment_beta(self):
        version = PythonVersion(2, 3, 4, 'b5')
        self.assertFalse(version.is_nondevelopment)

    def test_is_release(self):
        version = PythonVersion(2, 3)
        self.assertTrue(version.is_release)

    def test_is_release_dev(self):
        version = PythonVersion(2, 3, 4, '+')
        self.assertFalse(version.is_release)

    def test_is_release_beta(self):
        version = PythonVersion(2, 3, 4, 'b5')
        self.assertTrue(version.is_release)

    def test_invalid_alpha_serial_none(self):
        self.assertRaises(ValueError, PythonVersion, 2, 7, 9, ('a', None))

    def test_invalid_alpha_serial_missing(self):
        self.assertRaises(ValueError, PythonVersion, 2, 7, 9, ('a',))

    def test_invalid_alpha_string(self):
        self.assertRaises(ValueError, PythonVersion, 2, 7, 9, 'a')
