#Libraries - Classes
from filereader import *
from p1parser import *



#-------------------------------------------
#Getting data from the file and trying to parse and returnmetervaluesintoalist
#-------------------------------------------

#instanciate from fileReaderClass, one object called file:
file= FileReader()
file.TelegramfileReading("C:\\Users\Amel\Documents\TWINGZ\P1ParserPython\MeterTelegram.txt")
parser = P1Parser()  #one object from p1parser (class)
telegram=file.telegram
bufferblock = telegram.split("!")
telegram= bufferblock[0] + "!" + "\r\n"


if (isinstance(file.telegram, str)):
    parser.p1parser_receive_telegram(file.telegram)
    print(parser.converttojson())
    print("Well done converted to json format")
