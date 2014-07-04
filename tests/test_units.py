"""versioning function unit tests"""

import operator
import unittest

from verschemes import *


class SegmentFieldTestCase(unittest.TestCase):

    def test_eq_default(self):
        self.assertEqual(SegmentField(), SegmentField())

    def test_eq_type(self):
        self.assertEqual(SegmentField(type=str), SegmentField(type=str))

    def test_eq_name(self):
        self.assertEqual(SegmentField(name='same'), SegmentField(name='same'))

    def test_eq_re_pattern(self):
        self.assertEqual(SegmentField(re_pattern='[0-9]*'),
                         SegmentField(re_pattern='[0-9]*'))

    def test_eq_name_and_re_pattern(self):
        self.assertEqual(SegmentField(name='same', re_pattern='[0-9]*'),
                         SegmentField(name='same', re_pattern='[0-9]*'))

    def test_eq_type_and_name_and_re_pattern(self):
        self.assertEqual(SegmentField(type=str, name='same', re_pattern='x+'),
                         SegmentField(type=str, name='same', re_pattern='x+'))

    def test_ne_type(self):
        self.assertNotEqual(SegmentField(), SegmentField(type=str))

    def test_ne_name(self):
        self.assertNotEqual(SegmentField(), SegmentField(name='different'))

    def test_ne_re_pattern(self):
        self.assertNotEqual(SegmentField(), SegmentField(re_pattern='[0-5]'))


class SegmentDefinitionTestCase(unittest.TestCase):

    def test_init_fields_noniterable(self):
        self.assertEqual(SegmentDefinition(),
                         SegmentDefinition(fields=SegmentField()))

    def test_init_fields_bad_type(self):
        self.assertRaises(ValueError, SegmentDefinition, fields='wrong')

    def test_init_fields_name_duplicate_default(self):
        fields = (SegmentField(), SegmentField())
        self.assertRaises(ValueError, SegmentDefinition, fields=fields)

    def test_init_fields_name_duplicate(self):
        fields = (SegmentField(name='oops'), SegmentField(name='oops'))
        self.assertRaises(ValueError, SegmentDefinition, fields=fields)

    def test_eq_default(self):
        self.assertEqual(SegmentDefinition(), SegmentDefinition())


class VersionTestCase(unittest.TestCase):

    def test_invalid_segment_definitions(self):
        class VersionBad(Version):
            SEGMENT_DEFINITIONS = (
                'not a SegmentDefinition',
            )
        self.assertRaises(TypeError, VersionBad, 1)

    def test_init_no_values(self):
        self.assertRaises(ValueError, Version)

    def test_init_value_string_parsed(self):
        version = Version('1.2.3')
        self.assertEqual(1, version[0])

    def test_init_value_string_not_parsed(self):
        class VersionString(Version):
            SEGMENT_DEFINITIONS = (
                SegmentDefinition(
                    fields=SegmentField(type=str,
                                        re_pattern='[0-9]+(?:[.][0-9]+)*')),
            )
        version = VersionString('1.2.3')
        self.assertEqual('1.2.3', version[0])
        self.assertRaises(IndexError, version.__getitem__, 1)

    def test_init_value_string_does_not_match_re(self):
        class VersionString(Version):
            SEGMENT_DEFINITIONS = (
                SegmentDefinition(
                    fields=SegmentField(type=str,
                                        re_pattern='[0-9]+(?:[.][0-9]+)*')),
            )
        # Matching string succeeds.
        VersionString("1.2.3")
        self.assertRaises(ValueError, VersionString, "1.2x.3")

    def test_init_values_exceed_definitions(self):
        class Version1(Version):
            SEGMENT_DEFINITIONS = (SegmentDefinition(),)
        # Specifying one segment value succeeds.
        Version1(1)
        # Specifying two segment values fails.
        self.assertRaises(ValueError, Version1, 1, 2)

    def test_repr(self):
        version = Version(3, 5, 8, 13)
        self.assertEqual("verschemes.Version(3, 5, 8, 13)", repr(version))
        version = Version('3.5.8.13')
        self.assertEqual("verschemes.Version(3, 5, 8, 13)", repr(version))

    def test_eq(self):
        self.assertEqual(Version('8.13.21'), Version(8, 13, 21))

    def test_eq_different_type_same_segment_definitions(self):
        class Version1(Version):
            SEGMENT_DEFINITIONS = (SegmentDefinition(),)
        self.assertEqual(Version(7), Version1(7))

    def test_eq_string(self):
        self.assertEqual(Version(8, 13, 21), '8.13.21')

    def test_eq_float(self):
        self.assertEqual(Version(8, 13), 8.13)

    def test_eq_incompatible(self):
        self.assertNotEqual(Version(8, 13, 21), complex(8.13, 21))

    def test_eq_different_segment_definitions(self):
        class Version1(Version):
            SEGMENT_DEFINITIONS = (SegmentDefinition(default=1),)
        self.assertEqual(Version(7), Version1(7))

    def test_ne_value(self):
        self.assertNotEqual(Version(1), Version(2))

    def test_lt_value(self):
        self.assertLess(Version(1), Version(2))

    def test_lt_string(self):
        self.assertLess(Version(8, 13, 21), '8.2db')

    def test_lt_float(self):
        self.assertLess(Version(8, 13), 9.0)

    def test_lt_incompatible(self):
        self.assertRaises(TypeError, operator.lt,
                          Version(7, 5, 2), complex(7.6, 2))

    def test_lt_different_segment_definitions(self):
        class Version1(Version):
            SEGMENT_DEFINITIONS = (SegmentDefinition(default=1),)
        version = Version(7)
        version1 = Version1(8)
        self.assertLess(version, version1)
        self.assertFalse(version1 < version)
        version1 = Version1(7)
        self.assertFalse(version < version1)
        self.assertFalse(version1 < version)
