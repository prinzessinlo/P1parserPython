import io

class FileReader:


    def __init__(self):  # Notre méthode constructeur avce paramétre
        self.telegram=""


    def TelegramfileReading(self, filepath):
        with io.open(filepath, 'rt', newline='') as f:
            lines = f.readlines()
            for line in lines:
                # print (line.strip())
                self.telegram = self.telegram + str(line) #convert list of lines to string