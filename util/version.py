import os


class VersionUtils(object):
    """
    Class containing utility methods for interacting with the Python scripting directory
    """

    def __init__(self, config_repo_path):
        self.config_repo_path = config_repo_path
        self.version_file_path = os.path.join(self.config_repo_path, "configurations", "config_version.txt")

    def version_file_exists(self):
        return os.path.isfile(self.version_file_path)

    def get_version(self):
        return open(self.version_file_path).readline().strip()
