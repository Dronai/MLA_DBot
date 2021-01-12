import os, datetime
from dotenv import load_dotenv

class Logger:

    load_dotenv()

    def __init__(self):
        self.path =  os.getenv('LOG_PATH')

    def write_file(self, content):
        fichier = open(self.path, "a")
        fichier.write("\n" + content)
        fichier.close()

    def getDate(self):
        return datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    
    def info(self, content):
        conte = "[" + str(self.getDate()) + "] INFO: " + content
        self.write_file(conte)

    def error(self, content):
        conte = "[" + str(self.getDate()) + "] ERROR: " + content
        self.write_file(conte)