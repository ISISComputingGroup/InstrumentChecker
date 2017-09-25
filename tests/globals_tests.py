import unittest
from settings import Settings
from util.globals import GlobalsUtils


class GlobalsTests(unittest.TestCase):

    def setUp(self):
        self.globals_utils = GlobalsUtils(Settings.config_repo_path)
        if not self.globals_utils.file_exists():
            self.skipTest("Globals file did not exist.")

    def test_globals_has_correct_syntax(self):
        for linenumber, line in enumerate(self.globals_utils.get_lines(), 1):
            self.assertIsInstance(line, basestring)
            self.assertTrue(self.globals_utils.check_syntax(line),
                            "Invalid syntax on line {linenumber}. Line contents was: {contents}"
                            .format(linenumber=linenumber, contents=line))

    def test_that_there_are_no_unexpected_globals_files(self):
        self.assertEqual(self.globals_utils.get_number_of_globals_files(), 1 if self.globals_utils.file_exists() else 0,
                         "Extra globals files ({}) files in repository.".format(self.globals_utils.GLOBALS_FILE))
