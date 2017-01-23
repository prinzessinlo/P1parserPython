import random
from p1parserclass import *
import unittest


class P1ParserTest(unittest.TestCase):


    def test_choice(self):
        """Test le fonctionnement de la fonction 'random.choice'."""
        liste = list(range(10))
        elt = random.choice(liste)
        # Vérifie que 'elt' est dans 'liste'
        #self.assertIn(elt, liste)

    def test_ParserLookingForLetter1OnSlach(self):
        parser= P1Parser()
        parser.temporarystate = "PARSER_LOOKING_FOR_BEGIN"
        parser.telegram="/"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual("PARSER_LOOKING_FOR_LETTER1", parser.temporarystate)

    def test_ParserLookingForLetter2OnLetter1(self):
        parser= P1Parser()
        parser.temporarystate = "PARSER_LOOKING_FOR_BEGIN"
        parser.telegram="/M"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual("PARSER_LOOKING_FOR_LETTER2", parser.temporarystate)

    def test_ParserLookingForLetter3OnLetter2(self):
        parser= P1Parser()
        parser.temporarystate = "PARSER_LOOKING_FOR_BEGIN"
        parser.telegram="/MC"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual("PARSER_LOOKING_FOR_LETTER3", parser.temporarystate)


    def test_ParserLookingForNumberOnLetter3(self):
        parser= P1Parser()
        parser.temporarystate = "PARSER_LOOKING_FOR_BEGIN"
        parser.telegram="/MMS"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual("PARSER_LOOKING_FOR_NUMBER", parser.temporarystate)

    def test_ParserLookingForCR1OnNumber(self):
        parser= P1Parser()
        parser.temporarystate = "PARSER_LOOKING_FOR_BEGIN"
        parser.telegram="/MMS5"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual("PARSER_LOOKING_FOR_CR1", parser.temporarystate)

    def test_ParserLookingForLF1OnCR1(self):
        parser= P1Parser()
        parser.temporarystate = "PARSER_LOOKING_FOR_BEGIN"
        parser.telegram="/MMS5IDIDID\r"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual("PARSER_LOOKING_FOR_LF1", parser.temporarystate)

    def test_ParserLookingForCR2OnLF1(self):
        parser= P1Parser()
        parser.temporarystate = "PARSER_LOOKING_FOR_BEGIN"
        parser.telegram="/MMS5IDIDID\r\n"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual("PARSER_LOOKING_FOR_CR2", parser.temporarystate)

    def test_ParserLookingForLF2OnCR2(self):
        parser= P1Parser()
        parser.temporarystate = "PARSER_LOOKING_FOR_BEGIN"
        parser.telegram="/MMS5IDIDID\r\n\r"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual("PARSER_LOOKING_FOR_LF2", parser.temporarystate)

    def test_ParserLookingForDATAOnLF2(self):
        parser= P1Parser()
        parser.temporarystate = "PARSER_LOOKING_FOR_BEGIN"
        parser.telegram="/MMS5IDIDID\r\n\r\n"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual("PARSER_LOOKING_FOR_DATAGeneral", parser.temporarystate)
    #case 1
    def test_ParserLookingForBeginOnNOData(self):
        parser= P1Parser()
        parser.temporarystate = "PARSER_LOOKING_FOR_BEGIN"
        parser.telegram="/MMS5IDIDID\r\n\r\n\0"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual("PARSER_LOOKING_FOR_BEGIN", parser.temporarystate)

    #case 2

    def test_ParserIncreaseDataIdxIfWedidntreachExclamationpoint(self):
        parser = P1Parser()
        parser.temporarystate = "PARSER_LOOKING_FOR_BEGIN"
        parser.telegram = "/MMS5IDIDID\r\n\r\n1-0:0.8.0(00900)"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertGreater(parser.DataIdx, 0)
        self.assertEqual("PARSER_LOOKING_FOR_DATAGeneral", parser.temporarystate)

    # case 3
    def test_ParserRejectWhenFindExclamationandDataLenisZero(self):
        parser = P1Parser()
        parser.temporarystate = "PARSER_LOOKING_FOR_DATAGeneral"
        parser.telegram = "!"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual("PARSER_LOOKING_FOR_BEGIN", parser.temporarystate)

    # case 4
    def test_ParserLookingForEndOfBlockOnDATA(self):
        parser= P1Parser()
        parser.temporarystate = "PARSER_LOOKING_FOR_DATAGeneral"
        parser.telegram="1-0:0.8.0(00900)\r\n1-0:0.3.1(01000)\r\n!"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertGreater(parser.DataIdx, 0)
        self.assertEqual("PARSER_LOOKING_FOR_ENDOFBLOC", parser.temporarystate)
    #No CRC, CRLF at the endoftheblock
    def test_ParserLookingForCROnEndOfBlock(self):
        #BlockwithoutCRC "\r\n" after "!"
        parser= P1Parser()
        parser.temporarystate = "PARSER_LOOKING_FOR_ENDOFBLOC"
        parser.telegram="\r"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual("PARSER_LOOKING_FOR_LF", parser.temporarystate)

    def test_ParserLookingForLastreturnOnCRLF(self):
        #BlockwithoutCRC "\r\n" after "!"
        parser= P1Parser()
        parser.temporarystate = "PARSER_LOOKING_FOR_ENDOFBLOC"
        parser.telegram="\r\n"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertTrue(parser.CRC_is_OK)

    #We've CRC+CRLF at the endoftheblock

    #case 5
    def test_ParserLookingForCRCOnExclamation(self):
        #BlockwithCRC after "!"
        parser= P1Parser()
        parser.temporarystate = "PARSER_LOOKING_FOR_ENDOFBLOC"
        parser.telegram="A"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual(parser.CRCLen,1)
        self.assertEqual(parser.bufferCRC, "A")
        self.assertEqual("PARSER_LOOKING_FOR_CRC", parser.temporarystate)
        parser.temporarystate = "PARSER_LOOKING_FOR_CRC"
        parser.telegram = "A8B"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual(parser.CRCLen, 4)
        self.assertEqual(parser.bufferCRC, "AA8B")
        self.assertEqual("PARSER_LOOKING_FOR_CR", parser.temporarystate)




    # case 6
    def test_ParserLookingForLFOnCR(self):
        parser = P1Parser()
        parser.temporarystate = "PARSER_LOOKING_FOR_CR"
        parser.telegram = "\r"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual("PARSER_LOOKING_FOR_LF", parser.temporarystate)

    # case 7
    def test_ParserLookingForLFOnCR(self):
        parser = P1Parser()
        parser.temporarystate = "PARSER_LOOKING_FOR_CR"
        parser.telegram = "\r\n"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertTrue(parser.CRC_is_OK)

    # case 8
    def test_ParserLookingForBlockValidation(self):
        # BlockwithCRC after "!"
        parser = P1Parser()
        parser.temporarystate = "PARSER_LOOKING_FOR_BEGIN"
        parser.telegram = "/KFM5KAIFA-METER\r\n\r\n1-0:1.8.0(000671.578*kWh)\r\n1-0:2.8.0(000842.472*kWh)\r\n1-0:1.7.0(00.333*kW)\r\n1-0:2.7.0(00.444*kW)\r\n!399E\r"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual("PARSER_LOOKING_FOR_LF", parser.temporarystate)

    #---------------------------------------------------------
        parser.telegram = "/KFM5KAIFA-METER\r\n\r\n1-0:1.8.0(000671.578*kWh)\r\n1-0:2.8.0(000842.472*kWh)\r\n1-0:1.7.0(00.333*kW)\r\n1-0:2.7.0(00.444*kW)\r\n!399E\r\n"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual(parser.CRCLen, 4)
        self.assertEqual(parser.bufferCRC, "399E")
        ReturnedValue= parser.frominttostringofhex(CRC16().calculate(parser.bufferBlock))
        self.assertEqual(ReturnedValue, "399E")
        self.assertTrue(parser.CRC_is_OK)


