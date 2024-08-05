import os
from builtins import object

import git


class ScriptingUtils(object):
    """
    Class containing utility methods for interacting with the Python scripting directory
    """

    def __init__(self, config_repo_path):
        self.config_repo_path = config_repo_path

    def get_scripting_directory(self):
        """
        :return: Scripting directory base in configurations
        """
        return os.path.join(self.config_repo_path, "Python")

    def get_instrument_scripts_directory(self):
        """
        :return: directory for the instrument script module (may not exist may be a single file)
        """
        return os.path.join(self.get_scripting_directory(), "inst")

    def diff_against_latest_master(self, file_to_diff):
        repo = git.Repo(self.config_repo_path)
        return repo.git.diff("origin/master", file_to_diff)

    def get_instrument_script_file(self):
        """
        :return: the file in which instrument scripts can be held (may not exist may be a module)
        """
        return os.path.join(self.get_scripting_directory(), "inst.py")
