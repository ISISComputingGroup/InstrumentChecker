from __future__ import absolute_import
import unittest
import os
import xml.etree.ElementTree as ET
from parameterized import parameterized

from .settings import Settings
from util.common import CommonUtils, skip_on_instruments
from util.configurations import ConfigurationUtils, ComponentUtils
from util.globals import GlobalsUtils
from .abstract_test_utils import AbstractSingleTests


class ConfigurationsSingleTests(AbstractSingleTests):
    """
    Tests in this class will be run exactly once regardless of how many configs exist.
    """

    TOTAL_NON_INTERESTING_PVS_IN_BLOCKS = 0

    def __init__(self, *args, **kwargs):
        super(ConfigurationsSingleTests, self).__init__(*args, **kwargs)
        self._configuration_utils = ConfigurationUtils(Settings.config_repo_path)

    @property
    def utils(self):
        return self._configuration_utils

    @property
    def type(self):
        return "configurations"

    def test_GIVEN_an_instrument_THEN_the_configurations_directory_exists_and_contains_at_least_one_configuration(self):
        self.assertGreaterEqual(len(self.utils.get_configurations_as_list()), 1,
                                "Configurations directory was empty or did not exist")

    def update_total_non_interesting_block_pvs(self, num_non_interesting_block_pvs):
        ConfigurationsSingleTests.TOTAL_NON_INTERESTING_PVS_IN_BLOCKS += num_non_interesting_block_pvs


