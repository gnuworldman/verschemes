"""verschemes unit tests"""

# Support Python 2 & 3.
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from verschemes.future import *

import operator
import re
import sys
import types
import unittest

from verschemes import SegmentDefinition, SegmentField, Version, _VersionMeta


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

    def test_init_segment_name_not_identifier(self):
        self.assertRaises(ValueError, SegmentDefinition, name='oop$')

    def test_init_segment_name_starts_with_underscore(self):
        self.assertRaises(ValueError, SegmentDefinition, name='_oops')

    def test_init_separator_re_pattern_invalid_re(self):
        self.assertRaises(re.error, SegmentDefinition,
                          separator_re_pattern='unpaired(parenthesis')

    def test_init_separator_re_pattern_invalid_type(self):
        self.assertRaises(TypeError, SegmentDefinition,
                          separator_re_pattern=4)

    def test_eq_default(self):
        self.assertEqual(SegmentDefinition(), SegmentDefinition())

    def test_eq_name(self):
        self.assertEqual(SegmentDefinition(name='same'),
                         SegmentDefinition(name='same'))

    def test_ne_name(self):
        self.assertNotEqual(SegmentDefinition(name='different1'),
                            SegmentDefinition(name='different2'))

    def test_render(self):
        sd = SegmentDefinition()
        self.assertEqual('5', sd.render(5))

    def test_render_muliple_fields(self):
        sd = SegmentDefinition(fields=(SegmentField(name='a'),
                                       SegmentField(name='b')))
        self.assertEqual('138', sd.render((13, 8)))

    def test_validate_value(self):
        sd = SegmentDefinition(fields=(SegmentField(name='a'),
                                       SegmentField(name='b')))
        self.assertEqual((1, 2), sd.validate_value((1, 2)))
        self.assertEqual((4, 3), sd.validate_value([4, 3]))

    def test_validate_value_missing(self):
        sd = SegmentDefinition()
        self.assertRaises(ValueError, sd.validate_value, None)

    def test_validate_value_partial(self):
        sd = SegmentDefinition(fields=(
            SegmentField(name='a'),
            SegmentField(name='b',
                         re_pattern='(?<=[0])|(?<![0])(?:0|[1-9][0-9]*)',
                         render=lambda x: "" if x is None else str(x))))
        self.assertEqual((0, None), sd.validate_value((0, None)))
        self.assertEqual((0, None), sd.validate_value((0,)))
        self.assertRaises(ValueError, sd.validate_value, (0, 3))
        self.assertEqual((1, 2), sd.validate_value((1, 2)))
        self.assertRaises(ValueError, sd.validate_value, (1,))


class VersionMetaTestCase(unittest.TestCase):

    def test_lack_of_segment_definitions(self):
        # has valid SEGMENT_DEFINITIONS, so succeeds
        _VersionMeta('NewVersion', (), dict(SEGMENT_DEFINITIONS=()))
        # has no SEGMENT_DEFINITIONS, so fails
        self.assertRaises(TypeError, _VersionMeta, 'NonVersion', (), {})
        # same but with a base class
        self.assertRaises(TypeError, _VersionMeta, 'NonVersion', (object,), {})


