import configparser
import os

class IniFile:
    def __init__(self, filename):
        self.filename = filename

        if os.path.exists(filename):
            self.cp = configparser.ConfigParser()
            self.cp.read(filename)

    def __del__(self):
        with open(self.filename, "w") as config_file:
            self.cp.write(config_file)
