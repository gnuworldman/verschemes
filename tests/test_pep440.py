"""PEP 440 versioning tests"""

import unittest

from versioning.pep440 import *


class Pep440VersionTestCase(unittest.TestCase):

    def test_valid_one_segment(self):
        version = Pep440Version(release1=4)
        self.assertEqual("4", str(version))
        self.assertEqual(0, version[EPOCH])
        self.assertEqual(4, version[RELEASE1])
        self.assertEqual(0, version[RELEASE2])
        self.assertEqual(0, version[RELEASE3])
        self.assertEqual(0, version[RELEASE4])
        self.assertEqual(0, version[RELEASE5])
        self.assertEqual(0, version[RELEASE6])
        self.assertEqual(None, version[PRE_RELEASE])
        self.assertEqual(None, version[POST_RELEASE])
        self.assertEqual(None, version[DEVELOPMENT])

    def test_valid_two_segments(self):
        version = Pep440Version(release1=8, release2=2)
        self.assertEqual("8.2", str(version))
        self.assertEqual(8, version[RELEASE1])
        self.assertEqual(2, version[RELEASE2])

    def test_valid_three_segments(self):
        version = Pep440Version(None, 3, 11, 8)
        self.assertEqual("3.11.8", str(version))
        self.assertEqual(3, version[RELEASE1])
        self.assertEqual(11, version[RELEASE2])
        self.assertEqual(8, version[RELEASE3])

    def test_valid_four_segments(self):
        version = Pep440Version(release1=7, release2=1, release3=26,
                                release4=5)
        self.assertEqual("7.1.26.5", str(version))
        self.assertEqual(7, version[RELEASE1])
        self.assertEqual(1, version[RELEASE2])
        self.assertEqual(26, version[RELEASE3])
        self.assertEqual(5, version[RELEASE4])

    def test_valid_epoch(self):
        version = Pep440Version(4, 3, 11, 8)
        self.assertEqual("4:3.11.8", str(version))
        self.assertEqual(4, version[EPOCH])
        self.assertEqual(3, version[RELEASE1])
        self.assertEqual(11, version[RELEASE2])
        self.assertEqual(8, version[RELEASE3])

    def test_valid_pre_release(self):
        version = Pep440Version(None, 3, 11, 8, pre_release=('a', 2))
        self.assertEqual("3.11.8a2", str(version))
        self.assertEqual(0, version[EPOCH])
        self.assertEqual(3, version[RELEASE1])
        self.assertEqual(11, version[RELEASE2])
        self.assertEqual(8, version[RELEASE3])
        self.assertEqual(0, version[RELEASE4])
        self.assertEqual(0, version[RELEASE5])
        self.assertEqual(0, version[RELEASE6])
        self.assertEqual(('a', 2), version[PRE_RELEASE])
        self.assertEqual(None, version[POST_RELEASE])
        self.assertEqual(None, version[DEVELOPMENT])

    def test_valid_post_release(self):
        version = Pep440Version(None, 3, 11, 8, pre_release=('a', 2))
        self.assertEqual("3.11.8a2", str(version))
        self.assertEqual(0, version[EPOCH])
        self.assertEqual(3, version[RELEASE1])
        self.assertEqual(11, version[RELEASE2])
        self.assertEqual(8, version[RELEASE3])
        self.assertEqual(0, version[RELEASE4])
        self.assertEqual(0, version[RELEASE5])
        self.assertEqual(0, version[RELEASE6])
        self.assertEqual(('a', 2), version[PRE_RELEASE])
        self.assertEqual(None, version[POST_RELEASE])
        self.assertEqual(None, version[DEVELOPMENT])

    def test_valid_pre_and_post_release(self):
        version = Pep440Version(2, 3, 11, 8, pre_release=('a', 2),
                                      post_release=4)
        self.assertEqual("2:3.11.8a2.post4", str(version))
        self.assertEqual(2, version[EPOCH])
        self.assertEqual(3, version[RELEASE1])
        self.assertEqual(11, version[RELEASE2])
        self.assertEqual(8, version[RELEASE3])
        self.assertEqual(0, version[RELEASE4])
        self.assertEqual(0, version[RELEASE5])
        self.assertEqual(0, version[RELEASE6])
        self.assertEqual(('a', 2), version[PRE_RELEASE])
        self.assertEqual(4, version[POST_RELEASE])
        self.assertEqual(None, version[DEVELOPMENT])

    def test_valid_development(self):
        version = Pep440Version(release1=2112, development=90125)
        self.assertEqual("2112.dev90125", str(version))
        self.assertEqual(0, version[EPOCH])
        self.assertEqual(2112, version[RELEASE1])
        self.assertEqual(0, version[RELEASE2])
        self.assertEqual(0, version[RELEASE3])
        self.assertEqual(0, version[RELEASE4])
        self.assertEqual(0, version[RELEASE5])
        self.assertEqual(0, version[RELEASE6])
        self.assertEqual(None, version[PRE_RELEASE])
        self.assertEqual(None, version[POST_RELEASE])
        self.assertEqual(90125, version[DEVELOPMENT])

    def test_valid_pre_release_and_development(self):
        version = Pep440Version(None, 3, 11, 8, pre_release=('a', 2),
                                      development=36)
        self.assertEqual("3.11.8a2.dev36", str(version))
        self.assertEqual(0, version[EPOCH])
        self.assertEqual(3, version[RELEASE1])
        self.assertEqual(11, version[RELEASE2])
        self.assertEqual(8, version[RELEASE3])
        self.assertEqual(0, version[RELEASE4])
        self.assertEqual(0, version[RELEASE5])
        self.assertEqual(0, version[RELEASE6])
        self.assertEqual(('a', 2), version[PRE_RELEASE])
        self.assertEqual(None, version[POST_RELEASE])
        self.assertEqual(36, version[DEVELOPMENT])

    def test_valid_pre_and_post_release_and_development(self):
        version = Pep440Version(1, 3, 11, 8, pre_release=('a', 2),
                                      post_release=5, development=74)
        self.assertEqual("1:3.11.8a2.post5.dev74", str(version))
        self.assertEqual(1, version[EPOCH])
        self.assertEqual(3, version[RELEASE1])
        self.assertEqual(11, version[RELEASE2])
        self.assertEqual(8, version[RELEASE3])
        self.assertEqual(0, version[RELEASE4])
        self.assertEqual(0, version[RELEASE5])
        self.assertEqual(0, version[RELEASE6])
        self.assertEqual(('a', 2), version[PRE_RELEASE])
        self.assertEqual(5, version[POST_RELEASE])
        self.assertEqual(74, version[DEVELOPMENT])

    def test_valid_development_only(self):
        version = Pep440Version(development=666)
        self.assertEqual("0.dev666", str(version))
        self.assertEqual(0, version[EPOCH])
        self.assertEqual(0, version[RELEASE1])
        self.assertEqual(0, version[RELEASE2])
        self.assertEqual(0, version[RELEASE3])
        self.assertEqual(0, version[RELEASE4])
        self.assertEqual(0, version[RELEASE5])
        self.assertEqual(0, version[RELEASE6])
        self.assertEqual(None, version[PRE_RELEASE])
        self.assertEqual(None, version[POST_RELEASE])
        self.assertEqual(666, version[DEVELOPMENT])

    def test_valid_init_string(self):
        version = Pep440Version("1:6.48.2")
        self.assertEqual(1, version[EPOCH])
        self.assertEqual(6, version[RELEASE1])
        self.assertEqual(48, version[RELEASE2])
        self.assertEqual(2, version[RELEASE3])
        self.assertEqual("1:6.48.2", str(version))

    def test_valid_defaulted_segments(self):
        version = Pep440Version(release4=5)
        self.assertEqual("0.0.0.5", str(version))

    def test_render(self):
        version = Pep440Version(development=42)
        self.assertEqual(str(version), version.render())
        self.assertEqual("0.dev42", version.render())
        self.assertEqual("0.0.dev42", version.render(min_release_segments=2))
        self.assertEqual("0.0.0.dev42", version.render(min_release_segments=3))
        self.assertEqual("0:0.0.0.0.0.0.dev42",
                         version.render(exclude_defaults=False))
        version[EPOCH] = 0
        self.assertEqual("0:0.0.dev42", version.render(min_release_segments=2))

    def test_is_release(self):
        version = Pep440Version(development=42)
        self.assertFalse(version.is_release)
        version = Pep440Version(None, 4, 2)
        self.assertTrue(version.is_release)
        version = Pep440Version(release4=11)
        self.assertTrue(version.is_release)


if __name__ == '__main__':
    unittest.main()