class VersionTestCase(unittest.TestCase):

    def test_invalid_segment_definitions(self):
        invalids = [
            ('not',),  # iterable, but not a SegmentDefinition
            666,  # not even an iterable
        ]
        for invalid in invalids:
            self.assertRaises(TypeError, type, 'VersionBad', (Version,),
                              dict(SEGMENT_DEFINITIONS=invalid))

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
        # Non-matching string raises exception.
        self.assertRaises(ValueError, VersionString, "1.2x.3")

    def test_init_value_string_no_separator(self):
        class Version1(Version):
            SEGMENT_DEFINITIONS = (
                SegmentDefinition(
                    optional=True,
                    default=0,
                ),
                SegmentDefinition(
                    separator='',
                    fields=SegmentField(type=str,
                                        re_pattern='[a-z]')),
            )
        self.assertEqual("2x", str(Version1("2x")))
        self.assertEqual("0x", str(Version1("0x")))
        self.assertEqual("0x", str(Version1("x")))

    def test_init_values_exceed_definitions(self):
        class Version1(Version):
            SEGMENT_DEFINITIONS = (SegmentDefinition(),)
        # Specifying one segment value succeeds.
        Version1(1)
        # Specifying two segment values fails.
        self.assertRaises(ValueError, Version1, 1, 2)

    def test_init_definitions_exceed_values(self):
        class Version1(Version):
            SEGMENT_DEFINITIONS = (SegmentDefinition(),
                                   SegmentDefinition(default=0))
        version = Version1(1)
        self.assertEqual(1, version[0])
        self.assertEqual(0, version[1])

    def test_init_definitions_all_optional(self):
        self.assertRaises(ValueError, type, 'Version1', (Version,),
                          dict(SEGMENT_DEFINITIONS=
                               (SegmentDefinition(optional=True, default=0),
                                SegmentDefinition(optional=True, default=0))))

    def test_init_definitions_first_optional(self):
        class Version1(Version):
            SEGMENT_DEFINITIONS = (SegmentDefinition(optional=True,
                                                     default=0),
                                   SegmentDefinition(default=0))
        version = Version1("7")
        self.assertEqual("0.7", str(version))
        self.assertEqual(0, version[0])
        self.assertEqual(7, version[1])

    def test_init_segment_name_duplicate(self):
        self.assertRaises(ValueError, type, 'VersionBad', (Version,),
                          dict(SEGMENT_DEFINITIONS=
                               (SegmentDefinition(name='oops'),
                                SegmentDefinition(name='unique'),
                                SegmentDefinition(name='oops'))))

    def test_invalid_attribute(self):
        version = Version(1, 2, 3)
        # Version objects are immutable and have no __dict__.
        self.assertRaises(AttributeError, getattr, version, '__dict__')
        self.assertRaises(AttributeError, setattr, version,
                          'nonexistent_attribute', 0)

    def test_repr(self):
        expected = 'verschemes.Version(3, 5, 8, 13)'
        self.assertEqual(expected, repr(Version(3, 5, 8, 13)))
        self.assertEqual(expected, repr(Version('3.5.8.13')))

    def test_eq(self):
        self.assertEqual(Version(8, 13, 21), Version(8, 13, 21))

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
        if sys.version_info[0] < 3:
            # The complex type seems to have a comparison that does not raise a
            # TypeError exception and instead returns an actual boolean value
            # in Python 2 (complex instance less than any Version, it seems).
            self.assertFalse(Version(7, 5, 2) < complex(7.6, 2))
        else:
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

    def test_optional_segments(self):
        # All segments are separated by '.'; two segments are required.
        class Version1(Version):
            SEGMENT_DEFINITIONS = (SegmentDefinition(optional=True,
                                                     default=1),
                                   SegmentDefinition(default=2),
                                   SegmentDefinition(),
                                   SegmentDefinition(optional=True,
                                                     default=4),
                                   SegmentDefinition(),
                                   SegmentDefinition(optional=True))
        # One segment is not enough.
        self.assertRaises(ValueError, Version1, '6')
        # The two segments given fill the two required.
        self.assertEqual('1.2.6.4.7', str(Version1('6.7')))
        # More than two segments fills earliest non-required first.
        self.assertEqual('6.2.7.4.8', str(Version1('6.7.8')))
        self.assertEqual('6.7.8.4.9', str(Version1('6.7.8.9')))
        self.assertEqual('6.7.8.9.0', str(Version1('6.7.8.9.0')))

    def test_separator_re_pattern(self):
        class Version1(Version):
            SEGMENT_DEFINITIONS = (
                SegmentDefinition(),
                SegmentDefinition(separator_re_pattern='[.,-]'),
            )
        self.assertEqual('1.2', Version1('1.2'))
        self.assertEqual('1.2', Version1('1,2'))
        self.assertEqual('1.2', Version1('1-2'))


class VersionRenderTestCase(unittest.TestCase):

    def setUp(self):
        class Version1(Version):
            SEGMENT_DEFINITIONS = (SegmentDefinition(name='first'),
                                   SegmentDefinition(name='second',
                                                     default=2),
                                   SegmentDefinition(name='third',
                                                     optional=True,
                                                     default=3),
                                   SegmentDefinition(name='fourth',
                                                     optional=True,
                                                     default=4),
                                   SegmentDefinition(name='fifth',
                                                     optional=True))
        self.version_class = Version1
        self.version = Version1(1)

    def test_render(self):
        self.assertEqual('1.2', self.version.render())

    def test_render_include_defaults(self):
        self.assertEqual('1.2.3.4',
                         self.version.render(exclude_defaults=False))

    def test_render_include_callback_with_fixed_arg(self):
        def callback(version, index, test_arg):
            self.assertEqual('Red Tide', test_arg)
            return True
        self.assertEqual('1.2.3.4',
                         self.version.render(include_callbacks=
                                             [(callback, 'Red Tide')]))

    def test_render_include_callback_conditional(self):
        def callback(version, index):
            return index < 3
        self.assertEqual('1.2.3',
                         self.version.render(include_callbacks=[callback]))

    def test_render_exclude_defaults_callback_override(self):
        class Version1(Version):
            SEGMENT_DEFINITIONS = (
                SegmentDefinition(name='first'),
                SegmentDefinition(name='second', default=2),
                SegmentDefinition(name='third', optional=True, default=3),
                SegmentDefinition(name='fourth', optional=True, default=4),
                SegmentDefinition(name='fifth', optional=True, default=5),
            )
        class Version2(Version1):
            def _render_exclude_defaults_callback(self, index, scope=None):
                if scope is None:
                    scope = range(4)
                return super()._render_exclude_defaults_callback(index, scope)
        version1 = Version1(1, fifth=50)
        version2 = Version2(1, fifth=50)
        version2_with_third = Version2(1, third=30, fifth=50)
        version2_with_fourth = Version2(1, fourth=40, fifth=50)
        # when the callback's scope includes 'fifth'
        self.assertEqual('1.2.3.4.50', version1.render())
        # when it does not include 'fifth'
        self.assertEqual('1.2.50', version2.render())
        self.assertEqual('1.2.30.50', version2_with_third.render())
        self.assertEqual('1.2.3.40.50', version2_with_fourth.render())


