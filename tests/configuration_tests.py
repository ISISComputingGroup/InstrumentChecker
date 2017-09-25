import unittest
import os
from settings import Settings
from util.channel_access import ChannelAccessUtils
from util.configurations import ConfigurationUtils


class ConfigurationsSingleTests(unittest.TestCase):
    """
    Tests in this class will be run exactly once regardless of how many configs exist.
    """

    def setUp(self):
        self.config_utils = ConfigurationUtils(Settings.config_repo_path)

    def test_that_configs_directory_contains_at_least_one_config(self):
        self.assertGreaterEqual(len(self.config_utils.get_configurations_as_list()), 1,
                                "Configurations directory was empty or did not exist")


class ConfigurationsTests(unittest.TestCase):
    """
    Tests in this class will run once per config. If there are no configs, these tests will not run.

    This is so that one failing config doesn't hide another error in a different config.

    The configuration name can be accessed as self.config
    """

    def __init__(self, methodName, config=None):
        # Boilerplate so that unittest knows how to run these tests.
        super(ConfigurationsTests, self).__init__(methodName)

        self.config_utils = ConfigurationUtils(Settings.config_repo_path)
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

    def test_that_the_given_configuration_only_contains_valid_iocs(self):
        self._skip_if_valid_iocs_pv_is_not_available()

        for ioc in self.config_utils.get_iocs(self.config):

            self.assertIn(ioc, Settings.valid_iocs,
                          "Configuration {} contained an IOC that the server didn't know about ({})"
                          .format(self.config, ioc))

            self.assertNotIn(ioc, Settings.protected_iocs,
                             "Configuration {} contained a protected IOC ({})".format(self.config, ioc))

    def test_that_configurations_directory_only_contains_allowed_config_files(self):
        for filename in os.listdir(self.config_dir_path):
            self.assertIn(filename, ConfigurationUtils.ALLOWED_CONFIG_FILES,
                          "Component {} contained unexpected files in it's directory ({})"
                          .format(self.config, filename))

    def test_that_all_of_the_required_config_files_are_present_in_the_directory(self):
        for filename in ConfigurationUtils.REQUIRED_CONFIG_FILES:
            self.assertIn(filename, os.listdir(self.config_dir_path),
                          "Configuration {} did not contain the required config file {}"
                          .format(self.config, filename))
