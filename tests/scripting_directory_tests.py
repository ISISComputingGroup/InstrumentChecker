from __future__ import absolute_import
import unittest
import os
from unittest import skip

from .settings import Settings
from util.scripting import ScriptingUtils


class ScriptingDirectoryTests(unittest.TestCase):

    def setUp(self):
        self.script_utils = ScriptingUtils(Settings.config_repo_path)
        self.python_dir = self.script_utils.get_scripting_directory()
        self.inst_directory = self.script_utils.get_instrument_scripts_directory()
        self.inst_file = self.script_utils.get_instrument_script_file()
        self.name = Settings.name

        # Skip all tests in this class if scripting directory doesn't exist
        # Can't do this using skipIf because it's runtime behaviour
        if not os.path.isdir(self.python_dir):
            self.skipTest("Python directory not present")

    def test_GIVEN_a_python_directory_exists_THEN_it_contains_a_correctly_named_init_file(self):

        init_files = [file for file in os.listdir(self.python_dir)
                             if file.endswith(".py") and file.startswith("init_")]

        expected_init_file = "init_{}.py".format(self.name.lower().replace("-", "_"))

        self.assertIn(expected_init_file, init_files, "Instrument init file not found")
        self.assertEqual(len(init_files), 1, "Expected exactly one init file")

    @staticmethod
    def _directory_contains_compiled_files(dir):
        return len([file for file in os.listdir(dir) if file.endswith(".pyc")]) != 0

    @skip("This currently doesn't pass on any instruments but we should consider enforcing this.")
    def test_GIVEN_python_directory_exists_THEN_compiled_python_files_are_not_in_git(self):
        self.assertFalse(self._directory_contains_compiled_files(self.python_dir),
                         "Python directory contained compiled files")

    def test_GIVEN_that_python_directory_exists_THEN_inst_directory_exists(self):
        inst_is_dir = os.path.isdir(self.inst_directory)
        inst_is_file = os.path.isfile(self.inst_file)
        self.assertTrue(inst_is_dir or inst_is_file, "Instrument scripts directory/file is missing")

    @skip("This currently doesn't pass on any instruments but we should consider enforcing this.")
    def test_GIVEN_that_instrument_scripts_directory_exists_THEN_it_does_not_contain_compiled_python_files(self):

        if not os.path.isdir(self.inst_directory):
            self.skipTest("Instrument scripts directory missing")

        self.assertFalse(self._directory_contains_compiled_files(self.inst_directory),
                         "Instrument scripts directory contained compiled files")

    def test_GIVEN_init_file_in_inst_directory_then_its_contents_is_the_same_as_on_the_master_branch(self):
        if not os.path.isdir(self.inst_directory):
            self.skipTest("Instrument scripts directory missing")

        init_file = os.path.join(self.inst_directory, "__init__.py")

        self.assertTrue(os.path.isfile(init_file), "inst init file missing")
        self.assertTrue(self.script_utils.diff_against_latest_master(init_file) == "",
                        "inst/__init__.py had contents which differed from the one on origin/master")
