import unittest
import os
from settings import Settings
from util.scripting import ScriptingUtils


class ScriptingDirectoryTests(unittest.TestCase):

    def setUp(self):
        self.script_utils = ScriptingUtils(Settings.config_repo_path)
        self.python_dir = self.script_utils.get_scripting_directory()
        self.inst_directory = self.script_utils.get_instrument_scripts_directory()
        self.name = Settings.name

        # Skip all tests in this class if scripting directory doesn't exist
        # Can't do this using skipIf because it's runtime behaviour
        if not os.path.isdir(self.python_dir):
            self.skipTest("Python directory not present")

    def test_python_directory_contains_an_init_file_with_the_correct_name(self):

        init_files = [file for file in os.listdir(self.python_dir)
                             if file.endswith(".py") and file.startswith("init_")]

        expected_init_file = "init_{}.py".format(self.name.lower().replace("-", "_"))

        self.assertIn(expected_init_file, init_files, "Instrument init file not found")
        self.assertEqual(len(init_files), 1, "Expected exactly one init file")

    @staticmethod
    def _directory_contains_compiled_files(dir):
        return len([file for file in os.listdir(dir) if file.endswith(".pyc")]) != 0

    def test_python_directory_does_not_contain_compiled_files(self):
        self.assertFalse(self._directory_contains_compiled_files(self.python_dir),
                         "Python directory contained compiled files")

    def test_that_inst_directory_exists(self):
        self.assertTrue(os.path.isdir(self.inst_directory), "Instrument scripts directory missing")

    def test_that_inst_directory_does_not_contain_compiled_files(self):

        self.assertTrue(os.path.isdir(self.inst_directory), "Instrument scripts directory missing")
        self.assertFalse(self._directory_contains_compiled_files(self.inst_directory),
                         "Instrument scripts directory contained compiled files")
