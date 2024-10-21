from __future__ import absolute_import

import os
import re
import xml.etree.ElementTree as ET
from builtins import object

from tests.settings import Settings

from .common import CommonUtils


class AbstractConfigurationUtils(object):
    """
    Class containing utility methods common to both configuration and component directories.
    """

    REQUIRED_CONFIG_FILES = ["blocks.xml", "components.xml", "groups.xml", "iocs.xml", "meta.xml"]
    BLOCK_GW_PVLIST = "gwblock.pvlist"
    ALLOWED_CONFIG_FILES = REQUIRED_CONFIG_FILES + [
        "screens.xml",
        "block_config.xml",
        BLOCK_GW_PVLIST,
    ]
    DUMMY_INSTRUMENTS = ["SELAB", "DEMO"]

    IOC_XML_SCHEMA = "{http://epics.isis.rl.ac.uk/schema/iocs/1.0}"
    COMPONENT_XML_SCHEMA = "{http://epics.isis.rl.ac.uk/schema/components/1.0}"
    BLOCK_XML_SCHEMA = "{http://epics.isis.rl.ac.uk/schema/blocks/1.0}"
    DEVICES_XML_SCHEMA = "{http://epics.isis.rl.ac.uk/schema/screens/1.0/}"

    def __init__(self, config_repo_path: str) -> None:
        self.config_repo_path = config_repo_path

    def get_configurations_directory(self) -> str:
        raise NotImplementedError("This is an abstract class, use a concrete class instead")

    def get_configurations_as_list(self) -> list[str]:
        """
        Gets a list of all configurations/components of the current instrument.
        :return: a list of strings.
        """
        return CommonUtils.get_folders_in_directory_as_list(self.get_configurations_directory())

    def get_active_components_as_list(self, config_name: str) -> list[str]:
        """
        Gets a list of active components for a particular configuration.
        :param config_name: the configuration name
        :return: a list of components
        """
        return self.get_active_components_from_xml(self.get_components_xml(config_name))

    def get_components_xml(self, config_name: str) -> str:
        """
        Gets the XML corresponding to the components file for a particular configuration.
        :param config_name: the configuration name
        :return: the XML as a string
        """
        path = os.path.join(self.get_configurations_directory(), config_name, "components.xml")
        with open(path) as xml_file:
            return xml_file.read()

    def get_active_components_from_xml(self, xml: str) -> list[str]:
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

    def get_set_of_block_pvs_for_all_configs(self) -> set[str]:
        """
        Gets a set of all pvs that have a block on them in any configuration or component
        of the instrument.
        :return: A set of strings representing the names of the pvs.
        """
        block_pvs_set = {
            block_pv
            for config in self.get_configurations_as_list()
            for block_pv in self.get_block_pvs(config)
        }

        return block_pvs_set

    def get_block_pvs(self, config_name: str) -> list[str]:
        """
        Gets list of PVs that have a block on them for a particular configuration or component.
        :param config_name: Name of configuration or component.
        :return: list of PVs that have a block on them.
        """

        return self.get_block_pvs_from_xml(Settings.pv_prefix, self.get_blocks_xml(config_name))

    def get_blocks_xml(self, config_name: str) -> str:
        """
        Gets the XML corresponding to the blocks file for a particular configuration.
        :param config_name: the configuration name
        :return: the XML containing the blocks as a string
        """
        path = os.path.join(self.get_configurations_directory(), config_name, "blocks.xml")

        with open(path) as xml_file:
            return xml_file.read()

    def get_block_pvs_from_xml(self, pv_prefix: str, block_xml: str) -> list[str]:
        """
        Gets a list of all PVs which a have block on them in a certain component or configuration.
        :param pv_prefix: A string representing the instrument prefix of the PV. If the PV is local,
        then this prefix will be ignored.
        :param block_xml: A string representing the XML block data of a component or configuration.
        :return: A list of the names of all PVs which have a block on them.
        The names of the PV include the instrument prefix.
        """
        root = ET.fromstring(block_xml)
        pvs_with_blocks = []

        for block in root.iter("{}block".format(self.BLOCK_XML_SCHEMA)):
            pv_name_block = block.find("{}read_pv".format(self.BLOCK_XML_SCHEMA))
            assert pv_name_block is not None
            pv_name = pv_name_block.text
            assert pv_name is not None
            pv_name = AbstractConfigurationUtils._get_pv_name_without_field(pv_name)

            local_block = block.find("{}local".format(self.BLOCK_XML_SCHEMA))
            assert local_block is not None
            if local_block.text == "True":
                pv_name = pv_prefix + pv_name

            pvs_with_blocks.append(pv_name)

        return pvs_with_blocks

    def get_blocks(self, config_name: str) -> list[str]:
        """
        Returns a list of block names.
        :param config_name: the configuration name
        :return: The list of block names.
        """
        root = ET.fromstring(self.get_blocks_xml(config_name))

        blocks = []
        for block in root.iter("{}block".format(self.BLOCK_XML_SCHEMA)):
            blocks_raw = block.find("{}name".format(self.BLOCK_XML_SCHEMA))
            assert blocks_raw is not None
            blocks.append(blocks_raw.text)

        return blocks

    @staticmethod
    def _get_pv_name_without_field(pv_name: str) -> str:
        """
        Removes any PV field from a name a block is pointing to
        so it will return the name of the PV of the field the block points to.
        :param pv_name: a string representing a name a block is pointing to.
        :return: The name of the pv of the field, as a string.
        """
        if "." in pv_name:
            return pv_name[: pv_name.index(".")]
        else:
            return pv_name

    def get_devices_directory(self) -> str:
        raise NotImplementedError("This is an abstract class, use a concrete class instead")

    def get_device_screens_from_xml(self) -> str:
        """
        Gets the XML corresponding to the Device Screens for the instrument
        Returns: the XML as a string
        """
        path = os.path.join(self.get_devices_directory(), "screens.xml")
        with open(path) as xml_file:
            return xml_file.read()

    def get_device_screens(self, xml: str) -> set[str]:
        """
        Args:
            xml: XML input to parse
        Returns:
            (set): Set of device screens
        """
        root = ET.fromstring(xml)

        devices = set()
        for device in root:
            devices_raw = device.find(f"{self.DEVICES_XML_SCHEMA}key")
            assert devices_raw is not None
            devices.add(devices_raw.text)

        return devices

    def get_iocs_xml(self, config_name: str) -> str:
        """
        Gets the XML corresponding to the IOCs file for a particular configuration.
        :param config_name: the configuration or component name
        :return: the XML as a string
        """
        path = os.path.join(self.get_configurations_directory(), config_name, "iocs.xml")
        with open(path) as xml_file:
            return xml_file.read()

    def get_iocs(self, xml: str) -> list[str]:
        """
        Returns a list of iocs in the xml provided.
        :return:
        """
        root = ET.fromstring(xml)

        iocs = []
        for ioc in root.iter("{}ioc".format(self.IOC_XML_SCHEMA)):
            iocs.append(ioc.attrib["name"])

        return iocs

    def get_ioc_macros(self, xml: str, ioc_name: str) -> dict[str, str]:
        """
        Returns a dictionary of macro information for a given ioc_name in the given xml.

        :param xml: The IOC xml.
        :param ioc_name: The name of the ioc.
        :return: A dictionary of macro information.
        Keys are the macro name, values are the macro value
        """
        # Parse the XML
        root = ET.fromstring(xml)

        ioc_xml = tuple(
            ioc
            for ioc in root.iter("{}ioc".format(self.IOC_XML_SCHEMA))
            if ioc.attrib["name"] == ioc_name
        )

        # Extract the macros
        if len(ioc_xml) == 0:
            return dict()
        else:
            return {
                m.attrib["name"]: m.attrib["value"]
                for m in ioc_xml[0].iter("{}macro".format(self.IOC_XML_SCHEMA))
            }

    def get_ioc_in_sim_mode(self, xml: str, ioc_name: str) -> bool:
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
            assert ioc is not None
            if ioc.attrib["name"] == ioc_name:
                return ioc.attrib["simlevel"] != "none"
        raise ValueError(f"Can't get simulation level of ioc {ioc_name}")

    @staticmethod
    def check_if_macros_match_pattern(
        macros: dict[str, str], regex: str, search_for_value: bool
    ) -> dict[str, str]:
        """
        Returns all macros which match a specific pattern
        :param macros: Dictionary (name:value) of macros
        :param regex: Regex to pattern match against
        :param search_for_value: Boolean for whether to check against name or value
        :return: A dictionary (name:value) of matching macros
        """
        matching_macros = {}

        for name, value in macros.items():
            if re.search(regex, value if search_for_value else name):
                matching_macros.update({name: value})

        return matching_macros


class ConfigurationUtils(AbstractConfigurationUtils):
    """
    Class containing utility methods for interacting with the configurations directory
    """

    def get_configurations_directory(self) -> str:
        return os.path.join(self.config_repo_path, "configurations", "configurations")


class ComponentUtils(AbstractConfigurationUtils):
    """
    Class containing utility methods for interacting with components
    """

    BASE_COMPONENT = "_base"

    def get_configurations_directory(self) -> str:
        return os.path.join(self.config_repo_path, "configurations", "components")


class DeviceUtils(AbstractConfigurationUtils):
    """
    Class containing the utility methods of interacting with the devices directory
    """

    def get_devices_directory(self) -> str:
        return os.path.join(self.config_repo_path, "configurations", "devices")
