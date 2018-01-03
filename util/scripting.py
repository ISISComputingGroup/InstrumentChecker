import os


class ScriptingUtils(object):
    """
    Class containing utility methods for interacting with the Python scripting directory
    """

    def __init__(self, config_repo_path):
        self.config_repo_path = config_repo_path

    def get_scripting_directory(self):
        return os.path.join(self.config_repo_path, "Python")

    def get_instrument_scripts_directory(self):
        return os.path.join(self.get_scripting_directory(), "inst")
