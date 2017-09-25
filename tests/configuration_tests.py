import unittest
import os
from settings import Settings
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
        self.assertTrue(os.path.isdir(self.config_dir_path))
