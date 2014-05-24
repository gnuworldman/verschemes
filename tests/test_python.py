"""versioning tests"""

import unittest

from versioning.python import *


class PythonVersionTestCase(unittest.TestCase):

    def test_valid_major(self):
        version = PythonMajorVersion(8)
        self.assertEqual("8", str(version))
        self.assertEqual("8", version.render(exclude_defaults=False))
        self.assertEqual(8, version[0])
        self.assertRaises(IndexError, version.__getitem__, 1)
        self.assertRaises(IndexError, version.__getitem__, 2)
        self.assertRaises(IndexError, version.__getitem__, 3)
        self.assertRaises(IndexError, version.__getitem__, 4)

    def test_valid_minor(self):
        version = PythonMinorVersion(5, 2)
        self.assertEqual("5.2", str(version))
        self.assertEqual("5.2", version.render(exclude_defaults=False))
        self.assertEqual(5, version[0])
        self.assertEqual(2, version[1])
        self.assertRaises(IndexError, version.__getitem__, 2)

    def test_valid_minor_major_comparison(self):
        version = PythonMinorVersion(5, 2)
        self.assertEqual("5.2", str(version))
        self.assertEqual(PythonMajorVersion(5), version.major_version)

    def test_valid_alpha(self):
        version = PythonVersion(2, 7, 9, ('a', 4))
        self.assertEqual("2.7.9a4", str(version))
        self.assertEqual("2.7.9a4", version.render(exclude_defaults=False))
        self.assertEqual(2, version[0])
        self.assertEqual(7, version[1])
        self.assertEqual(9, version[2])
        self.assertEqual(('a', 4), version[3])
        self.assertRaises(IndexError, version.__getitem__, 4)

    def test_valid_beta(self):
        version = PythonVersion(2, 7, 12, ('b', 6))
        self.assertEqual("2.7.12b6", str(version))
        self.assertEqual("2.7.12b6", version.render(exclude_defaults=False))
        self.assertEqual(2, version[0])
        self.assertEqual(7, version[1])
        self.assertEqual(12, version[2])
        self.assertEqual(('b', 6), version[3])
        self.assertRaises(IndexError, version.__getitem__, 4)

    def test_valid_beta_micro_equality(self):
        self.assertEqual(PythonMicroVersion(2, 7, 12),
                         PythonVersion(2, 7, 12, ('b', 6)).micro_version)

    def test_valid_beta_micro_comparison(self):
        self.assertGreater(PythonMicroVersion(2, 7, 22),
                           PythonVersion(2, 7, 12, ('b', 6)).micro_version)

    def test_valid_release_candidate(self):
        version = PythonVersion(2, 7, 7, ('c', 1))
        self.assertEqual("2.7.7c1", str(version))
        self.assertEqual("2.7.7c1", version.render(exclude_defaults=False))
        self.assertEqual(2, version[0])
        self.assertEqual(7, version[1])
        self.assertEqual(7, version[2])
        self.assertEqual(('c', 1), version[3])
        self.assertRaises(IndexError, version.__getitem__, 4)

    def test_valid_development(self):
        version = PythonVersion(2, 7, 8, '+')
        self.assertEqual("2.7.8+", str(version))
        self.assertEqual("2.7.8+", version.render(exclude_defaults=False))
        self.assertEqual(2, version[0])
        self.assertEqual(7, version[1])
        self.assertEqual(8, version[2])
        self.assertEqual(('+', None), version[3])
        self.assertRaises(IndexError, version.__getitem__, 4)
        self.assertEqual(version, PythonVersion('2.7.8+'))

    def test_valid_development_minor_comparison(self):
        self.assertEqual(PythonMinorVersion(2, 3),
                         PythonVersion(2, 3, 4, '+').minor_version)

    def test_is_nondevelopment_release(self):
        version = PythonVersion(2, 3)
        self.assertTrue(version.is_nondevelopment)

    def test_is_nondevelopment_dev(self):
        version = PythonVersion(2, 3, 4, '+')
        self.assertFalse(version.is_nondevelopment)

    def test_is_nondevelopment_beta(self):
        version = PythonVersion(2, 3, 4, 'b5')
        self.assertFalse(version.is_nondevelopment)

    def test_invalid_alpha_serial_none(self):
        self.assertRaises(ValueError, PythonVersion, 2, 7, 9, ('a', None))

    def test_invalid_alpha_serial_missing(self):
        self.assertRaises(ValueError, PythonVersion, 2, 7, 9, ('a',))

    def test_invalid_alpha_string(self):
        self.assertRaises(ValueError, PythonVersion, 2, 7, 9, 'a')


if __name__ == '__main__':
    unittest.main()
