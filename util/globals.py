import os
import re


class GlobalsUtils(object):
    """
    Class containing utility methods for interacting with globals.txt
    """

    def __init__(self, config_repo_dir):
        self.config_repo_dir = config_repo_dir

    def _get_file_path(self):
        return os.path.join(self.config_repo_dir, "configurations", "globals.txt")

    def file_exists(self):
        return os.path.isfile(self._get_file_path())

    def get_lines(self):
        try:
            globals_file = open(self._get_file_path(), "r")
            return [i for i in globals_file.readlines()]
        except IOError:
            return []

    @staticmethod
    def check_syntax(line):
        # Remove comments, discard anything after a "#" sign
        line = line.split('#')[0]
        line = line.strip()

        alphanumeric = r"[a-zA-Z0-9]+"

        iocname_regex = r"{alphanumeric}(_?{alphanumeric})+".format(alphanumeric=alphanumeric)
        macro_regex = iocname_regex
        value_regex = r".*"

        regexp = r"^({ioc}__)?{macro}={value}$".format(ioc=iocname_regex, macro=macro_regex, value=value_regex)

        if line == "" or re.match(regexp, line):
            return True
        else:
            return False
