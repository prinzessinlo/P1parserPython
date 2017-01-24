import io

class FileReader:


    def __init__(self, filepath):  # Notre méthode constructeur avce paramétre
        self.telegram=""
        self.filepath= filepath

    def TelegramfileReading(self):
        with io.open("C:\\Users\Amel\Documents\TWINGZ\P1ParserPython\MeterTelegram.txt", 'rt', newline='') as f:
            lines = f.readlines()
            for line in lines:
                # print (line.strip())
                self.telegram = self.telegram + str(line) #convert list of lines to string

    def TelegramfileReading(self):
        with io.open(self.filepath, 'rt', newline='') as f:
            lines = f.readlines()
            for line in lines:
                # print (line.strip())
                self.telegram = self.telegram + str(line) #convert list of lines to string