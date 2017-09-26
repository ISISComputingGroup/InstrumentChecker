import unittest
from settings import Settings
from util.globals import GlobalsUtils


class GlobalsTests(unittest.TestCase):

    def setUp(self):
        self.globals_utils = GlobalsUtils(Settings.config_repo_path)

    def test_GIVEN_a_globals_file_exists_THEN_it_passes_a_syntax_check(self):

        if not self.globals_utils.file_exists():
            self.skipTest("Globals file did not exist.")

        for linenumber, line in enumerate(self.globals_utils.get_lines(), 1):
            self.assertIsInstance(line, basestring)
            self.assertTrue(self.globals_utils.check_syntax(line),
                            "Invalid syntax on line {linenumber}. Line contents was: {contents}"
                            .format(linenumber=linenumber, contents=line))

    def test_WHEN_checking_the_configs_directory_THEN_there_are_no_extra_files_called_globals(self):
        self.assertEqual(self.globals_utils.get_number_of_globals_files(), 1 if self.globals_utils.file_exists() else 0,
                         "Extra globals files ({}) files in repository.".format(self.globals_utils.GLOBALS_FILE))
