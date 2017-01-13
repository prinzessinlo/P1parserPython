# from ExtractValues import *

from P1scanner import *
#TOFIX function call in P1Parser.py

DataFromTelegram = ""  # buffer which contain the telegram as string
buffersize = 0  # size of telegram length

DataFromTelegram = "/XXX5AMEL\n\n1-0:1.8.0(000688.01*kWh)\n1-0:2.8.0(000131.72*kWh)\n1-0:1.7.0(000220.08*kWh)\n1-0:2.7.0(000999.08*kWh)\n!ABCD\n"
buffersize = len(DataFromTelegram)

DataFromTelegram1 = "/XXX5AMEL\n\n1-0:1.8.0(000333.01*kWh)\n1-0:2.8.0(000111.72*kWh)\n1-0:1.7.0(000229.88*kWh)\n1-0:2.7.0(000235.19*kWh)\n!ABCD\n"
buffersize = len(DataFromTelegram1)
ListofDataValues = [0, 0, 0, 0]
type = 0
value = 0
DotSeen= False
ParenthesisSeen= False
ColonSeen= False
StarSeen= False

def testfunctioncall():
    global test
    print("test function call! ")
    test = 5005
    print(test)

def p1parserreceivedtelegram(c):
    return 0
def p1parserscanner(c):
    global type
    global value
    global DotSeen
    global ParenthesisSeen
    global ColonSeen
    global StarSeen
    if c == ':':
        type = 0
        value = 0
        ColonSeen = True
        return 0
    elif c == '(':
        if (type == 0):
            type = value
        value = 0
        DotSeen = False
        ColonSeen = False
        ParenthesisSeen = True
        return 0
    elif c == '.':
        DotSeen = True
        return 0
    elif c == ')':
        if (DotSeen == True) and (type != 0):
            return True
        return 0
    elif c == '*':
        StarSeen = True
    elif c.isdigit() and ((ParenthesisSeen == True) or (ColonSeen == True) or (DotSeen == True)):
        b = int(float(c))
        value =10*value+b
        #print(value)
    elif c.isalpha and not(StarSeen):
        value = 0
        ParenthesisSeen = False
        WrongValueIsHere = True
        return 0
    elif (StarSeen) and (c == 'k' or c == 'W' or c == 'h'):
        return 0
    else:
        p1pDotSeen = False
        p1pParenthesisSeen = False
        p1pColonSeen = False
        p1pStarSeen = False
    return 0


def P1P_GetValue():
    if (type >= 100) and (type <= 999):
        return value
    else:
        return 0


def P1P_GetType():
    if (type >= 100) and (type <= 999):
        return type
    else:
        return 0  # non valid type




def extractvalues(data):
    meterValue = 0
    meterType = 0
    global ListofDataValues
    global a, b, c, d
    for letter in data:
        if (p1parserscanner(letter)):
            #print("Je suis là!")
            meterType = P1P_GetType()
            meterValue = P1P_GetValue()
            if meterType == 180:
                ListofDataValues[0] = meterValue  # energyConsumed
            elif meterType == 280:
                ListofDataValues[1] = meterValue  # energyProduced
            elif meterType == 170:
                ListofDataValues[2] = meterValue  # powerConsumed
            elif meterType == 270:
                ListofDataValues[3] = meterValue  # powerProduced
def f():
    global s
    print(s)
    s = "tu dois être global"
    print(s)


#-----------------------MAIN------------------------#




#extractvalues(DataFromTelegram)
#print("energyConsumed: ", ListofDataValues[0])
#print("energyProduced: ", ListofDataValues[1])
#print("powerConsumed: ", ListofDataValues[2])
#print("powerProduced: ", ListofDataValues[3])
Parserstates = {"PARSER_LOOKING_FOR_BEGIN", "PARSER_LOOKING_FOR_LETTER1", "PARSER_LOOKING_FOR_LETTER2",
                "PARSER_LOOKING_FOR_LETTER3", "PARSER_LOOKING_FOR_NUMBER", "PARSER_LOOKING_FOR_CR1", "PARSER_LOOKING_FOR_LF1",
                "PARSER_LOOKING_FOR_CR2", "PARSER_LOOKING_FOR_LF2", "PARSER_LOOKING_FOR_DATAGeneral", "PARSER_LOOKING_FOR_ENDOFBLOC",
                "PARSER_LOOKING_FOR_CRC", "PARSER_LOOKING_FOR_CR", "PARSER_LOOKING_FOR_LF"}


DataFromTelegram = "/XXX5AMEL\r\n\r\n1-0:1.8.0(000688.01*kWh)\n1-0:2.8.0(000131.72*kWh)\n1-0:1.7.0(000220.08*kWh)\n1-0:2.7.0(000999.08*kWh)\n!0505\r\n"
splitted=DataFromTelegram.split()
#print(splitted)

