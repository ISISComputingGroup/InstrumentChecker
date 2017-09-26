import unittest

from util.gui import GuiUtils


class GuiTests(unittest.TestCase):
    def test_GIVEN_a_3_level_version_WHEN_construct_release_branch_name_THEN_appropriate(self):
        # Arrange
        major = 3
        minor = 2
        patch = 1

        # Act
        branchname = GuiUtils._convert_release_to_branch_name(major, minor, patch)

        # Assert
        self.assertEqual(branchname, "Release_3.2.1")

    def test_GIVEN_a_2_level_version_WHEN_construct_release_branch_name_THEN_appropriate(self):
        # Arrange
        major = 3
        minor = 2

        # Act
        branchname = GuiUtils._convert_release_to_branch_name(major, minor)

        # Assert
        self.assertEqual(branchname, "Release_3.2.0")

    def test_GIVEN_a_1_level_version_WHEN_construct_release_branch_name_THEN_appropriate(self):
        # Arrange
        major = 3

        # Act
        branchname = GuiUtils._convert_release_to_branch_name(major)

        # Assert
        self.assertEqual(branchname, "Release_3.0.0")

    def test_GIVEN_a_3_level_version_in_a_string_THEN_arguments_extracted_appropriately(self):
        # Arrange
        version = "3.2.1"

        # Act
        major, minor, patch = GuiUtils._extract_release_numbers_from_string(version)

        # Assert
        self.assertEqual(3, int(major))
        self.assertEqual(2, int(minor))
        self.assertEqual(1, int(patch))

    def test_GIVEN_a_3_level_version_with_a_checksum_in_a_string_THEN_arguments_extracted_appropriately(self):
        # Arrange
        version = "3.2.1.abc123abc"

        # Act
        major, minor, patch = GuiUtils._extract_release_numbers_from_string(version)

        # Assert
        self.assertEqual(3, int(major))
        self.assertEqual(2, int(minor))
        self.assertEqual(1, int(patch))

    def test_GIVEN_a_2_level_version_with_a_checksum_in_a_string_THEN_arguments_extracted_appropriately(self):
        # Arrange
        version = "3.2"

        # Act
        major, minor = GuiUtils._extract_release_numbers_from_string(version)

        # Assert
        self.assertEqual(3, int(major))
        self.assertEqual(2, int(minor))
