# type in the cmd line :>> easy_install PyCRC to add the lib package to python doc
from PyCRC.CRC16 import CRC16
from enum import Enum
from objectencoder import *


class energyCPObjAttr(object):
    def __init__(self, energy):
        self.value = str(energy)
        self.unit = "kWh"


class powerCPObjAttr(object):
    def __init__(self, power):
        self.value = str(power)
        self.unit = "kWh"

class Parserstates(Enum):
    PARSER_LOOKING_FOR_BEGIN = 1
    PARSER_LOOKING_FOR_LETTER1 = 2
    PARSER_LOOKING_FOR_LETTER2 = 3
    PARSER_LOOKING_FOR_LETTER3 = 4
    PARSER_LOOKING_FOR_NUMBER = 5
    PARSER_LOOKING_FOR_CR1 = 6
    PARSER_LOOKING_FOR_LF1 = 7
    PARSER_LOOKING_FOR_CR2 = 8
    PARSER_LOOKING_FOR_LF2 = 9
    PARSER_LOOKING_FOR_DATAGeneral = 10
    PARSER_LOOKING_FOR_ENDOFBLOC = 11
    PARSER_LOOKING_FOR_CRC = 12
    PARSER_LOOKING_FOR_CR = 13
    PARSER_LOOKING_FOR_LF = 14




