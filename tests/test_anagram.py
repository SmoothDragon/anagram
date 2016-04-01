#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_anagram
----------------------------------

Tests for `anagram` module.
"""

import unittest

from anagram import *


class TestAnagram(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_distill_input(self):
        self.assertEqual(distill_query('aBb2eE'), ('BE', 'ABE', 2))


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
