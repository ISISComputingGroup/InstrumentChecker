import unittest
import os
import xml.etree.ElementTree as ET

from settings import Settings
from util.common import CommonUtils, skip_on_instruments
from util.configurations import ComponentUtils
from abstract_test_utils import AbstractSingleTests


class ComponentsSingleTests(AbstractSingleTests):
    """
    Tests in this class will be run exactly once regardless of how many components exist.
    """
    TOTAL_NON_INTERESTING_PVS_IN_BLOCKS = 0

    def setUp(self):
        self.utils = ComponentUtils(Settings.config_repo_path)
        self.type = "components"

    def test_GIVEN_components_directory_THEN_it_contains_the_base_component(self):
        self.assertIn(ComponentUtils.BASE_COMPONENT, self.utils.get_configurations_as_list(),
                      "Base component was missing (should be called {})".format(ComponentUtils.BASE_COMPONENT))

    def print_total_non_interesting_block_pvs(self, num_non_interesting_block_pvs):
        ComponentsSingleTests.TOTAL_NON_INTERESTING_PVS_IN_BLOCKS += num_non_interesting_block_pvs
        print("{} non interesting component block pvs in total across all instruments".format(
                ComponentsSingleTests.TOTAL_NON_INTERESTING_PVS_IN_BLOCKS))


class ComponentsTests(unittest.TestCase):
    """
    Tests in this class will run once per component.

    This is so that one failing component doesn't hide another error in a different component.

    The component name can be accessed as self.config
    """

    def __init__(self, methodName, component=None):
        # Boilerplate so that unittest knows how to run these tests.
        super(ComponentsTests, self).__init__(methodName)

        self.component_utils = ComponentUtils(Settings.config_repo_path)
        self.component = component

    def setUp(self):
        # Class has to have an __init__ that accepts one argument for unittest's test loader to work properly.
        # However it should never be the default (None) when actually running the tests.
        self.assertIsNotNone(self.component, "Component should not be None")

        self.component_dir_path = os.path.join(self.component_utils.get_configurations_directory(), self.component)

        self.assertTrue(os.path.isdir(self.component_dir_path), "Config directory should exist ({})"
                        .format(self.component_dir_path))

    def _skip_if_valid_iocs_pv_is_not_available(self):
        if Settings.valid_iocs is None or Settings.protected_iocs is None:
            self.skipTest("Couldn't retrieve valid/protected IOCS from server.")

    def test_GIVEN_a_component_THEN_it_only_contains_valid_iocs(self):
        self._skip_if_valid_iocs_pv_is_not_available()

        for ioc in self.component_utils.get_iocs(self.component_utils.get_iocs_xml(self.component)):
            self.assertIn(ioc, Settings.valid_iocs,
                          "Component {} contained an IOC that the server didn't know about ({})"
                          .format(self.component, ioc))

    def test_GIVEN_a_component_THEN_it_does_not_contain_protected_iocs_unless_it_is_the_base_component(self):
        self._skip_if_valid_iocs_pv_is_not_available()

        for ioc in self.component_utils.get_iocs(self.component_utils.get_iocs_xml(self.component)):
            if self.component != ComponentUtils.BASE_COMPONENT:
                self.assertNotIn(ioc, Settings.protected_iocs,
                                 "Component {} contained a protected IOC ({})".format(self.component, ioc))

    def test_GIVEN_a_components_directory_THEN_it_only_contains_the_allowed_files(self):
        for filename in os.listdir(self.component_dir_path):
            self.assertIn(filename, ComponentUtils.ALLOWED_CONFIG_FILES,
                          "Component {} contained unexpected files in it's directory ({})"
                          .format(self.component, filename))

    def test_GIVEN_a_components_directory_THEN_it_contains_the_required_files(self):
        for filename in ComponentUtils.REQUIRED_CONFIG_FILES:
            self.assertIn(filename, os.listdir(self.component_dir_path),
                          "Component {} did not contain the required config file {}"
                          .format(self.component, filename))

    def test_GIVEN_a_components_directory_WHEN_parsing_its_contents_as_xml_THEN_no_errors_generated(self):
        for filename in CommonUtils.get_directory_contents_as_list(self.component_dir_path):
            try:
                ET.parse(os.path.join(self.component_dir_path, filename))
            except Exception as e:
                self.fail("Exception occurred while parsing file {} in component {} as XML. Error was: {}"
                          .format(filename, self.component, e))

    @skip_on_instruments(["DEMO"], "This does not matter on DEMO, and we often demo software in slightly odd configs")
    def test_GIVEN_a_configuration_WHEN_motors_are_used_THEN_both_or_neither_of_com_setting_and_motor_control_number_are_defined(
            self):
        iocs_xml = self.component_utils.get_iocs_xml(self.component)
        for motor_ioc in CommonUtils.MOTOR_IOCS:
            defined_macros = self.component_utils.get_ioc_macros(iocs_xml, motor_ioc)

            controller_number_defined = "MTRCTRL" in defined_macros
            comms_macro_defined = any(m in defined_macros for m in ["PORT", "GALILADDR"])

            self.assertTrue(controller_number_defined == comms_macro_defined,  # Both or neither
                            "Only one of com setting and motor control was defined in {} in component {}"
                            .format(motor_ioc, self.component))

    @skip_on_instruments(["DEMO"], "Demo is allowed to have IOCs in simulation mode, it is a fake instrument")
    def test_GIVEN_ioc_xml_WHEN_simlevel_is_not_none_THEN_get_ioc_in_sim_mode_returns_false(self):
        if Settings.name == "DEMO":
            self.skipTest("Having IOCs in simulation mode is valid on DEMO")

        iocs_xml = self.component_utils.get_iocs_xml(self.component)

        for ioc in self.component_utils.get_iocs(iocs_xml):
            self.assertFalse(self.component_utils.get_ioc_in_sim_mode(iocs_xml, ioc),
                             "Simulation Mode is Active on {} in component {}".format(ioc, self.component))
