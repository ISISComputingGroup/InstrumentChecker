import unittest
from settings import Settings
from util.globals import GlobalsUtils


class GlobalsTests(unittest.TestCase):

    def setUp(self):
        self.globals_utils = GlobalsUtils(Settings.config_repo_path)
        if not self.globals_utils.file_exists():
            self.skipTest("Globals file did not exist.")


    def test_globals_has_correct_syntax(self):
        for line in self.globals_utils.get_lines():
            self.assertTrue(self.globals_utils.check_syntax(line))

