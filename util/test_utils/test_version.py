import unittest

from util.version import VersionUtils


class VersionTests(unittest.TestCase):

    def test_GIVEN_two_identical_versions_WHEN_checking_if_they_are_similar_THEN_result_is_true(self):
        # Arrange
        version1 = "4.0.0"
        version2 = "4.0.0"

        # Act / Assert
        self.assertTrue(VersionUtils.versions_similar(version1, version2))
        self.assertTrue(VersionUtils.versions_similar(version2, version1))

    def test_GIVEN_two_different_versions_WHEN_checking_if_they_are_similar_THEN_result_is_false(self):
        # Arrange
        version1 = "4.0.0"
        version2 = "3.0.0"

        # Act / Assert
        self.assertFalse(VersionUtils.versions_similar(version1, version2))
        self.assertFalse(VersionUtils.versions_similar(version2, version1))

    def test_GIVEN_two_identical_versions_where_one_has_a_checksum_appended_WHEN_checking_if_they_are_similar_THEN_result_is_true(self):
        # Arrange
        version1 = "4.0.0"
        version2 = "4.0.0.abc123abc"

        # Act / Assert
        self.assertTrue(VersionUtils.versions_similar(version1, version2))
        self.assertTrue(VersionUtils.versions_similar(version2, version1))

    def test_GIVEN_two_different_versions_where_one_has_a_checksum_appended_WHEN_checking_if_they_are_similar_THEN_result_is_false(self):
        # Arrange
        version1 = "4.0.0"
        version2 = "3.0.0.abc123abc"

        # Act / Assert
        self.assertFalse(VersionUtils.versions_similar(version1, version2))
        self.assertFalse(VersionUtils.versions_similar(version2, version1))

    def test_GIVEN_only_minor_version_is_different_WHEN_checking_if_they_are_similar_THEN_result_is_false(self):
        # Arrange
        version1 = "4.0.0"
        version2 = "4.2.0"

        # Act / Assert
        self.assertFalse(VersionUtils.versions_similar(version1, version2))
        self.assertFalse(VersionUtils.versions_similar(version2, version1))

    def test_GIVEN_only_minor_version_is_different_WHEN_checking_if_they_are_similar_THEN_result_is_false(self):
        # Arrange
        version1 = "4.0.0"
        version2 = "4.0.2"

        # Act / Assert
        self.assertFalse(VersionUtils.versions_similar(version1, version2))
        self.assertFalse(VersionUtils.versions_similar(version2, version1))
