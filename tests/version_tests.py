import unittest
from tests.settings import Settings
from util.channel_access import ChannelAccessUtils
from util.common import skip_on_instruments
from util.version import VersionUtils


class VersionTests(unittest.TestCase):

    def setUp(self):
        self.version_utils = VersionUtils(Settings.config_repo_path)
        self.ca = ChannelAccessUtils(Settings.pv_prefix)

    def test_WHEN_looking_for_config_version_file_THEN_it_exists(self):
        self.assertTrue(self.version_utils.version_file_exists(), "Config version file did not exist")

    def test_WHEN_counting_config_version_files_in_repository_THEN_there_is_exactly_one_file(self):
        self.assertLessEqual(self.version_utils.count_config_version_files(), 1,
                             "There should not be more than one '{}' file in the repository."
                             .format(VersionUtils.VERSION_FILE))

    @skip_on_instruments(["DEMO"], "DEMO does not typically have a full release installed")
    def test_GIVEN_version_file_exists_THEN_it_is_the_same_as_version_pv_on_server(self):
        if not self.version_utils.version_file_exists():
            self.skipTest("Version file did not exist.")

        config_version = self.version_utils.get_version()
        server_version = self.ca.get_version_string()

        if server_version is None:
            self.skipTest("Couldn't connect to version PV on server")

        if (Settings.name == "POLREF" or Settings.name == "CRISP") and server_version.startswith("7.2.0"):
            self.skipTest("Reflectometry reverted to 7.2.0 due to #6472")

        # Special case for server version 0.0.0 which is a development release - assume it's always up to date.
        if not server_version.startswith("0.0.0"):
            self.assertTrue(self.version_utils.versions_similar(config_version, server_version),
                            "Config version was wrong. Server version={}, config version={}"
                            .format(server_version, config_version))