class ConfigurationsTests(unittest.TestCase):
    """
    Tests in this class will run once per config. If there are no configs, these tests will not run.

    This is so that one failing config doesn't hide another error in a different config.

    The configuration name can be accessed as self.config
    """

    def __init__(self, method_name, config=None):
        # Boilerplate so that unittest knows how to run these tests.
        super(ConfigurationsTests, self).__init__(method_name)

        self.config_utils = ConfigurationUtils(Settings.config_repo_path)
        self.comp_utils = ComponentUtils(Settings.config_repo_path)
        self.global_utils = GlobalsUtils(Settings.config_repo_path)
        self.config = config

    def setUp(self):
        # Class has to have an __init__ that accepts one argument for unittest's test loader to work properly.
        # However it should never be the default (None) when actually running the tests.
        self.assertIsNotNone(self.config, "Config should not be None")

        self.config_dir_path = os.path.join(self.config_utils.get_configurations_directory(), self.config)

        self.assertTrue(os.path.isdir(self.config_dir_path), "Config directory should exist ({})"
                        .format(self.config_dir_path))

    def _skip_if_valid_iocs_pv_is_not_available(self):
        if Settings.valid_iocs is None or Settings.protected_iocs is None:
            self.skipTest("Couldn't retrieve valid/protected IOCS from server.")

    def test_GIVEN_a_configuration_THEN_it_only_contains_valid_iocs(self):
        self._skip_if_valid_iocs_pv_is_not_available()

        for ioc in self.config_utils.get_iocs(self.config_utils.get_iocs_xml(self.config)):

            self.assertIn(ioc, Settings.valid_iocs,
                          "Configuration {} contained an IOC that the server didn't know about ({})"
                          .format(self.config, ioc))

    def test_GIVEN_a_configuration_THEN_it_does_not_contain_any_invalid_iocs(self):
        self._skip_if_valid_iocs_pv_is_not_available()

        for ioc in self.config_utils.get_iocs(self.config_utils.get_iocs_xml(self.config)):
            self.assertNotIn(ioc, Settings.protected_iocs,
                             "Configuration {} contained a protected IOC ({})".format(self.config, ioc))

    def test_GIVEN_a_configuration_and_active_components_THEN_does_not_contain_multiple_instances_of_same_ioc(self):
        components = self.config_utils.get_active_components_as_list(self.config)

        iocs = self.config_utils.get_iocs(self.config_utils.get_iocs_xml(self.config))

        for comp in components:
            iocs.extend(self.comp_utils.get_iocs(self.comp_utils.get_iocs_xml(comp)))

        for ioc in iocs:
            self.assertEqual(len([i for i in iocs if i == ioc]), 1,
                             "Configuration {} contained multiple instances of ioc ({})".format(self.config, ioc))

    def test_GIVEN_a_configuration_THEN_the_directory_does_not_contain_unexpected_files(self):
        for filename in os.listdir(self.config_dir_path):
            self.assertIn(filename, ConfigurationUtils.ALLOWED_CONFIG_FILES,
                          "Component {} contained unexpected files in it's directory ({})"
                          .format(self.config, filename))

    def test_GIVEN_a_configuration_THEN_the_directory_contains_the_required_config_files(self):
        for filename in ConfigurationUtils.REQUIRED_CONFIG_FILES:
            self.assertIn(filename, os.listdir(self.config_dir_path),
                          "Configuration {} did not contain the required config file {}"
                          .format(self.config, filename))

    def test_GIVEN_a_configurations_directory_WHEN_parsing_its_contents_as_xml_THEN_no_errors_generated(self):
        for filename in CommonUtils.get_directory_contents_as_list(self.config_dir_path):
            # pvlist is not xml
            if filename != ConfigurationUtils.BLOCK_GW_PVLIST:
                try:
                    ET.parse(os.path.join(self.config_dir_path, filename))
                except Exception as e:
                    self.fail("Exception occurred while parsing file {} in configuration {} as XML. Error was: {}"
                            .format(filename, self.config, e))

    @skip_on_instruments(["DEMO"], "This does not matter on DEMO, and we often demo software in slightly odd configs")
    def test_GIVEN_a_configuration_WHEN_motors_are_used_THEN_both_or_neither_of_com_setting_and_motor_control_number_are_defined(self):
        iocs_xml = self.config_utils.get_iocs_xml(self.config)
        for motor_ioc in CommonUtils.MOTOR_IOCS:
            defined_macros = self.config_utils.get_ioc_macros(iocs_xml, motor_ioc)

            controller_number_defined = "MTRCTRL" in defined_macros
            comms_macro_defined = any(m in defined_macros for m in ["PORT", "GALILADDR"])

            self.assertTrue(controller_number_defined == comms_macro_defined,  # Both or neither
                            "Only one of com setting and motor control was defined in {} in component {}"
                            .format(motor_ioc, self.config))

    @skip_on_instruments(["DEMO"], "Demo is allowed to have IOCs in simulation mode, it is a fake instrument")
    def test_GIVEN_ioc_xml_WHEN_simlevel_is_not_none_THEN_get_ioc_in_sim_mode_returns_false(self):
        iocs_xml = self.config_utils.get_iocs_xml(self.config)

        for ioc in self.config_utils.get_iocs(iocs_xml):
            self.assertFalse(self.config_utils.get_ioc_in_sim_mode(iocs_xml, ioc),
                             "Simulation Mode is Active on {} in configuration {}".format(ioc, self.config))

    def test_GIVEN_a_configuration_and_active_components_THEN_it_does_not_contain_blocks_that_are_the_same_ignoring_case(self):
        components = self.config_utils.get_active_components_as_list(self.config)

        blocks = self.config_utils.get_blocks(self.config)

        for comp in components:
            blocks.extend(self.comp_utils.get_blocks(comp))

        duplicates = set([x for x in blocks if blocks.count(x) > 1])

        self.assertTrue(len(duplicates) == 0, "Duplicate blocks found in {}: {}".format(self.config, duplicates))

        upper_blocks = [b.upper() for b in blocks]
        duplicates = set([x for x in upper_blocks if upper_blocks.count(x) > 1])

        self.assertTrue(len(duplicates) == 0, "Case insensitive duplicate blocks found in {}: {}"
                        .format(self.config, duplicates))

    def test_GIVEN_a_configuration_THEN_it_does_not_contain_a_block_with_invalid_name_length(self):
        components = self.config_utils.get_active_components_as_list(self.config)

        blocks = self.config_utils.get_blocks(self.config)
        
        for comp in components:
            blocks.extend(self.comp_utils.get_blocks(comp))
        
        invalid_names = set([str(block) + " | len " + str(len(block)) for block in blocks if len(block) > 25])
        self.assertTrue(len(invalid_names) == 0, "Invalid block name length (> 25): {} , in configuration {}".format(invalid_names, self.config))
    

    def _test_for_ioc_present_at_least_one_macro_set(self, ioc, macro_name, macro_regex, value_regex):
        iocs_xml = self.config_utils.get_iocs_xml(self.config)
        iocs = self.config_utils.get_iocs(iocs_xml)
        
        if ioc in iocs:
            config_macros = self.config_utils.check_if_macros_match_pattern(self.config_utils.get_ioc_macros(iocs_xml, ioc),
                        macro_regex, search_for_value=False)
            globals_macros = self.config_utils.check_if_macros_match_pattern(self.global_utils.get_macros(ioc), 
                        macro_regex, search_for_value=False)            
            
            self.assertTrue(len(config_macros)!=0 or len(globals_macros)!=0, 
                        "No {} macros found in {} in configuration {}".format(macro_name, ioc, self.config))

            config_macros = self.config_utils.check_if_macros_match_pattern(config_macros, value_regex, 
                        search_for_value=True)
            globals_macros = self.config_utils.check_if_macros_match_pattern(globals_macros, value_regex, 
                        search_for_value=True)

            self.assertTrue(len(config_macros) != 0 or len(globals_macros) != 0, 
                        "At least one {} macro in {} not set in configuration {}".format(macro_name, ioc, self.config))
    
    @parameterized.expand(
        [("MCLEN_{:02d}".format(i),"AXIS", "^AXIS[1-8]$", "^yes$") for i in range(1, 4)] +
        [("EUROTHRM_{:02d}".format(i), "ADDRESS", "^ADDR_([1-9]|10)$", "^[0-9]+$") for i in range(1, 7)] +
        [("LINMOT_{:02d}".format(i), "AXIS", "^AXIS[1-8]$", "^yes$") for i in range(1, 4)] +
        [("KHLY2001_01", "CHANNEL ACTIVATED", "^ACTIVATE_CHAN_0[1-9]$", "^1$")] +
        [("NWPRTXPS_01", "AXIS", "^AXIS[1-4]_ID$", "^.*[.].*$")]
    )
    @skip_on_instruments(ConfigurationUtils.DUMMY_INSTRUMENTS, "Allowed invalid iocs, these are dummy instruments")
    def test_GIVEN_a_config_THEN_for_each_ioc_present_at_least_one_macro_set(self, ioc, macro_name, macro_regex, value_regex):
        self._test_for_ioc_present_at_least_one_macro_set(ioc, macro_name, macro_regex, value_regex)
    
    @parameterized.expand(
        [("MERCURY_{:02d}".format(i), "TEMPERATURE/LEVEL/PRESSURE", "^(TEMP_[1-4]|LEVEL_[1-2]|PRESSURE_[1-2])$", "^.*[.].*$") 
        for i in range(1, 3)]
    )
    @skip_on_instruments(ConfigurationUtils.DUMMY_INSTRUMENTS, "Allowed invalid iocs, these are dummy instruments")
    @skip_on_instruments(["LARMOR", "ZOOM", "IRIS", "SANDALS", "GEM", "MAPS", "OSIRIS", "LET"], "Mercury iTC macros on these instruments are out of date")
    def test_GIVEN_a_config_THEN_for_each_mercury_present_at_least_one_macro_set(self, ioc, macro_name, macro_regex, value_regex):
        self._test_for_ioc_present_at_least_one_macro_set(ioc, macro_name, macro_regex, value_regex)
