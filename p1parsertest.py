import random
from p1parserclass import *
import unittest
from readfile import *
import io



class P1ParserTest(unittest.TestCase):


    def test_choice(self):
        """Test le fonctionnement de la fonction 'random.choice'."""
        liste = list(range(10))
        elt = random.choice(liste)
        # Vérifie que 'elt' est dans 'liste'
        #self.assertIn(elt, liste)

    def test_ParserLookingForLetter1OnSlach(self):
        parser= P1Parser()
        parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
        parser.telegram="/"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual(Parserstates.PARSER_LOOKING_FOR_LETTER1.name, parser.temporarystate)

    def test_ParserLookingForLetter2OnLetter1(self):
        parser= P1Parser()
        parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
        parser.telegram="/M"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual(Parserstates.PARSER_LOOKING_FOR_LETTER2.name, parser.temporarystate)

    def test_ParserLookingForLetter3OnLetter2(self):
        parser= P1Parser()
        parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
        parser.telegram="/MC"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual(Parserstates.PARSER_LOOKING_FOR_LETTER3.name, parser.temporarystate)


    def test_ParserLookingForNumberOnLetter3(self):
        parser= P1Parser()
        parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
        parser.telegram="/MMS"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual(Parserstates.PARSER_LOOKING_FOR_NUMBER.name, parser.temporarystate)

    def test_ParserLookingForCR1OnNumber(self):
        parser= P1Parser()
        parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
        parser.telegram="/MMS5"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual(Parserstates.PARSER_LOOKING_FOR_CR1.name, parser.temporarystate)

    def test_ParserLookingForLF1OnCR1(self):
        parser= P1Parser()
        parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
        parser.telegram="/MMS5IDIDID\r"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual(Parserstates.PARSER_LOOKING_FOR_LF1.name, parser.temporarystate)

    def test_ParserLookingForCR2OnLF1(self):
        parser= P1Parser()
        parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
        parser.telegram="/MMS5IDIDID\r\n"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual("PARSER_LOOKING_FOR_CR2", parser.temporarystate)

    def test_ParserLookingForLF2OnCR2(self):
        parser= P1Parser()
        parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
        parser.telegram="/MMS5IDIDID\r\n\r"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual(Parserstates.PARSER_LOOKING_FOR_LF2.name, parser.temporarystate)

    def test_ParserLookingForDATAOnLF2(self):
        parser= P1Parser()
        parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
        parser.telegram="/MMS5IDIDID\r\n\r\n"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual(Parserstates.PARSER_LOOKING_FOR_DATAGeneral.name, parser.temporarystate)
    #case 1
    def test_ParserLookingForBeginOnNOData(self):
        parser= P1Parser()
        parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
        parser.telegram="/MMS5IDIDID\r\n\r\n\0"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual(Parserstates.PARSER_LOOKING_FOR_BEGIN.name, parser.temporarystate)

    #case 2

    def test_ParserIncreaseDataIdxIfWedidntreachExclamationpoint(self):
        parser = P1Parser()
        parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
        parser.telegram = "/MMS5IDIDID\r\n\r\n1-0:0.8.0(00900)"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertGreater(parser.DataIdx, 0)
        self.assertEqual(Parserstates.PARSER_LOOKING_FOR_DATAGeneral.name, parser.temporarystate)

    # case 3
    def test_ParserRejectWhenFindExclamationandDataLenisZero(self):
        parser = P1Parser()
        parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_DATAGeneral.name
        parser.telegram = "!"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual(Parserstates.PARSER_LOOKING_FOR_BEGIN.name, parser.temporarystate)

    # case 4
    def test_ParserLookingForEndOfBlockOnDATA(self):
        parser= P1Parser()
        parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_DATAGeneral.name
        parser.telegram="1-0:0.8.0(00900)\r\n1-0:0.3.1(01000)\r\n!"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertGreater(parser.DataIdx, 0)
        self.assertEqual(Parserstates.PARSER_LOOKING_FOR_ENDOFBLOC.name, parser.temporarystate)
    #No CRC, CRLF at the endoftheblock
    def test_ParserLookingForCROnEndOfBlock(self):
        #BlockwithoutCRC "\r\n" after "!"
        parser= P1Parser()
        parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_ENDOFBLOC.name
        parser.telegram="\r"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual(Parserstates.PARSER_LOOKING_FOR_LF.name, parser.temporarystate)

    def test_ParserLookingForLastreturnOnCRLF(self):
        #BlockwithoutCRC "\r\n" after "!"
        parser= P1Parser()
        parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_ENDOFBLOC.name
        parser.telegram="\r\n"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertTrue(parser.CRC_is_OK)

    #We've CRC+CRLF at the endoftheblock

    #case 5
    def test_ParserLookingForCRCOnExclamation(self):
        #BlockwithCRC after "!"
        parser= P1Parser()
        parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_ENDOFBLOC.name
        parser.telegram="A"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual(parser.CRCLen,1)
        self.assertEqual(parser.bufferCRC, "A")
        self.assertEqual(Parserstates.PARSER_LOOKING_FOR_CRC.name, parser.temporarystate)
        parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_CRC.name
        parser.telegram = "A8B"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual(parser.CRCLen, 4)
        self.assertEqual(parser.bufferCRC, "AA8B")
        self.assertEqual(Parserstates.PARSER_LOOKING_FOR_CR.name, parser.temporarystate)




    # case 6
    def test_ParserLookingForLFOnCR(self):
        parser = P1Parser()
        parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_CR.name
        parser.telegram = "\r"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual(Parserstates.PARSER_LOOKING_FOR_LF.name, parser.temporarystate)

    # case 7
    def test_ParserLookingForLFOnCR(self):
        parser = P1Parser()
        parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_CR.name
        parser.telegram = "\r\n"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertTrue(parser.CRC_is_OK)

    # case 8
    def test_ParserLookingForBlockValidation(self):
        # BlockwithCRC after "!"
        parser = P1Parser()
        parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
        parser.telegram = "/KFM5KAIFA-METER\r\n\r\n1-0:1.8.0(000671.578*kWh)\r\n1-0:2.8.0(000842.472*kWh)\r\n1-0:1.7.0(00.333*kW)\r\n1-0:2.7.0(00.444*kW)\r\n!E52C\r"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual(Parserstates.PARSER_LOOKING_FOR_LF.name, parser.temporarystate)

    #---------------------------------------------------------

    def test_IfCRCvalueCalculatedSameAsTheOneInTelegram(self):
        parser = P1Parser()
        parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
        parser.telegram = "/KFM5KAIFA-METER\r\n\r\n1-0:1.8.0(000671.578*kWh)\r\n1-0:2.8.0(000842.472*kWh)\r\n1-0:1.7.0(00.333*kW)\r\n1-0:2.7.0(00.444*kW)\r\n!E52C\r\n"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual(parser.CRCLen, 4)
        #self.assertEqual(parser.bufferCRC, "E52C")
        ReturnedValue= parser.frominttostringofhex(CRC16().calculate(parser.bufferBlock))
        #self.assertEqual(ReturnedValue, "E52C")
        if (ReturnedValue == parser.bufferCRC):
            self.assertTrue(parser.CRC_is_OK)

    def test_IfBufferBlockIsNotEmpty(self):
        file = FileReader()
        file.TelegramfileReading("C:\\Users\Amel\Documents\TWINGZ\P1ParserPython\MeterTelegram.txt")
        parser = P1Parser()  # one object from p1parserclass
        localtelegram = file.telegram
        parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
        parser.P1Parser_Receive_char(localtelegram)
        self.assertNotEqual(parser.bufferBlock, "")


    def test_RejectIfTelegramIsNotValid(self):
        file = FileReader()
        file.TelegramfileReading("C:\\Users\Amel\Documents\TWINGZ\P1ParserPython\\NotValidTelegram.txt")
        parser = P1Parser()  # one object from p1parserclass
        localtelegram = file.telegram
        parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
        parser.P1Parser_Receive_char(localtelegram)
        self.assertNotEqual(parser.bufferBlock, "")
        self.assertNotEqual(Parserstates.PARSER_LOOKING_FOR_LF.name, parser.temporarystate)


    def test_RejectIfItsNotAValidTelegram(self):
        parser = P1Parser()
        parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
        parser.telegram = "/FM5KAIFA-METER\r\n\r\n1-0:1.8.0(000671.578*kWh)\r\n1-0:2.8.0(000842.472*kWh)\r\n1-0:1.7.0(00.333*kW)\r\n1-0:2.7.0(00.444*kW)\r\n!E52C\r\n"
        parser.P1Parser_Receive_char(parser.telegram)
        self.assertEqual(parser.temporarystate, Parserstates.PARSER_LOOKING_FOR_BEGIN.name)


    def test_ParserReadingFromMeterTelegramtxtAndCheckCRC(self):
        file = FileReader()
        file.TelegramfileReading("C:\\Users\Amel\Documents\TWINGZ\P1ParserPython\MeterTelegram.txt")
        parser = P1Parser()  # one object from p1parserclass
        localtelegram = file.telegram
        parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
        parser.P1Parser_Receive_char(localtelegram)
        ReturnedValue = parser.frominttostringofhex(CRC16().calculate(parser.bufferBlock))
        if (parser.bufferCRC != ""):
            if (len(ReturnedValue) == 3):
                ReturnedValue = "0" + ReturnedValue
            self.assertEqual(ReturnedValue, parser.bufferCRC)


    def test_ParserReadingFromExample1(self):
        file = FileReader()
        file.TelegramfileReading("C:\\Users\Amel\Documents\TWINGZ\P1ParserPython\Telegrams\example1.txt")
        if (file.telegram != ""):
            parser = P1Parser()  # one object from p1parserclass
            localtelegram = file.telegram
            parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
            parser.P1Parser_Receive_char(localtelegram)
            ReturnedValue = parser.frominttostringofhex(CRC16().calculate(parser.bufferBlock))
            if (parser.bufferCRC != ""):
                if (len(ReturnedValue) == 3):
                    ReturnedValue = "0" + ReturnedValue
                self.assertEqual(ReturnedValue, parser.bufferCRC)
                self.assertTrue(parser.CRC_is_OK)
                #print("test1", parser.bufferCRC)
        else:
            print("file is empty! ")

    def test_ParserReadingFromExample2(self):
        file = FileReader()
        file.TelegramfileReading("C:\\Users\Amel\Documents\TWINGZ\P1ParserPython\Telegrams\example2.txt")
        if (file.telegram != ""):
            parser = P1Parser()  # one object from p1parserclass
            localtelegram = file.telegram
            parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
            parser.P1Parser_Receive_char(localtelegram)
            ReturnedValue = parser.frominttostringofhex(CRC16().calculate(parser.bufferBlock))
            if (parser.bufferCRC != ""):
                if (len(ReturnedValue) == 3):
                    ReturnedValue = "0" + ReturnedValue
                self.assertEqual(ReturnedValue, parser.bufferCRC)
                self.assertTrue(parser.CRC_is_OK)
                #print("test2", parser.bufferCRC)
        else:
            print("file is empty! ")

    def test_ParserReadingFromExample3(self):
        file = FileReader()
        file.TelegramfileReading("C:\\Users\Amel\Documents\TWINGZ\P1ParserPython\Telegrams\example3.txt")
        if (file.telegram != ""):
            parser = P1Parser()  # one object from p1parserclass
            localtelegram = file.telegram
            parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
            parser.P1Parser_Receive_char(localtelegram)
            ReturnedValue = parser.frominttostringofhex(CRC16().calculate(parser.bufferBlock))
            if (parser.bufferCRC != ""):
                if (len(ReturnedValue) == 3):
                    ReturnedValue = "0" + ReturnedValue
                self.assertEqual(ReturnedValue, parser.bufferCRC)
                self.assertTrue(parser.CRC_is_OK)
                #print("test3", parser.bufferCRC)
        else:
            print("file is empty! ")

    def test_ParserReadingFromExample4(self):
        file = FileReader()
        file.TelegramfileReading("C:\\Users\Amel\Documents\TWINGZ\P1ParserPython\Telegrams\example4.txt")
        if (file.telegram != ""):
            parser = P1Parser()  # one object from p1parserclass
            localtelegram = file.telegram
            parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
            parser.P1Parser_Receive_char(localtelegram)
            ReturnedValue = parser.frominttostringofhex(CRC16().calculate(parser.bufferBlock))
            if (parser.bufferCRC != ""):
                if (len(ReturnedValue) == 3):
                    ReturnedValue = "0" + ReturnedValue
                self.assertEqual(ReturnedValue, parser.bufferCRC)
                self.assertTrue(parser.CRC_is_OK)
                #print("test4", parser.bufferCRC)
        else:
            print("file is empty! ")

    def test_ParserReadingFromExample5(self):
        file = FileReader()
        file.TelegramfileReading("C:\\Users\Amel\Documents\TWINGZ\P1ParserPython\Telegrams\example5.txt")
        if (file.telegram != ""):
            parser = P1Parser()  # one object from p1parserclass
            localtelegram = file.telegram
            parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
            parser.P1Parser_Receive_char(localtelegram)
            ReturnedValue = parser.frominttostringofhex(CRC16().calculate(parser.bufferBlock))
            if (parser.bufferCRC != ""):
                if (len(ReturnedValue) == 3):
                    ReturnedValue = "0" + ReturnedValue
                self.assertEqual(ReturnedValue, parser.bufferCRC)
                self.assertTrue(parser.CRC_is_OK)
                #print("test5", parser.bufferCRC)
        else:
            print("file is empty! ")

    def test_ParserReadingFromExample6(self):
        file = FileReader()
        file.TelegramfileReading("C:\\Users\Amel\Documents\TWINGZ\P1ParserPython\Telegrams\example6.txt")
        if (file.telegram != ""):
            parser = P1Parser()  # one object from p1parserclass
            localtelegram = file.telegram
            parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
            parser.P1Parser_Receive_char(localtelegram)
            ReturnedValue = parser.frominttostringofhex(CRC16().calculate(parser.bufferBlock))
            if (parser.bufferCRC != ""):
                if (len(ReturnedValue) == 3):
                    ReturnedValue = "0" + ReturnedValue
                self.assertEqual(ReturnedValue, parser.bufferCRC)
                self.assertTrue(parser.CRC_is_OK)
                #print("test6", parser.bufferCRC)
        else:
            print("file is empty! ")

    def test_ParserReadingFromExample7(self):
        file = FileReader()
        file.TelegramfileReading("C:\\Users\Amel\Documents\TWINGZ\P1ParserPython\Telegrams\example7.txt")
        if (file.telegram != ""):
            parser = P1Parser()  # one object from p1parserclass
            localtelegram = file.telegram
            parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
            parser.P1Parser_Receive_char(localtelegram)
            ReturnedValue = parser.frominttostringofhex(CRC16().calculate(parser.bufferBlock))
            if (parser.bufferCRC != ""):
                if (len(ReturnedValue) == 3):
                    ReturnedValue = "0" + ReturnedValue
                self.assertEqual(ReturnedValue, parser.bufferCRC)
                self.assertTrue(parser.CRC_is_OK)
                #print("test7", parser.bufferCRC)
        else:
            print("file is empty! ")

    def test_ParserReadingFromExample8(self):
        file = FileReader()
        file.TelegramfileReading("C:\\Users\Amel\Documents\TWINGZ\P1ParserPython\Telegrams\example8.txt")
        if (file.telegram != ""):
            parser = P1Parser()  # one object from p1parserclass
            localtelegram = file.telegram
            parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
            parser.P1Parser_Receive_char(localtelegram)
            ReturnedValue = parser.frominttostringofhex(CRC16().calculate(parser.bufferBlock))
            if (parser.bufferCRC != ""):
                if (len(ReturnedValue) == 3):
                    ReturnedValue = "0" + ReturnedValue
                self.assertEqual(ReturnedValue, parser.bufferCRC)
                self.assertTrue(parser.CRC_is_OK)
                #print("test8", parser.bufferCRC)
        else:
            print("file is empty! ")

    def test_ParserReadingFromExample9(self):
        file = FileReader()
        file.TelegramfileReading("C:\\Users\Amel\Documents\TWINGZ\P1ParserPython\Telegrams\example9.txt")
        if (file.telegram != ""):
            parser = P1Parser()  # one object from p1parserclass
            localtelegram = file.telegram
            parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
            parser.P1Parser_Receive_char(localtelegram)
            ReturnedValue = parser.frominttostringofhex(CRC16().calculate(parser.bufferBlock))
            if (parser.bufferCRC != ""):
                if (len(ReturnedValue) == 3):
                    ReturnedValue = "0" + ReturnedValue
                self.assertEqual(ReturnedValue, parser.bufferCRC)
                self.assertTrue(parser.CRC_is_OK)
                #print("test9", parser.bufferCRC)
        else:
            print("file is empty! ")

    def test_ParserReadingFromExample10(self):
        file = FileReader()
        file.TelegramfileReading("C:\\Users\Amel\Documents\TWINGZ\P1ParserPython\Telegrams\example10.txt")
        if (file.telegram != ""):
            parser = P1Parser()  # one object from p1parserclass
            localtelegram = file.telegram
            parser.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
            parser.P1Parser_Receive_char(localtelegram)
            ReturnedValue = parser.frominttostringofhex(CRC16().calculate(parser.bufferBlock))
            if (parser.bufferCRC != ""):
                if (len(ReturnedValue) == 3):
                    ReturnedValue = "0" + ReturnedValue
                self.assertEqual(ReturnedValue, parser.bufferCRC)
                self.assertTrue(parser.CRC_is_OK)
                #print("test10", parser.bufferCRC)
        else:
            print("file is empty! ")


