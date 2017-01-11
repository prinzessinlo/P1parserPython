from unittest import TestCase
from P1parser import *

class TestP1parserscanner(TestCase):
    def test_scannercolon(self):
        p1parserscanner(':')
        self.assertEqual(type, 0)
        self.assertEqual(value, 0)
        self.assertTrue(ColonSeen)

    def test_scannerParenthesis(self):
        self.assertEqual(p1parserscanner('('), 0)
        self.assertEqual(value, 0)
        self.assertFalse(ColonSeen)

    def test_upperlowercase(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())