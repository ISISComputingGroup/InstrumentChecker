from builtins import object
import os
import re

from util.common import CommonUtils


def strip_comments(line):
    line = line.split('#')[0]
    return line.strip()


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
            return [i for i in globals_file.read().splitlines()]
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

    def get_values_of_macro(self, macro_name):
        """
        Get the values of all macros of a given name.
        :param macro_name: The name of the macro to search for
        :return:  A dictionary of all instances of the matching values and the values.
        """
        lines = self.get_lines()
        macros = dict()
        for line in lines:
            if not line.startswith('#'):
                if macro_name in line:
                    line = strip_comments(line)
                    if "__" in line:
                        line = line.split("__")[1]
                    key, value = line.split("=")
                    macros[key] = value
        return macros

    def is_any_ioc_in_sim_mode(self):
        """
        :return: TRUE if any simulation flags are set
        """
        has_recsim = "1" in list(self.get_values_of_macro("RECSIM").values())
        has_devsim = "1" in list(self.get_values_of_macro("DEVSIM").values())
        has_simulate = "1" in list(self.get_values_of_macro("SIMULATE").values())
        return has_recsim or has_devsim or has_simulate

    @staticmethod
    def check_syntax(line):
        line = strip_comments(line)

        alphanumeric = r"[a-zA-Z0-9]+"

        iocname_regex = r"{alphanumeric}(_?{alphanumeric})+".format(alphanumeric=alphanumeric)
        macro_regex = iocname_regex
        value_regex = r".*"

        regexp = r"^({ioc}__)?{macro}={value}$".format(ioc=iocname_regex, macro=macro_regex, value=value_regex)

        if line == "" or re.match(regexp, line):
            return True
        else:
            return False
