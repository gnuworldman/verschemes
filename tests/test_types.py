# -*- coding: utf-8 -*-
"""verschemes._types tests"""

from __future__ import absolute_import
from __future__ import unicode_literals

import unittest

from verschemes._types import int_default_zero


class IntDefaultZeroTestCase(unittest.TestCase):

    def test_int(self):
        self.assertEqual(1, int_default_zero(1))

    def test_string(self):
        self.assertEqual(1, int_default_zero("1"))

    def test_empty_string(self):
        self.assertEqual(0, int_default_zero(""))

    def test_none(self):
        self.assertEqual(0, int_default_zero(None))

    def test_int_keyword(self):
        self.assertEqual(1, int_default_zero(x=1))

    def test_string_keyword(self):
        self.assertEqual(1, int_default_zero(x="1"))

    def test_empty_string_keyword(self):
        self.assertEqual(0, int_default_zero(x=""))

    def test_none_keyword(self):
        self.assertEqual(0, int_default_zero(x=None))
