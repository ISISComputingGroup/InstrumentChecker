import unittest
import os
from settings import Settings
from util.components import ComponentUtils


class ComponentsSingleTests(unittest.TestCase):
    """
    Tests in this class will be run exactly once regardless of how many configs exist.
    """

    def setUp(self):
        self.component_utils = ComponentUtils(Settings.config_repo_path)

    def test_that_components_directory_contains_base_component(self):
        self.assertIn(ComponentUtils._BASE_COMPONENT, self.component_utils.get_configurations_as_list(),
                      "Base component was missing (should be called {})".format(ComponentUtils._BASE_COMPONENT))


class ComponentsTests(unittest.TestCase):
    """
    Tests in this class will run once per component.

    This is so that one failing component doesn't hide another error in a different component.

    The component name can be accessed as self.config
    """

    def __init__(self, methodName, config=None):
        # Boilerplate so that unittest knows how to run these tests.
        super(ComponentsTests, self).__init__(methodName)

        self.config_utils = ComponentUtils(Settings.config_repo_path)
        self.config = config

    def setUp(self):
        self.assertIsNotNone(self.config, "Config should not be None")
        self.assertIsInstance(self.config, basestring, "Config name should be a string")
        self.assertGreater(len(self.config), 0, "Config name should be a non-empty string")
        self.config_dir_path = os.path.join(self.config_utils.get_configurations_directory(), self.config)
        self.assertTrue(os.path.isdir(self.config_dir_path), "Config directory should exist ({})"
                        .format(self.config_dir_path))

    def _skip_if_valid_iocs_pv_is_not_available(self):
        if Settings.valid_iocs is None or Settings.protected_iocs is None:
            self.skipTest("Couldn't retrieve valid/protected IOCS from server.")

    def test_that_the_given_component_only_contains_valid_iocs(self):
        self._skip_if_valid_iocs_pv_is_not_available()

        for ioc in self.config_utils.get_iocs(self.config):
            self.assertIn(ioc, Settings.valid_iocs,
                          "Configuration {} contained an IOC that the server didn't know about ({})"
                          .format(self.config, ioc))

            if self.config != ComponentUtils._BASE_COMPONENT:
                self.assertNotIn(ioc, Settings.protected_iocs,
                                 "Component {} contained a protected IOC ({})".format(self.config, ioc))

