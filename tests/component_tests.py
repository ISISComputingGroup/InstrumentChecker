import unittest
import os
from settings import Settings
from util.common import CommonUtils
from util.configurations import ComponentUtils
import xml.etree.ElementTree as ET


class ComponentsSingleTests(unittest.TestCase):
    """
    Tests in this class will be run exactly once regardless of how many configs exist.
    """

    def setUp(self):
        self.component_utils = ComponentUtils(Settings.config_repo_path)

    def test_GIVEN_components_directory_THEN_it_contains_the_base_component(self):
        self.assertIn(ComponentUtils.BASE_COMPONENT, self.component_utils.get_configurations_as_list(),
                      "Base component was missing (should be called {})".format(ComponentUtils.BASE_COMPONENT))


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
        self.assertIsNotNone(self.component, "Config should not be None")

        self.component_dir_path = os.path.join(self.component_utils.get_configurations_directory(), self.component)

        self.assertTrue(os.path.isdir(self.component_dir_path), "Config directory should exist ({})"
                        .format(self.component_dir_path))

    def _skip_if_valid_iocs_pv_is_not_available(self):
        if Settings.valid_iocs is None or Settings.protected_iocs is None:
            self.skipTest("Couldn't retrieve valid/protected IOCS from server.")

    def test_GIVEN_a_component_THEN_it_only_contains_valid_iocs(self):
        self._skip_if_valid_iocs_pv_is_not_available()

        for ioc in self.component_utils.get_iocs(self.component):
            self.assertIn(ioc, Settings.valid_iocs,
                          "Component {} contained an IOC that the server didn't know about ({})"
                          .format(self.component, ioc))

    def test_GIVEN_a_component_THEN_it_does_not_contain_protected_iocs_unless_it_is_the_base_component(self):
        self._skip_if_valid_iocs_pv_is_not_available()

        for ioc in self.component_utils.get_iocs(self.component):
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
