import os
import xml.etree.ElementTree as ET
from common import CommonUtils


class AbstractConfigurationUtils(object):
    """
    Class containing utility methods common to both configuration and component directories.
    """
    REQUIRED_CONFIG_FILES = ["blocks.xml", "components.xml", "groups.xml", "iocs.xml", "meta.xml"]
    ALLOWED_CONFIG_FILES = REQUIRED_CONFIG_FILES + ["screens.xml"]

    XML_SCHEMA = "{http://epics.isis.rl.ac.uk/schema/iocs/1.0}"

    def __init__(self, config_repo_path):
        self.config_repo_path = config_repo_path

    def get_configurations_directory(self):
        raise NotImplementedError("This is an abstract class, use a concrete class instead")

    def get_configurations_as_list(self):
        return CommonUtils.get_folders_in_directory_as_list(self.get_configurations_directory())

    def get_iocs_xml(self, config_name):
        """
        Gets the XML corresponding to the IOCs file for a particular configuration.
        :param config_name: the configuration or component name
        :return: the XML as a string
        """
        path = os.path.join(self.get_configurations_directory(), config_name, "iocs.xml")
        with open(path) as f:
            return f.read()

    def get_iocs(self, xml):
        """
        Returns a list of iocs in the xml provided.
        :return:
        """
        root = ET.fromstring(xml)

        iocs = []
        for ioc in root.iter("{}ioc".format(self.XML_SCHEMA)):
            iocs.append(ioc.attrib["name"])

        return iocs

    def get_ioc_macros(self, xml, ioc_name, config_name):
        """
        Returns a dictionary of macro information for a given ioc_name in the given xml.

        :param xml: The IOC xml.
        :param ioc_name: The name of the ioc.
        :param config_name: The name of the configuration we're looking in.
        :return: A dictionary of macro information. Keys are the macro name, values are the macro value
        """
        # Parse the XML
        root = ET.fromstring(xml)
        ioc_xml = tuple(ioc for ioc in root.iter("{}ioc".format(self.XML_SCHEMA)) if ioc.attrib["name"] == ioc_name)

        # Extract the macros
        if len(ioc_xml) == 0:
            return dict()
        else:
            return {m.attrib["name"]: m.attrib["value"] for m in ioc_xml[0].iter("{}macro".format(self.XML_SCHEMA))}

    def get_ioc_in_sim_mode(self, xml, ioc_name):
        """
        Returns true if the given ioc_name is in simulation mode
        :param xml: The IOC xml.
        :param ioc_name: The name of the ioc.
        :return: True if in simulation mode, otherwise false.
        """
        # Parse the XML
        root = ET.fromstring(xml)

        # check the simulation mode for the given ioc
        for ioc in root.iter("{}ioc".format(self.XML_SCHEMA)):
            if ioc.attrib["name"] == ioc_name:
                return ioc.attrib["simlevel"] != "none"



class ConfigurationUtils(AbstractConfigurationUtils):
    """
    Class containing utility methods for interacting with the configurations directory
    """
    def get_configurations_directory(self):
        return os.path.join(self.config_repo_path, "configurations", "configurations")


class ComponentUtils(AbstractConfigurationUtils):
    """
    Class containing utility methods for interacting with components
    """
    BASE_COMPONENT = "_base"

    def get_configurations_directory(self):
        return os.path.join(self.config_repo_path, "configurations", "components")
