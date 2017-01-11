from unittest import TestCase
from P1parser import *

class TestExtractvalues(TestCase):
    def test_listofdatavalue(self):
        DataFromTelegram1 = "/XXX5AMEL\n\n1-0:1.8.0(000333.01*kWh)\n1-0:2.8.0(000111.72*kWh)\n1-0:1.7.0(000229.88*kWh)\n1-0:2.7.0(000235.19*kWh)\n!ABCD\n"
        extractvalues(DataFromTelegram1)
        self.assertEqual(33301, ListofDataValues[0])
        self.assertEqual(11172, ListofDataValues[1])
        self.assertEqual(22988, ListofDataValues[2])
        self.assertEqual(23519, ListofDataValues[3])


