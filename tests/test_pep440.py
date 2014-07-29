# -*- coding: utf-8 -*-
"""PEP 440 verschemes tests"""

import unittest

from verschemes.pep440 import Pep440Version


class Pep440VersionTestCase(unittest.TestCase):

    def test_one_segment(self):
        version = Pep440Version(release1=4)
        self.assertEqual("4", str(version))
        self.assertEqual(0, version.epoch)
        self.assertEqual(4, version.release1)
        self.assertEqual(0, version.release2)
        self.assertEqual(0, version.release3)
        self.assertEqual(0, version.release4)
        self.assertEqual(0, version.release5)
        self.assertEqual(0, version.release6)
        self.assertEqual(None, version.pre_release)
        self.assertEqual(None, version.post_release)
        self.assertEqual(None, version.development)

    def test_two_segments(self):
        version = Pep440Version(release1=8, release2=2)
        self.assertEqual("8.2", str(version))
        self.assertEqual(8, version.release1)
        self.assertEqual(2, version.release2)

    def test_three_segments(self):
        version = Pep440Version(None, 3, 11, 8)
        self.assertEqual("3.11.8", str(version))
        self.assertEqual(3, version.release1)
        self.assertEqual(11, version.release2)
        self.assertEqual(8, version.release3)

    def test_four_segments(self):
        version = Pep440Version(release1=7, release2=1, release3=26,
                                release4=5)
        self.assertEqual("7.1.26.5", str(version))
        self.assertEqual(7, version.release1)
        self.assertEqual(1, version.release2)
        self.assertEqual(26, version.release3)
        self.assertEqual(5, version.release4)

    def test_epoch(self):
        version = Pep440Version(4, 3, 11, 8)
        self.assertEqual("4!3.11.8", str(version))
        self.assertEqual(4, version.epoch)
        self.assertEqual(3, version.release1)
        self.assertEqual(11, version.release2)
        self.assertEqual(8, version.release3)

    def test_pre_release(self):
        version = Pep440Version(None, 3, 11, 8, pre_release=('a', 2))
        self.assertEqual("3.11.8a2", str(version))
        self.assertEqual(0, version.epoch)
        self.assertEqual(3, version.release1)
        self.assertEqual(11, version.release2)
        self.assertEqual(8, version.release3)
        self.assertEqual(0, version.release4)
        self.assertEqual(0, version.release5)
        self.assertEqual(0, version.release6)
        self.assertEqual(('a', 2), version.pre_release)
        self.assertEqual('a', version.pre_release.level)
        self.assertEqual(2, version.pre_release.serial)
        self.assertEqual(None, version.post_release)
        self.assertEqual(None, version.development)

    def test_post_release(self):
        version = Pep440Version(None, 3, 11, 8, pre_release=('a', 2))
        self.assertEqual("3.11.8a2", str(version))
        self.assertEqual(0, version.epoch)
        self.assertEqual(3, version.release1)
        self.assertEqual(11, version.release2)
        self.assertEqual(8, version.release3)
        self.assertEqual(0, version.release4)
        self.assertEqual(0, version.release5)
        self.assertEqual(0, version.release6)
        self.assertEqual(('a', 2), version.pre_release)
        self.assertEqual('a', version.pre_release.level)
        self.assertEqual(2, version.pre_release.serial)
        self.assertEqual(None, version.post_release)
        self.assertEqual(None, version.development)

    def test_pre_and_post_release(self):
        version = Pep440Version(2, 3, 11, 8, pre_release=('a', 2),
                                      post_release=4)
        self.assertEqual("2!3.11.8a2.post4", str(version))
        self.assertEqual(2, version.epoch)
        self.assertEqual(3, version.release1)
        self.assertEqual(11, version.release2)
        self.assertEqual(8, version.release3)
        self.assertEqual(0, version.release4)
        self.assertEqual(0, version.release5)
        self.assertEqual(0, version.release6)
        self.assertEqual(('a', 2), version.pre_release)
        self.assertEqual('a', version.pre_release.level)
        self.assertEqual(2, version.pre_release.serial)
        self.assertEqual(4, version.post_release)
        self.assertEqual(None, version.development)

    def test_development(self):
        version = Pep440Version(release1=2112, development=90125)
        self.assertEqual("2112.dev90125", str(version))
        self.assertEqual(0, version.epoch)
        self.assertEqual(2112, version.release1)
        self.assertEqual(0, version.release2)
        self.assertEqual(0, version.release3)
        self.assertEqual(0, version.release4)
        self.assertEqual(0, version.release5)
        self.assertEqual(0, version.release6)
        self.assertEqual(None, version.pre_release)
        self.assertEqual(None, version.post_release)
        self.assertEqual(90125, version.development)

    def test_pre_release_and_development(self):
        version = Pep440Version(None, 3, 11, 8, pre_release=('a', 2),
                                      development=36)
        self.assertEqual("3.11.8a2.dev36", str(version))
        self.assertEqual(0, version.epoch)
        self.assertEqual(3, version.release1)
        self.assertEqual(11, version.release2)
        self.assertEqual(8, version.release3)
        self.assertEqual(0, version.release4)
        self.assertEqual(0, version.release5)
        self.assertEqual(0, version.release6)
        self.assertEqual(('a', 2), version.pre_release)
        self.assertEqual('a', version.pre_release.level)
        self.assertEqual(2, version.pre_release.serial)
        self.assertEqual(None, version.post_release)
        self.assertEqual(36, version.development)

    def test_pre_and_post_release_and_development(self):
        version = Pep440Version(1, 3, 11, 8, pre_release=('a', 2),
                                      post_release=5, development=74)
        self.assertEqual("1!3.11.8a2.post5.dev74", str(version))
        self.assertEqual(1, version.epoch)
        self.assertEqual(3, version.release1)
        self.assertEqual(11, version.release2)
        self.assertEqual(8, version.release3)
        self.assertEqual(0, version.release4)
        self.assertEqual(0, version.release5)
        self.assertEqual(0, version.release6)
        self.assertEqual(('a', 2), version.pre_release)
        self.assertEqual('a', version.pre_release.level)
        self.assertEqual(2, version.pre_release.serial)
        self.assertEqual(5, version.post_release)
        self.assertEqual(74, version.development)

    def test_development_only(self):
        version = Pep440Version(development=666)
        self.assertEqual("0.dev666", str(version))
        self.assertEqual(0, version.epoch)
        self.assertEqual(0, version.release1)
        self.assertEqual(0, version.release2)
        self.assertEqual(0, version.release3)
        self.assertEqual(0, version.release4)
        self.assertEqual(0, version.release5)
        self.assertEqual(0, version.release6)
        self.assertEqual(None, version.pre_release)
        self.assertEqual(None, version.post_release)
        self.assertEqual(666, version.development)

    def test_init_string(self):
        version = Pep440Version("6.48.2")
        self.assertEqual(0, version.epoch)
        self.assertEqual(6, version.release1)
        self.assertEqual(48, version.release2)
        self.assertEqual(2, version.release3)
        self.assertEqual("6.48.2", str(version))

    def test_init_string_epoch(self):
        version = Pep440Version("1!6.48.2")
        self.assertEqual(1, version.epoch)
        self.assertEqual(6, version.release1)
        self.assertEqual(48, version.release2)
        self.assertEqual(2, version.release3)
        self.assertEqual("1!6.48.2", str(version))

    def test_init_string_alpha_separator(self):
        indicators = ("a", "A", "alpha", "alpHA", "Alpha", "AlPHa", "ALPHA")
        expected = "1.2a3"
        for indicator in indicators:
            self.assertEqual(expected,
                             str(Pep440Version("1.2{}3".format(indicator))))
            self.assertEqual(expected,
                             str(Pep440Version("1.2.{}3".format(indicator))))
            self.assertEqual(expected,
                             str(Pep440Version("1.2-{}3".format(indicator))))
        expected = "1.2a0"
        for indicator in indicators:
            self.assertEqual(expected,
                             str(Pep440Version("1.2{}".format(indicator))))
            self.assertEqual(expected,
                             str(Pep440Version("1.2.{}".format(indicator))))
            self.assertEqual(expected,
                             str(Pep440Version("1.2-{}".format(indicator))))

    def test_init_string_beta_separator(self):
        indicators = ("b", "B", "beta", "beTA", "Beta", "BeTa", "BETA")
        expected = "1.2b3"
        for indicator in indicators:
            self.assertEqual(expected,
                             str(Pep440Version("1.2{}3".format(indicator))))
            self.assertEqual(expected,
                             str(Pep440Version("1.2.{}3".format(indicator))))
            self.assertEqual(expected,
                             str(Pep440Version("1.2-{}3".format(indicator))))
        expected = "1.2b0"
        for indicator in indicators:
            self.assertEqual(expected,
                             str(Pep440Version("1.2{}".format(indicator))))
            self.assertEqual(expected,
                             str(Pep440Version("1.2.{}".format(indicator))))
            self.assertEqual(expected,
                             str(Pep440Version("1.2-{}".format(indicator))))

    def test_init_string_release_candidate_separator(self):
        indicators = ("c", "C", "rc", "RC", "rC", "Rc")
        expected = "1.2c3"
        for indicator in indicators:
            self.assertEqual(expected,
                             str(Pep440Version("1.2{}3".format(indicator))))
            self.assertEqual(expected,
                             str(Pep440Version("1.2.{}3".format(indicator))))
            self.assertEqual(expected,
                             str(Pep440Version("1.2-{}3".format(indicator))))
        expected = "1.2c0"
        for indicator in indicators:
            self.assertEqual(expected,
                             str(Pep440Version("1.2{}".format(indicator))))
            self.assertEqual(expected,
                             str(Pep440Version("1.2.{}".format(indicator))))
            self.assertEqual(expected,
                             str(Pep440Version("1.2-{}".format(indicator))))

    def test_init_string_post_release_separator(self):
        expected = "1.2.post3"
        self.assertEqual(expected, str(Pep440Version("1.2post3")))
        self.assertEqual(expected, str(Pep440Version("1.2.post3")))
        self.assertEqual(expected, str(Pep440Version("1.2-post3")))
        expected = "1.2.post0"
        self.assertEqual(expected, str(Pep440Version("1.2post")))
        self.assertEqual(expected, str(Pep440Version("1.2.post")))
        self.assertEqual(expected, str(Pep440Version("1.2-post")))

    def test_init_string_development_separator(self):
        expected = "1.2.dev3"
        self.assertEqual(expected, str(Pep440Version("1.2dev3")))
        self.assertEqual(expected, str(Pep440Version("1.2.dev3")))
        self.assertEqual(expected, str(Pep440Version("1.2-dev3")))
        expected = "1.2.dev0"
        self.assertEqual(expected, str(Pep440Version("1.2dev")))
        self.assertEqual(expected, str(Pep440Version("1.2.dev")))
        self.assertEqual(expected, str(Pep440Version("1.2-dev")))

    def test_defaulted_segments(self):
        version = Pep440Version(release4=5)
        self.assertEqual("0.0.0.5", str(version))

    def test_render(self):
        version = Pep440Version(development=42)
        self.assertEqual(str(version), version.render())
        self.assertEqual("0.dev42", version.render())
        self.assertEqual("0.0.dev42", version.render(min_release_segments=2))
        self.assertEqual("0.0.0.dev42", version.render(min_release_segments=3))
        self.assertEqual("0!0.0.0.0.0.0.dev42",
                         version.render(exclude_defaults=False))
        version = version.replace(epoch=0)
        self.assertEqual("0!0.0.dev42", version.render(min_release_segments=2))

    def test_render_exclude_defaults_callback_scope(self):
        version = Pep440Version()
        self.assertTrue(version._render_exclude_defaults_callback(0, [1, 2]))
        self.assertFalse(version._render_exclude_defaults_callback(1, [1, 2]))

    def test_is_release(self):
        version = Pep440Version(development=42)
        self.assertFalse(version.is_release)
        version = Pep440Version(None, 4, 2)
        self.assertTrue(version.is_release)
        version = Pep440Version(release4=11)
        self.assertTrue(version.is_release)
