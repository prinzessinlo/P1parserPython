import random
from p1parserclass import *
import unittest


class P1ScannerTest(unittest.TestCase):


    def test_IfCharisColon(self):
        parser = P1Parser()
        parser.p1parserscanner(":")
        self.assertEqual(parser.type,0)
        self.assertEqual(parser.value, 0)
        self.assertTrue(parser.ColonSeen)

    def test_IfCharisOpenParenthesis(self):
        parser = P1Parser()
        parser.p1parserscanner("(")
        self.assertEqual(parser.type,0)
        self.assertEqual(parser.value, 0)
        if (parser.type==0):
            self.assertEqual(parser.type, parser.value)
        self.assertFalse(parser.DotSeen)
        self.assertFalse(parser.ColonSeen)
        self.assertTrue(parser.ParenthesisSeen)

    def test_IfCharisPoint(self):
        parser = P1Parser()
        parser.p1parserscanner(".")
        self.assertTrue(parser.Dotseen)

    def test_IfCharisCloseParenthesis(self):
        parser = P1Parser()
        parser.DotSeen= True
        parser.type= 111
        self.assertTrue(parser.p1parserscanner(")"))

    def test_IfCharisStar(self):
        parser = P1Parser()
        parser.p1parserscanner("*")
        self.assertTrue(parser.StarSeen)

    def test_Returningrighttypeandvalue(self):
        string= "1-0:1.8.0(000671.578*kWh)"
        parser = P1Parser()
        for letter in string:
            parser.p1parserscanner(letter)
        self.assertEqual(parser.type, 180)
        self.assertEqual(parser.value, 671578)
