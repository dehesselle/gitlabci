import configparser
import os
import errno


class IniFile:
    def __init__(self, filename):
        self.filename = filename

        if os.path.exists(filename):
            self.cp = configparser.ConfigParser()
            self.cp.read(filename)

    def __del__(self):
        with open(self.filename, "w") as config_file:
            self.cp.write(config_file)

    def __getitem__(self, item):
        return self.cp[item]


class GitlabIni(IniFile):
    def __init__(self, filename=""):
        if os.path.exists(filename):
            IniFile.__init__(self, filename)
        else:
            filename = os.getenv("HOME") + "/.local/etc/gitlab.ini"
            if os.path.exists(filename):
                IniFile.__init__(self, filename)
            else:
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)

        self.project_id = self["gitlab"]["project_id"]
        self.ci_job = self["gitlab"]["ci_job"]
        self.server = self["gitlab"]["server"]
        self.token = self["gitlab"]["access_token"]
