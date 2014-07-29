"""X.org verschemes tests"""

import unittest

from verschemes.xorg import XorgVersion


class XorgVersionTestCase(unittest.TestCase):

    def test_valid_major(self):
        version = XorgVersion(8)
        self.assertEqual("8.0.0", str(version))
        self.assertEqual("8.0.0.0", version.render(exclude_defaults=False))
        self.assertEqual(8, version.major)
        self.assertEqual(0, version.minor)
        self.assertEqual(0, version.patch)
        self.assertEqual(0, version.snapshot)
        self.assertRaises(IndexError, version.__getitem__, 4)

    def test_valid_minor(self):
        version = XorgVersion(5, 2)
        self.assertEqual("5.2.0", str(version))
        self.assertEqual("5.2.0.0", version.render(exclude_defaults=False))
        self.assertEqual(5, version.major)
        self.assertEqual(2, version.minor)
        self.assertEqual(0, version.patch)
        self.assertEqual(0, version.snapshot)
        self.assertRaises(IndexError, version.__getitem__, 4)

    def test_valid_bugfix(self):
        version = XorgVersion(2, 7, 9)
        self.assertEqual("2.7.9", str(version))
        self.assertEqual("2.7.9.0", version.render(exclude_defaults=False))
        self.assertEqual(2, version.major)
        self.assertEqual(7, version.minor)
        self.assertEqual(9, version.patch)
        self.assertEqual(0, version.snapshot)
        self.assertRaises(IndexError, version.__getitem__, 4)

    def test_valid_development(self):
        version = XorgVersion(2, 3, 99, 6)
        self.assertEqual("2.3.99.6", str(version))
        self.assertEqual("2.3.99.6", version.render(exclude_defaults=False))
        self.assertEqual(2, version.major)
        self.assertEqual(3, version.minor)
        self.assertEqual(99, version.patch)
        self.assertEqual(6, version.snapshot)
        self.assertRaises(IndexError, version.__getitem__, 4)
        self.assertEqual(version, XorgVersion('2.3.99.6'))

    def test_valid_release_candidate(self):
        version = XorgVersion(2, 3, 4, 905)
        self.assertEqual("2.3.4.905", str(version))
        self.assertEqual("2.3.4.905", version.render(exclude_defaults=False))
        self.assertEqual(2, version.major)
        self.assertEqual(3, version.minor)
        self.assertEqual(4, version.patch)
        self.assertEqual(905, version.snapshot)
        self.assertRaises(IndexError, version.__getitem__, 4)

    def test_valid_string_major(self):
        version = XorgVersion('11')
        self.assertEqual(11, version.major)
        self.assertEqual(0, version.minor)
        self.assertEqual(0, version.patch)
        self.assertEqual(0, version.snapshot)

    def test_valid_string_minor(self):
        version = XorgVersion('11.7')
        self.assertEqual(11, version.major)
        self.assertEqual(7, version.minor)
        self.assertEqual(0, version.patch)
        self.assertEqual(0, version.snapshot)

    def test_valid_string_patch(self):
        version = XorgVersion('11.7.1')
        self.assertEqual(11, version.major)
        self.assertEqual(7, version.minor)
        self.assertEqual(1, version.patch)
        self.assertEqual(0, version.snapshot)

    def test_valid_string_snapshot(self):
        version = XorgVersion('11.7.1.909')
        self.assertEqual(11, version.major)
        self.assertEqual(7, version.minor)
        self.assertEqual(1, version.patch)
        self.assertEqual(909, version.snapshot)

    def test_valid_string_development(self):
        version = XorgVersion(11, 7, 99, 6)
        self.assertEqual(11, version.major)
        self.assertEqual(7, version.minor)
        self.assertEqual(99, version.patch)
        self.assertEqual(6, version.snapshot)

    def test_eq(self):
        version = XorgVersion(3, 4, 2, 901)
        self.assertEqual(version, XorgVersion(3, 4, 2, 901))

    def test_is_release(self):
        version = XorgVersion(2, 3)
        self.assertTrue(version.is_release)

    def test_is_full_release(self):
        version = XorgVersion(2, 3)
        self.assertTrue(version.is_full_release)

    def test_is_full_release_bugfix(self):
        version = XorgVersion(2, 3, 1)
        self.assertFalse(version.is_full_release)

    def test_is_pre_full_release(self):
        version = XorgVersion(2, 3, 99, 1)
        self.assertTrue(version.is_pre_full_release)

    def test_is_pre_full_release_bugfix(self):
        version = XorgVersion(2, 3, 4)
        self.assertFalse(version.is_pre_full_release)

    def test_is_pre_full_release_bugfix_snapshot(self):
        version = XorgVersion(2, 3, 4, 901)
        self.assertFalse(version.is_pre_full_release)

    def test_is_bugfix_release(self):
        version = XorgVersion(2, 3, 4)
        self.assertTrue(version.is_bugfix_release)

    def test_is_bugfix_release_full(self):
        version = XorgVersion(2, 3, 0)
        self.assertFalse(version.is_bugfix_release)

    def test_is_bugfix_release_dev(self):
        version = XorgVersion(2, 3, 99, 6)
        self.assertFalse(version.is_bugfix_release)

    def test_is_development(self):
        version = XorgVersion(2, 3, 99, 6)
        self.assertTrue(version.is_development)

    def test_is_development_release(self):
        version = XorgVersion(2, 3, 4)
        self.assertFalse(version.is_development)

    def test_is_development_candidate(self):
        version = XorgVersion(2, 3, 4, 905)
        self.assertFalse(version.is_development)

    def test_is_development_pre_full(self):
        version = XorgVersion(2, 3, 99, 905)
        self.assertFalse(version.is_development)

    def test_is_branch_start(self):
        version = XorgVersion(2, 3, 99, 900)
        self.assertTrue(version.is_branch_start)

    def test_is_branch_start_release(self):
        version = XorgVersion(2, 3, 4)
        self.assertFalse(version.is_branch_start)

    def test_is_branch_start_candidate(self):
        version = XorgVersion(2, 3, 4, 905)
        self.assertFalse(version.is_branch_start)

    def test_is_branch_start_dev(self):
        version = XorgVersion(2, 3, 99, 4)
        self.assertFalse(version.is_branch_start)

    def test_is_release_candidate(self):
        version = XorgVersion(2, 3, 4, 905)
        self.assertTrue(version.is_release_candidate)

    def test_is_release_candidate_release(self):
        version = XorgVersion(2, 3, 4)
        self.assertFalse(version.is_release_candidate)

    def test_is_release_candidate_dev(self):
        version = XorgVersion(2, 3, 99, 4)
        self.assertFalse(version.is_release_candidate)

    def test_release_candidate(self):
        version = XorgVersion(2, 3, 4, 905)
        self.assertEqual(5, version.release_candidate)

    def test_stable_branch_suffix(self):
        version = XorgVersion(2, 3, 4)
        self.assertEqual('-2.3-branch', version.stable_branch_suffix)

    def test_stable_branch_suffix_dev(self):
        version = XorgVersion(2, 3, 99, 5)
        self.assertIsNone(version.stable_branch_suffix)

    def test_stable_branch_suffix_pre_full(self):
        version = XorgVersion(2, 3, 99, 905)
        self.assertEqual('-2.4-branch', version.stable_branch_suffix)

    def test_stable_branch_suffix_pre_full_major(self):
        version = XorgVersion(2, 99, 99, 905)
        self.assertEqual('-3.0-branch', version.stable_branch_suffix)

    def test_invalid_pre_full_release(self):
        self.assertRaises(ValueError, XorgVersion, 7, 1, 99, 0)

    def test_invalid_development(self):
        self.assertRaises(ValueError, XorgVersion, 7, 1, 3, 2)