#print(splitted[5])
def P1Parser_Receive_char(DataFromTelegram):
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
    for letter in DataFromTelegram:
        newChar=letter
        if temporarystate=="PARSER_LOOKING_FOR_BEGIN":
            if (newChar == '/'):
                BlockIdx = 0
                bufferBlock= bufferBlock+ newChar
                BlockIdx = BlockIdx + 1 #we store value into buffer block for CRC verification
                temporarystate = "PARSER_LOOKING_FOR_LETTER1"
                print(temporarystate)
            else:
                temporarystate = "PARSER_LOOKING_FOR_BEGIN"
                print(temporarystate)
        elif "PARSER_LOOKING_FOR_LETTER1" == temporarystate:
            if newChar.isalpha():
                temporarystate = "PARSER_LOOKING_FOR_LETTER2"
                print(temporarystate)
                bufferBlock = bufferBlock + newChar
                BlockIdx = BlockIdx + 1
            else:
                temporarystate= "PARSER_LOOKING_FOR_BEGIN"
        elif temporarystate == "PARSER_LOOKING_FOR_LETTER2":
            if newChar.isalpha():
                temporarystate = "PARSER_LOOKING_FOR_LETTER3"
                print(temporarystate)
                bufferBlock = bufferBlock + newChar
                BlockIdx = BlockIdx + 1
            else:
                temporarystate= "PARSER_LOOKING_FOR_BEGIN"
        elif temporarystate == "PARSER_LOOKING_FOR_LETTER3":
            if newChar.isalpha():
                temporarystate = "PARSER_LOOKING_FOR_NUMBER"
                print(temporarystate)
                bufferBlock = bufferBlock + newChar
                BlockIdx = BlockIdx + 1
            else:
                temporarystate = "PARSER_LOOKING_FOR_BEGIN"
        elif temporarystate == "PARSER_LOOKING_FOR_NUMBER":
            if newChar.isdigit():
                temporarystate = "PARSER_LOOKING_FOR_CR1"
                print(temporarystate)
                bufferBlock = bufferBlock + newChar
                BlockIdx = BlockIdx + 1
            else:
                temporarystate = "PARSER_LOOKING_FOR_BEGIN"
                print(temporarystate)
        elif temporarystate=="PARSER_LOOKING_FOR_CR1":
            if newChar == "\r": #if we receive \r
                bufferBlock = bufferBlock + newChar
                BlockIdx = BlockIdx + 1
                temporarystate = "PARSER_LOOKING_FOR_LF1"
                print(temporarystate)
            elif (IDidx <= 1024):  #and (P1P_IsPrintableChar(newChar)))
            #We don't know the exact length of ID but we know Data bloc can be up to 1024characters
                bufferBlock = bufferBlock + newChar
                BlockIdx =BlockIdx +1
                IDidx=IDidx+1
            else:
                temporarystate= "PARSER_LOOKING_FOR_BEGIN"
                print(temporarystate)
        elif temporarystate == "PARSER_LOOKING_FOR_LF1":
            if (newChar == "\n"):
                bufferBlock = bufferBlock + newChar
                BlockIdx =BlockIdx +1
                temporarystate = "PARSER_LOOKING_FOR_CR2"
                print(temporarystate)
            else:
                temporarystate = "PARSER_LOOKING_FOR_BEGIN"
                print(temporarystate)
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
                print(temporarystate)
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
                print(temporarystate)
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
                print(temporarystate)
            elif newChar == "\r":
                temporarystate = "PARSER_LOOKING_FOR_LF"
                print(temporarystate)
            else:
                temporarystate = "PARSER_LOOKING_FOR_BEGIN"

        elif temporarystate == "PARSER_LOOKING_FOR_CRC":
            if newChar.isdigit():
                if CRCLen <= 4:
                    bufferCRC = bufferCRC + newChar
                    CRCLen= CRCLen + 1
                if CRCLen == CRC:
                    temporarystate = "PARSER_LOOKING_FOR_CR"
                print(temporarystate)
            else:
                temporarystate = "PARSER_LOOKING_FOR_BEGIN"

        elif temporarystate == "PARSER_LOOKING_FOR_CR":
            if newChar == "\r": #if we receive \r
                temporarystate = "PARSER_LOOKING_FOR_LF"
                print(temporarystate)
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
        print("Im out of for")
        extractvalues(bufferData)
        print(ListofDataValues)
        print("energyConsumed: ", ListofDataValues[0])
        print("energyProduced: ", ListofDataValues[1])
        print("powerConsumed: ", ListofDataValues[2])
        print("powerProduced: ", ListofDataValues[3])

# -------------------------------------------
#function call for  P1Parser_Receive_char(DataFromTelegram)
#-------------------------------------------
#P1Parser_Receive_char(DataFromTelegram) #work correctly#

Exemple1   = "/ISk5\2ME383-1008\r\n\r\n0-0:96.1.0(52127969)\n1-0:0.9.1(140217)\n1-0:0.9.2(150427)\n1-0:1.8.0(000688.01*kWh)\n1-0:1.7.0(000131.72*kWh)\n1-0:1.8.2(000000.08*kWh)\n1-0:1.8.3(000000.26*kWh)\n1-0:1.7.0(000.000*kW)\n1-0:3.7.0(000.000*kvar)\n1-0:0.8.0(00900)\n1-0:0.3.0(01000)\n1-0:0.3.1(01000)\n!\r\n"
#P1Parser_Receive_char(Exemple1)


#-------------------------------------------
#Getting data from the file and trying to parse and extractvalues
#-------------------------------------------
metertelegram= open("MeterTelegram.txt", 'rU')
lines = metertelegram.read()
metertelegram.close()
print (lines)
for line in lines:
    line=line.strip()
if (isinstance(lines,str)):
    P1Parser_Receive_char(lines)
else:
    print ("error it's not a string")