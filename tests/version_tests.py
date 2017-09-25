import unittest
import os
from tests.settings import Settings
from util.channel_access import ChannelAccessUtils
from util.version import VersionUtils


class VersionTests(unittest.TestCase):

    def setUp(self):
        self.version_utils = VersionUtils(Settings.config_repo_path)
        self.ca = ChannelAccessUtils(Settings.pv_prefix)

    def test_that_configs_version_file_exists(self):
        self.assertTrue(self.version_utils.version_file_exists(), "Config version file did not exist")

    def test_version(self):
        if not self.version_utils.version_file_exists():
            self.skipTest("Version file did not exist.")

        config_version = self.version_utils.get_version()
        server_version = self.ca.get_version_string()

        if server_version is None:
            self.skipTest("Couldn't connect to version PV on server")

        # Use assertIn because expected version looks like "4.0.0.abc123abc"
        # whereas config_version.txt looks like "4.0.0"
        self.assertIn(config_version, server_version, "Config version was wrong. Server version={}, config version={}"
                         .format(server_version, config_version))
