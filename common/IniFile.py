import configparser
import os
import errno


class IniFile:
    def __init__(self, filename):
        self.filename = filename
        self.cp = configparser.ConfigParser()
        if os.path.exists(filename):
            self.cp.read(filename)

    def __del__(self):
        with open(self.filename, "w") as config_file:
            self.cp.write(config_file)

    def __getitem__(self, item):
        return self.cp[item]

    def __contains__(self, key):
        return self.cp.__contains__(key)

    def __setitem__(self, item1, item2="", item3=""):
        if not item3:
            self.cp[item1] = item2
        else:
            self.cp[item1][item2] = item3


class GitlabIni(IniFile):
    def __init__(self, filename=""):
        if not filename:   # Use default filename?
            config_dir = os.getenv("XDG_CONFIG_HOME")
            if not config_dir:
                config_dir = os.getenv("HOME") + "/.config"
            filename = config_dir + "/gitlabci.ini"

        if os.path.exists(filename):
            IniFile.__init__(self, filename)
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)

        self.project_id = self["gitlab"]["project_id"]
        self.server = self["gitlab"]["server"]
        self.token = self["gitlab"]["access_token"]
