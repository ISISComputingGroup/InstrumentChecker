import os

from util.common import CommonUtils


class VersionUtils(object):
    """
    Class containing utility methods relating to the version of IBEX.
    """

    VERSION_FILE = "config_version.txt"

    def __init__(self, config_repo_path):
        self.config_repo_path = config_repo_path
        self.version_file_path = os.path.join(self.config_repo_path, "configurations", VersionUtils.VERSION_FILE)

    def version_file_exists(self):
        return os.path.isfile(self.version_file_path)

    def count_config_version_files(self):
        """
        Scans the entire config repo for files named (VERSION_FILE). Returns the number of these files that were found.
        :return: the number of files named (VERSION_FILE)
        """
        return CommonUtils.count_files_with_name(self.config_repo_path, VersionUtils.VERSION_FILE)

    def get_version(self):
        return open(self.version_file_path).readline().strip()

    @staticmethod
    def versions_similar(version1, version2):
        return all(v1 == v2 for v1, v2 in zip(version1.split("."), version2.split(".")))

    @staticmethod
    def convert_release_to_branch_name(major, minor=0, patch=0):
        return "Release_{maj}.{min}.{patch}".format(maj=int(major), min=int(minor), patch=int(patch))

    @staticmethod
    def extract_release_numbers_from_string(version):
        return version.split(".")[0:3]
