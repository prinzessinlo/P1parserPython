import random
import unittest
from p1parserclass import *


class P1ParserTest(unittest.TestCase):


    def test_choice(self):
        """Test le fonctionnement de la fonction 'random.choice'."""
        liste = list(range(10))
        elt = random.choice(liste)
        # Vérifie que 'elt' est dans 'liste'
        #self.assertIn(elt, liste)

    def test_ParserLookingForLetter1OnSlach(self):
        parser= P1Parser()
        parser.temporarystate == "PARSER_LOOKING_FOR_BEGIN"
        parser.telegram="/"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual("PARSER_LOOKING_FOR_LETTER1", parser.temporarystate)

    def test_ParserLookingForLetter2OnLetter1(self):
        parser= P1Parser()
        parser.temporarystate == "PARSER_LOOKING_FOR_BEGIN"
        parser.telegram="/M"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual("PARSER_LOOKING_FOR_LETTER2", parser.temporarystate)

    def test_ParserLookingForLetter3OnLetter2(self):
        parser= P1Parser()
        parser.temporarystate == "PARSER_LOOKING_FOR_BEGIN"
        parser.telegram="/MC"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual("PARSER_LOOKING_FOR_LETTER3", parser.temporarystate)


    def test_ParserLookingForNumberOnLetter3(self):
        parser= P1Parser()
        parser.temporarystate == "PARSER_LOOKING_FOR_BEGIN"
        parser.telegram="/MMS"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual("PARSER_LOOKING_FOR_NUMBER", parser.temporarystate)

    def test_ParserLookingForCR1OnNumber(self):
        parser= P1Parser()
        parser.temporarystate == "PARSER_LOOKING_FOR_BEGIN"
        parser.telegram="/MMS5"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual("PARSER_LOOKING_FOR_CR1", parser.temporarystate)

    def test_ParserLookingForLF1OnCR1(self):
        parser= P1Parser()
        parser.temporarystate == "PARSER_LOOKING_FOR_BEGIN"
        parser.telegram="/MMS5IDIDID\r"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual("PARSER_LOOKING_FOR_LF1", parser.temporarystate)

    def test_ParserLookingForCR2OnLF1(self):
        parser= P1Parser()
        parser.temporarystate == "PARSER_LOOKING_FOR_BEGIN"
        parser.telegram="/MMS5IDIDID\r\n"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual("PARSER_LOOKING_FOR_CR2", parser.temporarystate)

    def test_ParserLookingForLF2OnCR2(self):
        parser= P1Parser()
        parser.temporarystate == "PARSER_LOOKING_FOR_BEGIN"
        parser.telegram="/MMS5IDIDID\r\n\r"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual("PARSER_LOOKING_FOR_LF2", parser.temporarystate)

    def test_ParserLookingForDATAOnLF2(self):
        parser= P1Parser()
        parser.temporarystate == "PARSER_LOOKING_FOR_BEGIN"
        parser.telegram="/MMS5IDIDID\r\n\r\n"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual("PARSER_LOOKING_FOR_DATAGeneral", parser.temporarystate)

    def test_ParserLookingForEndOfBlockOnDATA(self):
        parser= P1Parser()
        parser.temporarystate == "PARSER_LOOKING_FOR_BEGIN"
        parser.telegram="/MMS5IDIDID\r\n\r\n1-0:0.8.0(00900)\r\n1-0:0.3.0(01000)\r\n1-0:0.3.1(01000)!"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual("PARSER_LOOKING_FOR_ENDOFBLOC", parser.temporarystate)

    def test_ParserLookingForCROnEndOfBlock(self):
        #BlockwithoutCRC "\r\n" after "!"
        parser= P1Parser()
        parser.temporarystate == "PARSER_LOOKING_FOR_BEGIN"
        parser.telegram="/MMS5IDIDID\r\n\r\n1-0:0.8.0(00900)\r\n1-0:0.3.0(01000)\r\n1-0:0.3.1(01000)!\r"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual("PARSER_LOOKING_FOR_LF", parser.temporarystate)

    def test_ParserLookingForLastreturnOnCRLF(self):
        #BlockwithoutCRC "\r\n" after "!"
        parser= P1Parser()
        parser.temporarystate == "PARSER_LOOKING_FOR_BEGIN"
        parser.telegram="/MMS5IDIDID\r\n\r\n1-0:0.8.0(00900)\r\n1-0:0.3.0(01000)\r\n1-0:0.3.1(01000)\r\n!\r\n"
        parser.P1Parser_Receive_char(parser.telegram)
        #self.assertEqual(parser.CRC_is_OK, True)




if __name__ == '__main__':
    unittest.main()