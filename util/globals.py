import os
import re

from util.common import CommonUtils


class GlobalsUtils(object):
    """
    Class containing utility methods for interacting with globals.txt
    """

    GLOBALS_FILE = "globals.txt"

    def __init__(self, config_repo_dir):
        self.config_repo_dir = config_repo_dir

    def _get_file_path(self):
        return os.path.join(self.config_repo_dir, "configurations", GlobalsUtils.GLOBALS_FILE)

    def file_exists(self):
        return os.path.isfile(self._get_file_path())

    def get_number_of_globals_files(self):
        """
        Scans the entire config repo for files named (GLOBALS_FILE). Returns the number of these files that were found.
        :return: the number of files named (GLOBALS_FILE)
        """
        return CommonUtils.count_files_with_name(self.config_repo_dir, GlobalsUtils.GLOBALS_FILE)

    def get_lines(self):
        try:
            globals_file = open(self._get_file_path(), "r")
            return [i for i in globals_file.readlines()]
        except IOError:
            return []

    def get_macros(self, ioc_name):
        """
        Get the macros associated with an ioc of the given name
        :param ioc_name: Name of the IOC to search for
        :return: A dictionary of macros (keys) and values
        """
        lines = self.get_lines()
        macros = dict()
        for line in lines:
            if line.startswith(ioc_name):
                key, value = line.replace("{}__".format(ioc_name), "").split("=")
                macros[key] = value
        return macros

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
