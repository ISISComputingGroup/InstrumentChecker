import unittest

from tests.settings import Settings
from util.gui import GuiUtils
from util.synoptic import SynopticUtils
from util.version import VersionUtils


class SynopticTests(unittest.TestCase):

    def __init__(self, methodName, synoptic=None):
        # Boilerplate so that unittest knows how to run these tests.
        super(SynopticTests, self).__init__(methodName)

        self.synoptic = synoptic

    def setUp(self):
        self.gui_utils = GuiUtils(Settings.gui_repo_path)
        self.synoptic_utils = SynopticUtils(Settings.config_repo_path)
        self.version_utils = VersionUtils(Settings.config_repo_path)

        if not self.version_utils.version_file_exists():
            self.skipTest("Can't determine which version of the GUI is being used.")

        self.gui_utils.get_gui_repo_at_release(self.version_utils.get_version())

    def test_type_target_pairs_used_in_synoptic_appear_in_opi_info_for_the_relevant_gui_version(self):

        allowed_pairs = self.gui_utils.get_type_target_pairs(self.gui_utils.get_opi_info_xml())

        try:
            type_target_pairs = self.synoptic_utils.get_type_target_pairs(self.synoptic_utils.get_xml(self.synoptic))
        except Exception as e:
            self.fail("In synoptic {}, XML failed to parse properly. Error text was: {}"
                      .format(self.synoptic, e))

        for type, target in type_target_pairs:
            if self.synoptic_utils.should_be_ignored(type, target):
                continue

            elif type == "UNKNOWN":
                self.assertIn(target, [target for _, target in allowed_pairs],
                              "In synoptic {}, type={} is unknown at gui version{}"
                              .format(self.synoptic, target, self.version_utils.get_version()))

            else:
                self.assertIn((type, target), allowed_pairs,
                              "In synoptic {}, type={} and target={} is unknown at gui version {}"
                              .format(self.synoptic, type, target, self.version_utils.get_version()))
