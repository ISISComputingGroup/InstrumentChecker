import os
import xml.etree.ElementTree as ET
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
        return CommonUtils.get_folders_in_directory_as_list(self.get_configurations_directory())

    def get_iocs(self, config_name):
        """
        Returns a list of iocs in the configuration.
        :return:
        """
        root = ET.parse(os.path.join(self.get_configurations_directory(), config_name, "iocs.xml"))

        iocs = []
        for ioc in root.iter("ioc"):
            iocs.append(ioc.attrib["name"])

        return iocs
