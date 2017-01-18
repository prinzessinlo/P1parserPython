import json
from objectencoder import  *
class energyCPObjAttr(object):
    def __init__(self, energy):
        self.value = str(energy)
        self.unit = "kWh"

class powerCPObjAttr(object):
    def __init__(self, power):
        self.value = str(power)
        self.unit = "kWh"


class P1Parser(object):
    Parserstates = {"PARSER_LOOKING_FOR_BEGIN", "PARSER_LOOKING_FOR_LETTER1", "PARSER_LOOKING_FOR_LETTER2",
                    "PARSER_LOOKING_FOR_LETTER3", "PARSER_LOOKING_FOR_NUMBER", "PARSER_LOOKING_FOR_CR1", "PARSER_LOOKING_FOR_LF1",
                    "PARSER_LOOKING_FOR_CR2", "PARSER_LOOKING_FOR_LF2", "PARSER_LOOKING_FOR_DATAGeneral", "PARSER_LOOKING_FOR_ENDOFBLOC",
                    "PARSER_LOOKING_FOR_CRC", "PARSER_LOOKING_FOR_CR", "PARSER_LOOKING_FOR_LF"}

    def __init__(self):  # Notre méthode constructeur
        self.ListofDataValues = [0, 0, 0, 0]
        self.type = 0
        self.value = 0
        self.DotSeen = False
        self.ParenthesisSeen = False
        self.ColonSeen = False
        self.StarSeen = False

        #-------

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
        print(json.dumps({"EnergyConsumed":self.EnergyConsumed, "EnergyProduced":self.EnergyProduced, "PowerConsumed":self.PowerConsumed, "PowerProduced":self.PowerProduced }, cls=ObjectEncoder, indent=2, sort_keys=True))

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
#=======================================
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
#==========================================
    def extractvalues(self, data):
        meterValue = 0
        meterType = 0
        global a, b, c, d
        for letter in data:
            if self.p1parserscanner(letter):
                #print("Je suis là!")
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

