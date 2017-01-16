import io
class FileReader:
    def __init__(self):  # Notre méthode constructeur
        self.telegram=""

    def TelegramfileReading(self):

        with io.open("MeterTelegram.txt", 'rt', newline='') as f:
            lines = f.readlines()
            for line in lines:
                # print (line.strip())
                self.telegram = self.telegram + str(line) #convert list of lines to string