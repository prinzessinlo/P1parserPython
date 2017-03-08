# type in the cmd line :>> easy_install PyCRC to add the lib package to python doc
from PyCRC.CRC16 import CRC16 #for the CRC calculation and check
from enum import Enum
from objectencoder import * #for json.dumps function call Serialize obj to a JSON

#Prepare the object for energy format containing value & unit
class energyCPObjAttr(object): #Class naming use the CapWords convention
    def __init__(self, energy):
        self.value = str(energy)
        self.unit = "kWh"

#Prepare the object for power format containing value & unit
class powerCPObjAttr(object):
    def __init__(self, power):
        self.value = str(power)
        self.unit = "kW"

#Set the list of state as an enum
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
    def __init__(self):  # Constructor for p1parser class
        self.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
        self.ListofDataValues = [0, 0, 0, 0]
        self.type = 0
        self.value = 0
        self.DotSeen = False
        self.ParenthesisSeen = False
        self.ColonSeen = False
        self.StarSeen = False
        #added for unittest
        self.CIsDigit= False
        self.CRC_is_OK = False
        self.BlockIdx = 0
        self.DataIdx = 0
        self.CRCLen = 0
        self.bufferCRC = ""
        self.bufferBlock = ""
        self.bufferData= ""
        # -------

        self.EnergyConsumed = 0
        self.EnergyProduced = 0
        self.PowerConsumed = 0
        self.PowerProduced = 0

    def __getattr__(self, ListofDataValues):
        return self.ListofDataValues
    #Establish json format supposed to deliver
    def convert_to_json(self):
    #Function names should be lowercase, with words separated by underscores
    #as necessary to improve readability.
        self.EnergyConsumed = energyCPObjAttr(self.ListofDataValues[0])
        self.EnergyProduced = energyCPObjAttr(self.ListofDataValues[1])
        self.PowerConsumed = powerCPObjAttr(self.ListofDataValues[2])
        self.PowerProduced = powerCPObjAttr(self.ListofDataValues[3])
        print(json.dumps({"EnergyConsumed": self.EnergyConsumed, "EnergyProduced": self.EnergyProduced,
                    "PowerConsumed": self.PowerConsumed, "PowerProduced": self.PowerProduced}, cls=ObjectEncoder,
                   indent=2, sort_keys=True))

        #json.dumps({"EnergyConsumed": self.EnergyConsumed, "EnergyProduced": self.EnergyProduced,
        #              "PowerConsumed": self.PowerConsumed, "PowerProduced": self.PowerProduced}, cls=ObjectEncoder,
        #             indent=2, sort_keys=True)

    #
    def p1parser_scanner(self, c):
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
        elif (self.ParenthesisSeen == True) or (self.ColonSeen == True) or (self.DotSeen == True):
            if c.isdigit():
                self.CIsDigit = True
                b = int(float(c))
                self.value = 10 * self.value + b
            else:
                self.CIsDigit= False

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
    #return the value if it's valid
    def p1p_getvalue(self):
        if (self.type >= 100) and (self.type <= 999):
            return self.value
        else:
            return 0
        # =======================================
    #return the type if it's valid
    def p1p_gettype(self):
        if (self.type >= 100) and (self.type <= 999):
            return self.type
        else:
            return 0  # non valid type
            # ==========================================

    def returnmetervaluesintoalist(self, data):
        meterValue = 0
        meterType = 0
        global a, b, c, d
        for letter in data:
            if self.p1parser_scanner(letter):
                # print("Je suis là!")
                meterType = self.p1p_gettype()
                meterValue = self.p1p_getvalue()
                if meterType == 180:
                    self.ListofDataValues[0] = meterValue  # energyConsumed
                elif meterType == 280:
                    self.ListofDataValues[1] = meterValue  # energyProduced
                elif meterType == 170:
                    self.ListofDataValues[2] = meterValue  # powerConsumed
                elif meterType == 270:
                    self.ListofDataValues[3] = meterValue  # powerProduced

                    # ==========================================

    def p1parser_receive_telegram(self, telegramBeforeValidation):
        for letter in telegramBeforeValidation:
            self.p1parser_receive_char(letter)
        else:  # else of for loop
            # print("Im out of for")
            self.returnmetervaluesintoalist(self.bufferData)
            # print("cEnergy: ", self.ListofDataValues[0])
            # print("pEnergy: ", self.ListofDataValues[1])
            # print("cPower: ", self.ListofDataValues[2])
            # print("pPower: ", self.ListofDataValues[3])

    def p1parser_receive_char(self, letter):
        IDidx = 0
        CRC = 4
        CRC_is_OK = False
        newChar = letter
        if self.temporarystate == Parserstates.PARSER_LOOKING_FOR_BEGIN.name:
            if (newChar == '/'):
                self.BlockIdx = 0
                self.bufferBlock = self.bufferBlock + newChar
                self.BlockIdx = self.BlockIdx + 1  # we store value into buffer block for CRC verification
                self.temporarystate = Parserstates.PARSER_LOOKING_FOR_LETTER1.name

            else:
                self.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name

        elif Parserstates.PARSER_LOOKING_FOR_LETTER1.name == self.temporarystate:
            if newChar.isalpha():
                self.temporarystate = Parserstates.PARSER_LOOKING_FOR_LETTER2.name

                self.bufferBlock = self.bufferBlock + newChar
                self.BlockIdx = self.BlockIdx + 1
            else:
                self.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
        elif self.temporarystate == Parserstates.PARSER_LOOKING_FOR_LETTER2.name:
            if newChar.isalpha():
                self.temporarystate = Parserstates.PARSER_LOOKING_FOR_LETTER3.name

                self.bufferBlock = self.bufferBlock + newChar
                self.BlockIdx = self.BlockIdx + 1
            else:
                self.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
        elif self.temporarystate == Parserstates.PARSER_LOOKING_FOR_LETTER3.name:
            if newChar.isalpha():
                self.temporarystate = Parserstates.PARSER_LOOKING_FOR_NUMBER.name

                self.bufferBlock = self.bufferBlock + newChar
                self.BlockIdx = self.BlockIdx + 1
            else:
                self.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
        elif self.temporarystate == Parserstates.PARSER_LOOKING_FOR_NUMBER.name:
            if newChar.isdigit():
                self.temporarystate = Parserstates.PARSER_LOOKING_FOR_CR1.name

                self.bufferBlock = self.bufferBlock + newChar
                self.BlockIdx = self.BlockIdx + 1
            else:
                self.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name

        elif self.temporarystate == Parserstates.PARSER_LOOKING_FOR_CR1.name:
            if newChar == "\r":  # if we receive \r
                self.bufferBlock = self.bufferBlock + newChar
                self.BlockIdx = self.BlockIdx + 1
                self.temporarystate = Parserstates.PARSER_LOOKING_FOR_LF1.name

            elif IDidx <= 1024:  # and (P1P_IsPrintableChar(newChar)))
                # We don't know the exact length of ID but we know Data bloc can be up to 1024characters
                self.bufferBlock = self.bufferBlock + newChar
                self.BlockIdx = self.BlockIdx + 1
                IDidx = IDidx + 1
            else:
                self.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name

        elif self.temporarystate == Parserstates.PARSER_LOOKING_FOR_LF1.name:
            if newChar == "\n":
                self.bufferBlock = self.bufferBlock + newChar
                self.BlockIdx = self.BlockIdx + 1
                self.temporarystate = Parserstates.PARSER_LOOKING_FOR_CR2.name

            else:
                self.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name

        elif self.temporarystate == Parserstates.PARSER_LOOKING_FOR_CR2.name:
            if newChar == "\r":  # if we receive \r
                self.bufferBlock = self.bufferBlock + newChar
                self.BlockIdx = self.BlockIdx + 1
                self.temporarystate = Parserstates.PARSER_LOOKING_FOR_LF2.name
            else:
                self.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
        elif self.temporarystate == Parserstates.PARSER_LOOKING_FOR_LF2.name:
            if (newChar == "\n"):
                self.bufferBlock = self.bufferBlock + newChar
                self.BlockIdx = self.BlockIdx + 1
                self.temporarystate = Parserstates.PARSER_LOOKING_FOR_DATAGeneral.name

            else:
                self.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
        elif self.temporarystate == Parserstates.PARSER_LOOKING_FOR_DATAGeneral.name:
            # case 1
            if newChar == "\0":
                self.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
            # case 2
            elif newChar != "!":  # 0x21="!"
                # fixme if data is more than the length of the buffer#
                self.bufferBlock = self.bufferBlock + newChar
                self.BlockIdx = self.BlockIdx + 1
                self.bufferData = self.bufferData + newChar
                self.DataIdx = self.DataIdx + 1
            # case 3
            elif ((newChar == "!") and (self.DataIdx == 0)):
                # if we receive ! & no data we should again to begin
                self.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
            # case 4
            elif (newChar == "!" and self.DataIdx > 0):
                self.temporarystate = Parserstates.PARSER_LOOKING_FOR_ENDOFBLOC.name

                self.bufferBlock = self.bufferBlock + newChar
                self.BlockIdx = self.BlockIdx + 1
            else:
                self.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name

        elif self.temporarystate == Parserstates.PARSER_LOOKING_FOR_ENDOFBLOC.name:
            #case 5
            if newChar.isalnum():
                self.CRCLen = 1
                self.bufferCRC = self.bufferCRC + newChar
                self.BlockIdx = self.BlockIdx + 1
                self.temporarystate = Parserstates.PARSER_LOOKING_FOR_CRC.name

            elif newChar == "\r":
                self.temporarystate = Parserstates.PARSER_LOOKING_FOR_LF.name

            else:
                self.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name

        elif self.temporarystate == Parserstates.PARSER_LOOKING_FOR_CRC.name:
            if newChar.isalnum():
                if self.CRCLen <= 4:
                    self.bufferCRC = self.bufferCRC + newChar
                    self.CRCLen = self.CRCLen + 1
                if self.CRCLen == CRC:
                    self.temporarystate = Parserstates.PARSER_LOOKING_FOR_CR.name

            else:
                self.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
        #case 6
        elif self.temporarystate == Parserstates.PARSER_LOOKING_FOR_CR.name:
            if newChar == "\r":  # if we receive \r
                self.temporarystate = Parserstates.PARSER_LOOKING_FOR_LF.name

            else:
                self.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name
        # case 7
        elif self.temporarystate == Parserstates.PARSER_LOOKING_FOR_LF.name:
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
                self.temporarystate = Parserstates.PARSER_LOOKING_FOR_BEGIN.name

    def frominttostringofhex(self, ReturnCRCValue):
        b = str(hex(ReturnCRCValue))
        #Split the returned value from CRC16 calculation method.
        #Remove 0x from the CRC
        #To compare the calculated right value and the value in the telegram
        CRCUppercase = (b.split("0x"))[1].upper()
        return CRCUppercase
