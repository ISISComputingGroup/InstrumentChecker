import unittest

from util.version import VersionUtils


class VersionTests(unittest.TestCase):
    def test_GIVEN_two_identical_versions_WHEN_checking_if_they_are_similar_THEN_result_is_true(
        self,
    ):
        # Arrange
        version1 = "4.0.0"
        version2 = "4.0.0"

        # Act / Assert
        self.assertTrue(VersionUtils.versions_similar(version1, version2))
        self.assertTrue(VersionUtils.versions_similar(version2, version1))

    def test_GIVEN_two_different_versions_WHEN_checking_if_they_are_similar_THEN_result_is_false(
        self,
    ):
        # Arrange
        version1 = "4.0.0"
        version2 = "3.0.0"

        # Act / Assert
        self.assertFalse(VersionUtils.versions_similar(version1, version2))
        self.assertFalse(VersionUtils.versions_similar(version2, version1))

    def test_GIVEN_two_identical_versions_where_one_has_a_checksum_appended_WHEN_checking_if_they_are_similar_THEN_result_is_true(
        self,
    ):
        # Arrange
        version1 = "4.0.0"
        version2 = "4.0.0.abc123abc"

        # Act / Assert
        self.assertTrue(VersionUtils.versions_similar(version1, version2))
        self.assertTrue(VersionUtils.versions_similar(version2, version1))

    def test_GIVEN_two_different_versions_where_one_has_a_checksum_appended_WHEN_checking_if_they_are_similar_THEN_result_is_false(
        self,
    ):
        # Arrange
        version1 = "4.0.0"
        version2 = "3.0.0.abc123abc"

        # Act / Assert
        self.assertFalse(VersionUtils.versions_similar(version1, version2))
        self.assertFalse(VersionUtils.versions_similar(version2, version1))

    def test_GIVEN_only_minor_version_is_different_WHEN_checking_if_they_are_similar_THEN_result_is_false(
        self,
    ):
        # Arrange
        version1 = "4.0.0"
        version2 = "4.2.0"

        # Act / Assert
        self.assertFalse(VersionUtils.versions_similar(version1, version2))
        self.assertFalse(VersionUtils.versions_similar(version2, version1))

    def test_GIVEN_only_patch_version_is_different_WHEN_checking_if_they_are_similar_THEN_result_is_false(
        self,
    ):
        # Arrange
        version1 = "4.0.0"
        version2 = "4.0.2"

        # Act / Assert
        self.assertFalse(VersionUtils.versions_similar(version1, version2))
        self.assertFalse(VersionUtils.versions_similar(version2, version1))

    def test_GIVEN_a_3_level_version_WHEN_construct_release_branch_name_THEN_appropriate(self):
        # Arrange
        major = 3
        minor = 2
        patch = 1

        # Act
        branchname = VersionUtils.convert_release_to_tag_name(major, minor, patch)

        # Assert
        self.assertEqual(branchname, "v3.2.1")

    def test_GIVEN_a_2_level_version_WHEN_construct_release_branch_name_THEN_appropriate(self):
        # Arrange
        major = 3
        minor = 2

        # Act
        branchname = VersionUtils.convert_release_to_tag_name(major, minor)

        # Assert
        self.assertEqual(branchname, "v3.2.0")

    def test_GIVEN_a_1_level_version_WHEN_construct_release_branch_name_THEN_appropriate(self):
        # Arrange
        major = 3

        # Act
        branchname = VersionUtils.convert_release_to_tag_name(major)

        # Assert
        self.assertEqual(branchname, "v3.0.0")

    def test_GIVEN_a_3_level_version_in_a_string_THEN_arguments_extracted_appropriately(self):
        # Arrange
        version = "3.2.1"

        # Act
        major, minor, patch = VersionUtils.extract_release_numbers_from_string(version)

        # Assert
        self.assertEqual(3, int(major))
        self.assertEqual(2, int(minor))
        self.assertEqual(1, int(patch))

    def test_GIVEN_a_3_level_version_with_a_checksum_in_a_string_THEN_arguments_extracted_appropriately(
        self,
    ):
        # Arrange
        version = "3.2.1.abc123abc"

        # Act
        major, minor, patch = VersionUtils.extract_release_numbers_from_string(version)

        # Assert
        self.assertEqual(3, int(major))
        self.assertEqual(2, int(minor))
        self.assertEqual(1, int(patch))

    def test_GIVEN_a_2_level_version_in_a_string_THEN_arguments_extracted_appropriately(self):
        # Arrange
        version = "3.2"

        # Act
        major, minor = VersionUtils.extract_release_numbers_from_string(version)

        # Assert
        self.assertEqual(3, int(major))
        self.assertEqual(2, int(minor))
