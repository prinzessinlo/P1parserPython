#Libraries - Classes
from readfile import *
from p1parserclass import *


#DataFromTelegram = ""  # buffer which contain the telegram as string
#buffersize = 0  # size of telegram length

#DataFromTelegram = "/XXX5AMEL\n\n1-0:1.8.0(000688.01*kWh)\n1-0:2.8.0(000131.72*kWh)\n1-0:1.7.0(000220.08*kWh)\n1-0:2.7.0(000999.08*kWh)\n!ABCD\n"
#buffersize = len(DataFromTelegram)

 #DataFromTelegram1 = "/XXX5AMEL\n\n1-0:1.8.0(000333.01*kWh)\n1-0:2.8.0(000111.72*kWh)\n1-0:1.7.0(000229.88*kWh)\n1-0:2.7.0(000235.19*kWh)\n!ABCD\n"
#buffersize = len(DataFromTelegram1)

"""def f():
    global s
    print(s)
    s = "tu dois être global"
    print(s)"""

#-----------------------MAIN------------------------#
"""Parserstates = {"PARSER_LOOKING_FOR_BEGIN", "PARSER_LOOKING_FOR_LETTER1", "PARSER_LOOKING_FOR_LETTER2",
                "PARSER_LOOKING_FOR_LETTER3", "PARSER_LOOKING_FOR_NUMBER", "PARSER_LOOKING_FOR_CR1", "PARSER_LOOKING_FOR_LF1",
                "PARSER_LOOKING_FOR_CR2", "PARSER_LOOKING_FOR_LF2", "PARSER_LOOKING_FOR_DATAGeneral", "PARSER_LOOKING_FOR_ENDOFBLOC",
                "PARSER_LOOKING_FOR_CRC", "PARSER_LOOKING_FOR_CR", "PARSER_LOOKING_FOR_LF"}

"""
#DataFromTelegram = "/XXX5AMEL\r\n\r\n1-0:1.8.0(000688.01*kWh)\n1-0:2.8.0(000131.72*kWh)\n1-0:1.7.0(000220.08*kWh)\n1-0:2.7.0(000999.08*kWh)\n!0505\r\n"
#splitted=DataFromTelegram.split()
#print(splitted)

#print(splitted[5])


# -------------------------------------------
#function call for  P1Parser_Receive_char(DataFromTelegram)
#-------------------------------------------
#P1Parser_Receive_char(DataFromTelegram) #work correctly with \r#


#Exemple1   = "/ISk5\\2ME383-1008\r\n\r\n0-0:96.1.0(52127969)\r\n1-0:0.9.1(140217)\r\n1-0:0.9.2(150427)\r\n1-0:1.8.0(000688.01*kWh)\r\n1-0:2.8.0(000771.72*kWh)\r\n1-0:1.8.2(000000.08*kWh)\r\n1-0:1.8.3(000000.26*kWh)\r\n1-0:1.7.0(000.000*kW)\r\n1-0:3.7.0(000.000*kvar)\r\n1-0:0.8.0(00900)\r\n1-0:0.3.0(01000)\r\n1-0:0.3.1(01000)\r\n!\r\n"
#print("P1Parser Exemple1")
#P1Parser_Receive_char(Exemple1)


#-------------------------------------------
#Getting data from the file and trying to parse and extractvalues
#-------------------------------------------

#instanciate from fileReaderClass, one object called file:
"""file= FileReader()
file.TelegramfileReading()
parser = P1Parser()  #one object from p1parserclass
if (isinstance(file.telegram, str)):
