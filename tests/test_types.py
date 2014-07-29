# -*- coding: utf-8 -*-
"""verschemes._types tests"""

import unittest

from verschemes._types import int_empty_zero


class IntDefaultZeroTestCase(unittest.TestCase):

    def test_int(self):
        self.assertEqual(1, int_empty_zero(1))

    def test_string(self):
        self.assertEqual(1, int_empty_zero("1"))

    def test_empty_string(self):
        self.assertEqual(0, int_empty_zero(""))

    def test_none(self):
        self.assertRaises(TypeError, int_empty_zero, None)

    def test_int_keyword(self):
        self.assertEqual(1, int_empty_zero(x=1))

    def test_string_keyword(self):
        self.assertEqual(1, int_empty_zero(x="1"))

    def test_empty_string_keyword(self):
        self.assertEqual(0, int_empty_zero(x=""))

    def test_none_keyword(self):
        self.assertRaises(TypeError, int_empty_zero, x=None)
