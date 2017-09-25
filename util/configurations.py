import os
from common import CommonUtils


class ConfigurationUtils(object):
    """
    Class containing utility methods for interacting with the configurations directory
    """

    def __init__(self, config_repo_path):
        self.config_repo_path = config_repo_path

    def get_configurations_directory(self):
        return os.path.join(self.config_repo_path, "configurations", "configurations")

    def get_configurations_as_list(self):
        return CommonUtils.get_directory_contents_as_list(self.get_configurations_directory())
