# from ExtractValues import *

from readfile import *

from p1parserclass import *

#TOFIX function call in P1Parser.py

DataFromTelegram = ""  # buffer which contain the telegram as string
buffersize = 0  # size of telegram length

#DataFromTelegram = "/XXX5AMEL\n\n1-0:1.8.0(000688.01*kWh)\n1-0:2.8.0(000131.72*kWh)\n1-0:1.7.0(000220.08*kWh)\n1-0:2.7.0(000999.08*kWh)\n!ABCD\n"
#buffersize = len(DataFromTelegram)

 #DataFromTelegram1 = "/XXX5AMEL\n\n1-0:1.8.0(000333.01*kWh)\n1-0:2.8.0(000111.72*kWh)\n1-0:1.7.0(000229.88*kWh)\n1-0:2.7.0(000235.19*kWh)\n!ABCD\n"
#buffersize = len(DataFromTelegram1)



parser = P1Parser()  # one object from p1parserclass
def extractvalues(data):
    meterValue = 0
    meterType = 0

    global a, b, c, d
    for letter in data:
        if parser.p1parserscanner(letter):
            #print("Je suis là!")
            meterType = parser.P1P_GetType()
            meterValue = parser.P1P_GetValue()
            if meterType == 180:
                parser.ListofDataValues[0] = meterValue  # energyConsumed
            elif meterType == 280:
                parser.ListofDataValues[1] = meterValue  # energyProduced
            elif meterType == 170:
                parser.ListofDataValues[2] = meterValue  # powerConsumed
            elif meterType == 270:
                parser.ListofDataValues[3] = meterValue  # powerProduced
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


#DataFromTelegram = "/XXX5AMEL\r\n\r\n1-0:1.8.0(000688.01*kWh)\n1-0:2.8.0(000131.72*kWh)\n1-0:1.7.0(000220.08*kWh)\n1-0:2.7.0(000999.08*kWh)\n!0505\r\n"
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
        print("Im out of for")
        extractvalues(bufferData)
        print(parser.ListofDataValues)
        print("energyConsumed: ", parser.ListofDataValues[0])
        print("energyProduced: ", parser.ListofDataValues[1])
        print("powerConsumed: ", parser.ListofDataValues[2])
        print("powerProduced: ", parser.ListofDataValues[3])

# -------------------------------------------
#function call for  P1Parser_Receive_char(DataFromTelegram)
#-------------------------------------------
#P1Parser_Receive_char(DataFromTelegram) #work correctly with \r#


Exemple1   = "/ISk5\\2ME383-1008\r\n\r\n0-0:96.1.0(52127969)\r\n1-0:0.9.1(140217)\r\n1-0:0.9.2(150427)\r\n1-0:1.8.0(000688.01*kWh)\r\n1-0:2.8.0(000771.72*kWh)\r\n1-0:1.8.2(000000.08*kWh)\r\n1-0:1.8.3(000000.26*kWh)\r\n1-0:1.7.0(000.000*kW)\r\n1-0:3.7.0(000.000*kvar)\r\n1-0:0.8.0(00900)\r\n1-0:0.3.0(01000)\r\n1-0:0.3.1(01000)\r\n!\r\n"
#print("P1Parser Exemple1")
#P1Parser_Receive_char(Exemple1)


#-------------------------------------------
#Getting data from the file and trying to parse and extractvalues
#-------------------------------------------

#instanciate from fileReaderClass, one object called file:
file= FileReader()
file.TelegramfileReading()
if (isinstance(file.telegram, str)):
    P1Parser_Receive_char(file.telegram)