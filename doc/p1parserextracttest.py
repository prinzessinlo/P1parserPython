from p1parserclass import *
import unittest


class P1extractTest(unittest.TestCase):


    def test_IfReturningRightTypeAndValue(self):
        parser = P1Parser()
        parser.extractvalues("1-0:1.8.3(000666.666*kWh)")
        type= parser.P1P_GetType()
        self.assertEqual(type, 183)
        value = parser.P1P_GetValue()
        self.assertEqual(value, 666666)

    def test_IfFulfillingListOfValuewithWishedValues(self):
        parser = P1Parser()
        input= "1-0:1.8.0(000671.578*kWh)\r\n1-0:2.8.0(000842.472*kWh)\r\n1-0:1.7.0(00.333*kW)\r\n1-0:2.7.0(00.444*kW)\r\n"
        #we just give data(databuffer) to the method extractvalues
        parser.extractvalues(input)
        self.assertEqual(parser.ListofDataValues[0], 671578)
        self.assertEqual(parser.ListofDataValues[1], 842472)
        self.assertEqual(parser.ListofDataValues[2], 333)
        self.assertEqual(parser.ListofDataValues[3], 444)