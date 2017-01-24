#Libraries - Classes
from readfile import *
from p1parserclass import *



#-------------------------------------------
#Getting data from the file and trying to parse and extractvalues
#-------------------------------------------

#instanciate from fileReaderClass, one object called file:
file= FileReader("C:\\Users\Amel\Documents\TWINGZ\P1ParserPython\MeterTelegram.txt")
file.TelegramfileReading()
parser = P1Parser()  #one object from p1parserclass
telegram=file.telegram
bufferblock = telegram.split("!")
telegram= bufferblock[0] + "!" + "\r\n"
#print ("Telegram in the file\r\n", telegram)
#print(CRC16().calculate(telegram)) #58668= 0xE52C

if (isinstance(file.telegram, str)):
    parser.P1Parser_Receive_char(file.telegram)
    parser.converttojson()





#extra for help


#-----------------------
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





#input = "/KFM5KAIFA-METER\r\n\r\n1-0:1.8.0(000671.578*kWh)\r\n1-0:2.8.0(000842.472*kWh)\r\n1-0:2.8.1(000000.000*kWh)\r\n1-0:2.8.2(000000.000*kWh)\r\n0-0:96.14.0(0001)\r\n1-0:1.7.0(00.333*kW)\r\n1-0:2.7.0(00.444*kW)\r\n!"
#print(CRC16().calculate(input))

#bufferblock1="/KFM5KAIFA-METER\r\n\r\n1-0:1.8.0(000671.578*kWh)\r\n1-0:2.8.0(000842.472*kWh)\r\n1-0:1.7.0(00.333*kW)\r\n1-0:2.7.0(00.444*kW)\r\n!"
#print(CRC16().calculate(bufferblock1)) #399E


#bufferblock2="/ISk5\2MT382-1000\r\n\r\n1-3:0.2.8(40)0-0:1.0.0(101209113020W)\r\n" \
       #      "0-0:96.1.1(4B384547303034303436333935353037)\r\n1-0:1.8.1(123456.789*kWh)\r\n1-0:1.8.2(123456.789*kWh)\r\n1-0:2.8.1(123456.789*kWh)\r\n1-0:2.8.2(123456.789*kWh)\r\n" \
        #     "0-0:96.14.0(0002)\r\n1-0:1.7.0(01.193*kW)\r\n1-0:2.7.0(00.000*kW)\r\n0-0:17.0.0(016.1*kW)\r\n0-0:96.3.10(1)\r\n0-0:96.7.21(00004)\r\n0-0:96.7.9(00002)\r\n1-0:99:97.0(2)(0:96.7.19)(101208152415W)(0000000240*s)(101208151004W)(00000000301*s)1-0:32.32.0(00002)\r\n1-0:52.32.0(00001)\r\n1-0:72:32.0(00000)\r\n1-0:32.36.0(00000)\r\n1-0:52.36.0(00003)\r\n1-0:72.36.0(00000)\r\n0-0:96.13.1(3031203631203831)\r\n0-0:96.13.0(303132333435363738393A3B3C3D3E3F303132333435363738393A3B3C3D3E3F303132333435363738393A3B\r\n3C3D3E3F303132333435363738393A3B3C3D3E3F303132333435363738393A3B3C3D3E3F)\r\n0-1:24.1.0(03)\r\n0-1:96.1.0(3232323241424344313233343536373839)\r\n0-1:24.2.1(101209110000W)(12785.123*m3)\r\n0-1:24.4.0(1)\r\n!"
#print(CRC16().calculate(bufferblock2))#522B