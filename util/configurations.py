import os
import xml.etree.ElementTree as ET

from common import CommonUtils
from tests.settings import Settings


class AbstractConfigurationUtils(object):
    """
    Class containing utility methods common to both configuration and component directories.
    """
    REQUIRED_CONFIG_FILES = ["blocks.xml", "components.xml", "groups.xml", "iocs.xml", "meta.xml"]
    ALLOWED_CONFIG_FILES = REQUIRED_CONFIG_FILES + ["screens.xml"]

    IOC_XML_SCHEMA = "{http://epics.isis.rl.ac.uk/schema/iocs/1.0}"
    COMPONENT_XML_SCHEMA = "{http://epics.isis.rl.ac.uk/schema/components/1.0}"
    BLOCK_XML_SCHEMA = "{http://epics.isis.rl.ac.uk/schema/blocks/1.0}"

    def __init__(self, config_repo_path):
        self.config_repo_path = config_repo_path

    def get_configurations_directory(self):
        raise NotImplementedError("This is an abstract class, use a concrete class instead")

    def get_configurations_as_list(self):
        """
        Gets a list of all configurations/components of the current instrument.
        :return: a list of strings.
        """
        return CommonUtils.get_folders_in_directory_as_list(self.get_configurations_directory())

    def get_active_components_as_list(self, config_name):
        """
        Gets a list of active components for a particular configuration.
        :param config_name: the configuration name
        :return: a list of components
        """
        return self.get_active_components_from_xml(self.get_components_xml(config_name))

    def get_components_xml(self, config_name):
        """
        Gets the XML corresponding to the components file for a particular configuration.
        :param config_name: the configuration name
        :return: the XML as a string
        """
        path = os.path.join(self.get_configurations_directory(), config_name, "components.xml")
        with open(path) as xml_file:
            return xml_file.read()

    def get_active_components_from_xml(self, xml):
        """
        Gets a list of active components from a component XML.
        :param xml: a components XML as a string
        :return: a list of components
        """
        root = ET.fromstring(xml)

        components = []
        for component in root.iter("{}component".format(self.COMPONENT_XML_SCHEMA)):
            components.append(component.attrib["name"])

        return components

    def get_set_of_block_pvs_for_all_configs(self):
        """
        Gets a set of all pvs that have a block on them in any configuration or component of the instrument.
        :return: A set of strings representing the names of the pvs.
        """
        block_pvs_set = set()

        for configuration in self.get_configurations_as_list():
            for block_pv in self.get_block_pvs(configuration):
                block_pvs_set.add(block_pv)

        return block_pvs_set

    def get_block_pvs(self, config_name):
        """
        Gets list of PVs that have a block on them for a particular configuration or component.
        :param config_name: Name of configuration or component.
        :return: list of PVs that have a block on them.
        """

        return self.get_block_pvs_from_xml(Settings.pv_prefix, self.get_blocks_xml(config_name))

    def get_blocks_xml(self, config_name):
        """
        Gets the XML corresponding to the blocks file for a particular configuration.
        :param config_name: the configuration name
        :return: the XML containing the blocks as a string
        """
        path = os.path.join(self.get_configurations_directory(), config_name, "blocks.xml")

        with open(path) as xml_file:
            return xml_file.read()

    def get_block_pvs_from_xml(self, pv_prefix, block_xml):
        """
        Gets a list of all PVs which a have block on them in a certain component or configuration.
        :param block_xml: A string representing the XML block data of a component or configuration.
        :param pv_prefix: A string representing the instrument prefix of the PV. If the PV is local, then this prefix
        will be ignored.
        :return: A list of the names of all PVs which have a block on them. The names of the PV include the instrument
        prefix.
        """
        root = ET.fromstring(block_xml)
        pvs_with_blocks = []

        for block in root.iter("{}block".format(self.BLOCK_XML_SCHEMA)):
            pv_name = block.find("{}read_pv".format(self.BLOCK_XML_SCHEMA)).text

            if block.find("{}local".format(self.BLOCK_XML_SCHEMA)).text == "True":
                pv_name = pv_prefix + pv_name

            pvs_with_blocks.append(pv_name)

        return pvs_with_blocks

    def get_iocs_xml(self, config_name):
        """
        Gets the XML corresponding to the IOCs file for a particular configuration.
        :param config_name: the configuration or component name
        :return: the XML as a string
        """
        # self.get_block_pvs_from_xml(Settings.pv_prefix, self.get_blocks_xml(config_name))
        path = os.path.join(self.get_configurations_directory(), config_name, "iocs.xml")
        with open(path) as xml_file:
            return xml_file.read()

    def get_iocs(self, xml):
        """
        Returns a list of iocs in the xml provided.
        :return:
        """
        root = ET.fromstring(xml)

        iocs = []
        for ioc in root.iter("{}ioc".format(self.IOC_XML_SCHEMA)):
            iocs.append(ioc.attrib["name"])

        return iocs

    def get_ioc_macros(self, xml, ioc_name):
        """
        Returns a dictionary of macro information for a given ioc_name in the given xml.

        :param xml: The IOC xml.
        :param ioc_name: The name of the ioc.
        :return: A dictionary of macro information. Keys are the macro name, values are the macro value
        """
        # Parse the XML
        root = ET.fromstring(xml)

        ioc_xml = tuple(ioc for ioc in root.iter("{}ioc".format(self.IOC_XML_SCHEMA)) if ioc.attrib["name"] == ioc_name)

        # Extract the macros
        if len(ioc_xml) == 0:
            return dict()
        else:
            return {m.attrib["name"]: m.attrib["value"] for m in ioc_xml[0].iter("{}macro".format(self.IOC_XML_SCHEMA))}

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
        for ioc in root.iter("{}ioc".format(self.IOC_XML_SCHEMA)):
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