#==========================================

    def P1Parser_Receive_char(self, telegramBeforeValidation):
        temporarystate = "PARSER_LOOKING_FOR_BEGIN"
        newChar = '/'
        bufferBlock = ""
        bufferCRC = ""
        bufferData = ""
        IDidx = 0
        DataIdx = 0
        CRCLen = 0
        CRC = 4
        CRC_is_OK = False
        for letter in telegramBeforeValidation:
            newChar=letter
            if temporarystate=="PARSER_LOOKING_FOR_BEGIN":
                if (newChar == '/'):
                    BlockIdx = 0
                    bufferBlock= bufferBlock+ newChar
                    BlockIdx = BlockIdx + 1 #we store value into buffer block for CRC verification
                    temporarystate = "PARSER_LOOKING_FOR_LETTER1"

                else:
                    temporarystate = "PARSER_LOOKING_FOR_BEGIN"

            elif "PARSER_LOOKING_FOR_LETTER1" == temporarystate:
                if newChar.isalpha():
                    temporarystate = "PARSER_LOOKING_FOR_LETTER2"

                    bufferBlock = bufferBlock + newChar
                    BlockIdx = BlockIdx + 1
                else:
                    temporarystate= "PARSER_LOOKING_FOR_BEGIN"
            elif temporarystate == "PARSER_LOOKING_FOR_LETTER2":
                if newChar.isalpha():
                    temporarystate = "PARSER_LOOKING_FOR_LETTER3"

                    bufferBlock = bufferBlock + newChar
                    BlockIdx = BlockIdx + 1
                else:
                    temporarystate= "PARSER_LOOKING_FOR_BEGIN"
            elif temporarystate == "PARSER_LOOKING_FOR_LETTER3":
                if newChar.isalpha():
                    temporarystate = "PARSER_LOOKING_FOR_NUMBER"

                    bufferBlock = bufferBlock + newChar
                    BlockIdx = BlockIdx + 1
                else:
                    temporarystate = "PARSER_LOOKING_FOR_BEGIN"
            elif temporarystate == "PARSER_LOOKING_FOR_NUMBER":
                if newChar.isdigit():
                    temporarystate = "PARSER_LOOKING_FOR_CR1"

                    bufferBlock = bufferBlock + newChar
                    BlockIdx = BlockIdx + 1
                else:
                    temporarystate = "PARSER_LOOKING_FOR_BEGIN"

            elif temporarystate=="PARSER_LOOKING_FOR_CR1":
                if newChar == "\r": #if we receive \r
                    bufferBlock = bufferBlock + newChar
                    BlockIdx = BlockIdx + 1
                    temporarystate = "PARSER_LOOKING_FOR_LF1"

                elif (IDidx <= 1024):  #and (P1P_IsPrintableChar(newChar)))
                #We don't know the exact length of ID but we know Data bloc can be up to 1024characters
                    bufferBlock = bufferBlock + newChar
                    BlockIdx =BlockIdx +1
                    IDidx=IDidx+1
                else:
                    temporarystate= "PARSER_LOOKING_FOR_BEGIN"

            elif temporarystate == "PARSER_LOOKING_FOR_LF1":
                if (newChar == "\n"):
                    bufferBlock = bufferBlock + newChar
                    BlockIdx =BlockIdx +1
                    temporarystate = "PARSER_LOOKING_FOR_CR2"

                else:
                    temporarystate = "PARSER_LOOKING_FOR_BEGIN"

            elif temporarystate == "PARSER_LOOKING_FOR_CR2":
                if newChar == "\r": #if we receive \r
                    bufferBlock = bufferBlock + newChar
                    BlockIdx = BlockIdx + 1
                    temporarystate = "PARSER_LOOKING_FOR_LF2"
                else:
                    temporarystate= "PARSER_LOOKING_FOR_BEGIN"
            elif temporarystate == "PARSER_LOOKING_FOR_LF2":
                if (newChar == "\n"):
                    bufferBlock = bufferBlock + newChar
                    BlockIdx = BlockIdx + 1
                    temporarystate = "PARSER_LOOKING_FOR_DATAGeneral"

                else:
                    temporarystate = "PARSER_LOOKING_FOR_BEGIN"
            elif temporarystate == "PARSER_LOOKING_FOR_DATAGeneral":
                if newChar == "\0":
                    temporarystate = "PARSER_LOOKING_FOR_BEGIN"
                elif newChar != "!":   #0x21="!"
                    #fixme if data is more than the length of the buffer
                    bufferBlock = bufferBlock + newChar
                    BlockIdx = BlockIdx + 1
                    bufferData = bufferData+newChar
                    DataIdx = DataIdx+1
                elif ((newChar == "!") and (DataIdx == 0)):
                # if we receive ! & no data we should again to begin
                    temporarystate = "PARSER_LOOKING_FOR_BEGIN"
                elif (newChar == "!" and DataIdx > 0):
                    temporarystate = "PARSER_LOOKING_FOR_ENDOFBLOC"

                    bufferBlock = bufferBlock + newChar
                    BlockIdx = BlockIdx + 1
                else:
                    temporarystate = "PARSER_LOOKING_FOR_BEGIN"

            elif temporarystate == "PARSER_LOOKING_FOR_ENDOFBLOC":
                if newChar.isdigit():
                    CRCLen = 1
                    bufferBlock = bufferBlock + newChar
                    BlockIdx = BlockIdx + 1
                    temporarystate = "PARSER_LOOKING_FOR_CRC"

                elif newChar == "\n":
                    temporarystate = "PARSER_LOOKING_FOR_LF"

                else:
                    temporarystate = "PARSER_LOOKING_FOR_BEGIN"

            elif temporarystate == "PARSER_LOOKING_FOR_CRC":
                if newChar.isdigit():
                    if CRCLen <= 4:
                        bufferCRC = bufferCRC + newChar
                        CRCLen= CRCLen + 1
                    if CRCLen == CRC:
                        temporarystate = "PARSER_LOOKING_FOR_CR"

                else:
                    temporarystate = "PARSER_LOOKING_FOR_BEGIN"

            elif temporarystate == "PARSER_LOOKING_FOR_CR":
                if newChar == "\r": #if we receive \r
                    temporarystate = "PARSER_LOOKING_FOR_LF"

                else:
                    temporarystate= "PARSER_LOOKING_FOR_BEGIN"
            elif temporarystate == "PARSER_LOOKING_FOR_LF":
                if newChar == 0x0A:
                    if CRCLen == 0:
                        CRC_is_OK = True
                elif CRCLen == 4:
                    if bufferCRC=="0505":
                        CRC_is_OK = True
                        print("CRC is OK! Sleep well!" )
                if (CRC_is_OK==False):
                    temporarystate = "PARSER_LOOKING_FOR_BEGIN"
        else:
            #print("Im out of for")
            self.extractvalues(bufferData)

            #print("cEnergy: ", self.ListofDataValues[0])
            #print("pEnergy: ", self.ListofDataValues[1])
            #print("cPower: ", self.ListofDataValues[2])
            #print("pPower: ", self.ListofDataValues[3])