class VersionSegmentAccessTestCase(unittest.TestCase):

    def setUp(self):
        class VersionNamed(Version):
            SEGMENT_DEFINITIONS = (SegmentDefinition(name='first'),
                                   SegmentDefinition(name='second'),
                                   SegmentDefinition(name='third'))
        class VersionNamedWithDefault(Version):
            SEGMENT_DEFINITIONS = (SegmentDefinition(name='first'),
                                   SegmentDefinition(name='second',
                                                     default=6),
                                   SegmentDefinition(name='third'))
        class VersionNamedConflict(Version):
            SEGMENT_DEFINITIONS = (SegmentDefinition(name='render'),
                                   SegmentDefinition(name='second'),
                                   SegmentDefinition(name='replace'))
        self.version = VersionNamed(5, 12, 7)
        self.version_defaulted = VersionNamedWithDefault(3, third=4)
        self.version_conflict = VersionNamedConflict(1, 2, 3)

    def test_index(self):
        self.assertEqual(5, self.version[0])
        self.assertEqual(12, self.version[1])
        self.assertEqual(7, self.version[2])
        self.assertEqual(3, self.version_defaulted[0])
        self.assertEqual(6, self.version_defaulted[1])
        self.assertEqual(4, self.version_defaulted[2])
        self.assertEqual(1, self.version_conflict[0])
        self.assertEqual(2, self.version_conflict[1])
        self.assertEqual(3, self.version_conflict[2])

    def test_slice(self):
        self.assertEqual((5, 12), self.version[:2])
        self.assertEqual((12, 7), self.version[1:])
        self.assertEqual((3, 6), self.version_defaulted[:2])
        self.assertEqual((6, 4), self.version_defaulted[1:])
        self.assertEqual((1, 2), self.version_conflict[:2])
        self.assertEqual((2, 3), self.version_conflict[1:])

    def test_keyword(self):
        self.assertEqual(5, self.version['first'])
        self.assertEqual(12, self.version['second'])
        self.assertEqual(7, self.version['third'])
        self.assertEqual(3, self.version_defaulted['first'])
        self.assertEqual(6, self.version_defaulted['second'])
        self.assertEqual(4, self.version_defaulted['third'])
        self.assertEqual(1, self.version_conflict['render'])
        self.assertEqual(2, self.version_conflict['second'])
        self.assertEqual(3, self.version_conflict['replace'])

    def test_property(self):
        self.assertEqual(5, self.version.first)
        self.assertEqual(12, self.version.second)
        self.assertEqual(7, self.version.third)
        self.assertEqual(3, self.version_defaulted.first)
        self.assertEqual(6, self.version_defaulted.second)
        self.assertEqual(4, self.version_defaulted.third)
        # The segment's name matches a method attribute name.
        self.assertIsInstance(self.version_conflict.render, types.MethodType)
        # The segment's name does not match an existing attribute name.
        self.assertEqual(2, self.version_conflict.second)
        # The segment's name matches a method attribute name.
        self.assertIsInstance(self.version_conflict.replace, types.MethodType)

    def test_raw_index(self):
        self.assertEqual(3, self.version_defaulted.get_raw_item(0))
        self.assertEqual(None, self.version_defaulted.get_raw_item(1))
        self.assertEqual(4, self.version_defaulted.get_raw_item(2))

    def test_raw_slice(self):
        self.assertEqual((3, None),
                         self.version_defaulted.get_raw_item(slice(2)))
        self.assertEqual((None, 4),
                         self.version_defaulted.get_raw_item(slice(1, 3)))

    def test_raw_keyword(self):
        self.assertEqual(3, self.version_defaulted.get_raw_item('first'))
        self.assertEqual(None, self.version_defaulted.get_raw_item('second'))
        self.assertEqual(4, self.version_defaulted.get_raw_item('third'))

    def test_invalid_index(self):
        self.assertEqual(7, self.version.__getitem__(2))
        self.assertRaises(IndexError, self.version.__getitem__, 3)

    def test_invalid_keyword(self):
        self.assertEqual(7, self.version.__getitem__('third'))
        self.assertRaises(KeyError, self.version.__getitem__, 'fourth')

    def test_invalid_property(self):
        self.assertEqual(7, getattr(self.version, 'third'))
        self.assertRaises(AttributeError, getattr, self.version, 'fourth')

    def test_invalid_raw_index(self):
        self.assertEqual(7, self.version.get_raw_item(2))
        self.assertRaises(IndexError, self.version.get_raw_item, 3)

    def test_invalid_raw_keyword(self):
        self.assertEqual(7, self.version.get_raw_item('third'))
        self.assertRaises(KeyError, self.version.get_raw_item, 'fourth')