class P1Parser(object):
    def __init__(self):  # Notre méthode constructeur
        self.Parserstates = {"PARSER_LOOKING_FOR_BEGIN", "PARSER_LOOKING_FOR_LETTER1", "PARSER_LOOKING_FOR_LETTER2",
                             "PARSER_LOOKING_FOR_LETTER3", "PARSER_LOOKING_FOR_NUMBER", "PARSER_LOOKING_FOR_CR1",
                             "PARSER_LOOKING_FOR_LF1",
                             "PARSER_LOOKING_FOR_CR2", "PARSER_LOOKING_FOR_LF2", "PARSER_LOOKING_FOR_DATAGeneral",
                             "PARSER_LOOKING_FOR_ENDOFBLOC",
                             "PARSER_LOOKING_FOR_CRC", "PARSER_LOOKING_FOR_CR", "PARSER_LOOKING_FOR_LF"}

        self.temporarystate = "PARSER_LOOKING_FOR_BEGIN"
        self.ListofDataValues = [0, 0, 0, 0]
        self.type = 0
        self.value = 0
        self.DotSeen = False
        self.ParenthesisSeen = False
        self.ColonSeen = False
        self.StarSeen = False
        #added for unittest
        self.CRC_is_OK = False
        self.BlockIdx = 0
        self.DataIdx = 0
        self.CRCLen = 0
        self.bufferCRC = ""
        self.bufferBlock = ""

        # -------

        self.EnergyConsumed = 0
        self.EnergyProduced = 0
        self.PowerConsumed = 0
        self.PowerProduced = 0

    def __getattr__(self, ListofDataValues):
        return self.ListofDataValues

    def converttojson(self):
        self.EnergyConsumed = energyCPObjAttr(self.ListofDataValues[0])
        self.EnergyProduced = energyCPObjAttr(self.ListofDataValues[1])
        self.PowerConsumed = powerCPObjAttr(self.ListofDataValues[2])
        self.PowerProduced = powerCPObjAttr(self.ListofDataValues[3])
        json.dumps({"EnergyConsumed": self.EnergyConsumed, "EnergyProduced": self.EnergyProduced,
                    "PowerConsumed": self.PowerConsumed, "PowerProduced": self.PowerProduced}, cls=ObjectEncoder,
                   indent=2, sort_keys=True)

    def p1parserscanner(self, c):
        if c == ':':
            self.type = 0
            self.value = 0
            self.ColonSeen = True
            return 0
        elif c == '(':
            if (self.type == 0):
                self.type = self.value
            self.value = 0
            self.DotSeen = False
            self.ColonSeen = False
            self.ParenthesisSeen = True
            return 0
        elif c == '.':
            self.DotSeen = True
            return 0
        elif c == ')':
            if (self.DotSeen == True) and (self.type != 0):
                return True
            return 0
        elif c == '*':
            self.StarSeen = True
        elif c.isdigit() and ((self.ParenthesisSeen == True) or (self.ColonSeen == True) or (self.DotSeen == True)):
            b = int(float(c))
            self.value = 10 * self.value + b
        elif c.isalpha and not self.StarSeen:
            self.value = 0
            self.ParenthesisSeen = False
            self.WrongValueIsHere = True
            return 0
        elif (self.StarSeen) and (c == 'k' or c == 'W' or c == 'h'):
            return 0
        else:
            self.DotSeen = False
            self.ParenthesisSeen = False
            self.ColonSeen = False
            self.StarSeen = False
        return 0

    # =======================================
    def P1P_GetValue(self):
        if (self.type >= 100) and (self.type <= 999):
            return self.value
        else:
            return 0
        # =======================================

    def P1P_GetType(self):
        if (self.type >= 100) and (self.type <= 999):
            return self.type
        else:
            return 0  # non valid type
            # ==========================================

    def extractvalues(self, data):
        meterValue = 0
        meterType = 0
        global a, b, c, d
        for letter in data:
            if self.p1parserscanner(letter):
                # print("Je suis là!")
                meterType = self.P1P_GetType()
                meterValue = self.P1P_GetValue()
                if meterType == 180:
                    self.ListofDataValues[0] = meterValue  # energyConsumed
                elif meterType == 280:
                    self.ListofDataValues[1] = meterValue  # energyProduced
                elif meterType == 170:
                    self.ListofDataValues[2] = meterValue  # powerConsumed
                elif meterType == 270:
                    self.ListofDataValues[3] = meterValue  # powerProduced

                    # ==========================================

    def P1Parser_Receive_char(self, telegramBeforeValidation):

        newChar = '/'

        bufferData = ""
        IDidx = 0

        CRC = 4
        CRC_is_OK = False
        for letter in telegramBeforeValidation:
            newChar = letter
            if self.temporarystate == "PARSER_LOOKING_FOR_BEGIN":
                if (newChar == '/'):
                    self.BlockIdx = 0
                    self.bufferBlock = self.bufferBlock + newChar
                    self.BlockIdx = self.BlockIdx + 1  # we store value into buffer block for CRC verification
                    self.temporarystate = "PARSER_LOOKING_FOR_LETTER1"

                else:
                    self.temporarystate = "PARSER_LOOKING_FOR_BEGIN"

            elif "PARSER_LOOKING_FOR_LETTER1" == self.temporarystate:
                if newChar.isalpha():
                    self.temporarystate = "PARSER_LOOKING_FOR_LETTER2"

                    self.bufferBlock = self.bufferBlock + newChar
                    self.BlockIdx = self.BlockIdx + 1
                else:
                    self.temporarystate = "PARSER_LOOKING_FOR_BEGIN"
            elif self.temporarystate == "PARSER_LOOKING_FOR_LETTER2":
                if newChar.isalpha():
                    self.temporarystate = "PARSER_LOOKING_FOR_LETTER3"

                    self.bufferBlock = self.bufferBlock + newChar
                    self.BlockIdx = self.BlockIdx + 1
                else:
                    self.temporarystate = "PARSER_LOOKING_FOR_BEGIN"
            elif self.temporarystate == "PARSER_LOOKING_FOR_LETTER3":
                if newChar.isalpha():
                    self.temporarystate = "PARSER_LOOKING_FOR_NUMBER"

                    self.bufferBlock = self.bufferBlock + newChar
                    self.BlockIdx = self.BlockIdx + 1
                else:
                    self.temporarystate = "PARSER_LOOKING_FOR_BEGIN"
            elif self.temporarystate == "PARSER_LOOKING_FOR_NUMBER":
                if newChar.isdigit():
                    self.temporarystate = "PARSER_LOOKING_FOR_CR1"

                    self.bufferBlock = self.bufferBlock + newChar
                    self.BlockIdx = self.BlockIdx + 1
                else:
                    self.temporarystate = "PARSER_LOOKING_FOR_BEGIN"

            elif self.temporarystate == "PARSER_LOOKING_FOR_CR1":
                if newChar == "\r":  # if we receive \r
                    self.bufferBlock = self.bufferBlock + newChar
                    self.BlockIdx = self.BlockIdx + 1
                    self.temporarystate = "PARSER_LOOKING_FOR_LF1"

                elif (IDidx <= 1024):  # and (P1P_IsPrintableChar(newChar)))
                    # We don't know the exact length of ID but we know Data bloc can be up to 1024characters
                    self.bufferBlock = self.bufferBlock + newChar
                    self.BlockIdx = self.BlockIdx + 1
                    IDidx = IDidx + 1
                else:
                    self.temporarystate = "PARSER_LOOKING_FOR_BEGIN"

            elif self.temporarystate == "PARSER_LOOKING_FOR_LF1":
                if (newChar == "\n"):
                    self.bufferBlock = self.bufferBlock + newChar
                    self.BlockIdx = self.BlockIdx + 1
                    self.temporarystate = "PARSER_LOOKING_FOR_CR2"

                else:
                    self.temporarystate = "PARSER_LOOKING_FOR_BEGIN"

            elif self.temporarystate == "PARSER_LOOKING_FOR_CR2":
                if newChar == "\r":  # if we receive \r
                    self.bufferBlock = self.bufferBlock + newChar
                    self.BlockIdx = self.BlockIdx + 1
                    self.temporarystate = "PARSER_LOOKING_FOR_LF2"
                else:
                    self.temporarystate = "PARSER_LOOKING_FOR_BEGIN"
            elif self.temporarystate == "PARSER_LOOKING_FOR_LF2":
                if (newChar == "\n"):
                    self.bufferBlock = self.bufferBlock + newChar
                    self.BlockIdx = self.BlockIdx + 1
                    self.temporarystate = "PARSER_LOOKING_FOR_DATAGeneral"

                else:
                    self.temporarystate = "PARSER_LOOKING_FOR_BEGIN"
            elif self.temporarystate == "PARSER_LOOKING_FOR_DATAGeneral":
                # case 1
                if newChar == "\0":
                    self.temporarystate = "PARSER_LOOKING_FOR_BEGIN"
                # case 2
                elif newChar != "!":  # 0x21="!"
                    # fixme if data is more than the length of the buffer#
                    self.bufferBlock = self.bufferBlock + newChar
                    self.BlockIdx = self.BlockIdx + 1
                    bufferData = bufferData + newChar
                    self.DataIdx = self.DataIdx + 1
                # case 3
                elif ((newChar == "!") and (self.DataIdx == 0)):
                    # if we receive ! & no data we should again to begin
                    self.temporarystate = "PARSER_LOOKING_FOR_BEGIN"
                # case 4
                elif (newChar == "!" and self.DataIdx > 0):
                    self.temporarystate = "PARSER_LOOKING_FOR_ENDOFBLOC"

                    self.bufferBlock = self.bufferBlock + newChar
                    self.BlockIdx = self.BlockIdx + 1
                else:
                    self.temporarystate = "PARSER_LOOKING_FOR_BEGIN"

            elif self.temporarystate == "PARSER_LOOKING_FOR_ENDOFBLOC":
                #case 5
                if newChar.isalnum():
                    self.CRCLen = 1
                    self.bufferCRC = self.bufferCRC + newChar
                    self.BlockIdx = self.BlockIdx + 1
                    self.temporarystate = "PARSER_LOOKING_FOR_CRC"

                elif newChar == "\r":
                    self.temporarystate = "PARSER_LOOKING_FOR_LF"

                else:
                    self.temporarystate = "PARSER_LOOKING_FOR_BEGIN"

            elif self.temporarystate == "PARSER_LOOKING_FOR_CRC":
                if newChar.isalnum():
                    if self.CRCLen <= 4:
                        self.bufferCRC = self.bufferCRC + newChar
                        self.CRCLen = self.CRCLen + 1
                    if self.CRCLen == CRC:
                        self.temporarystate = "PARSER_LOOKING_FOR_CR"

                else:
                    self.temporarystate = "PARSER_LOOKING_FOR_BEGIN"
            #case 6
            elif self.temporarystate == "PARSER_LOOKING_FOR_CR":
                if newChar == "\r":  # if we receive \r
                    self.temporarystate = "PARSER_LOOKING_FOR_LF"

                else:
                    self.temporarystate = "PARSER_LOOKING_FOR_BEGIN"
            # case 7
            elif self.temporarystate == "PARSER_LOOKING_FOR_LF":
                if newChar == "\n":
                    if self.CRCLen == 0:
                        self.CRC_is_OK = True
                    elif self.CRCLen == 4:
                    # case 8
                        #self.bufferBlock= self.bufferBlock + "\r\n"
                        ReturnCRCValue = self.frominttostringofhex(CRC16().calculate(self.bufferBlock))
                        if (len(ReturnCRCValue) == 3):
                            ReturnCRCValue = "0" + ReturnCRCValue
                        if (ReturnCRCValue == self.bufferCRC):
                            self.CRC_is_OK = True

                if (self.CRC_is_OK == False):
                    self.temporarystate = "PARSER_LOOKING_FOR_BEGIN"
        else: #else of for loop
            # print("Im out of for")
            self.extractvalues(bufferData)

            # print("cEnergy: ", self.ListofDataValues[0])
            # print("pEnergy: ", self.ListofDataValues[1])
            # print("cPower: ", self.ListofDataValues[2])
            # print("pPower: ", self.ListofDataValues[3])

    def frominttostringofhex(self, ReturnCRCValue):
        b = str(hex(ReturnCRCValue))
        # splitted = b.split("0x")
        CRCUppercase = (b.split("0x"))[1].upper()
        return CRCUppercase
