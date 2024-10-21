import os
from builtins import object, zip

from util.common import CommonUtils


class VersionUtils(object):
    """
    Class containing utility methods relating to the version of IBEX.
    """

    VERSION_FILE = "config_version.txt"

    def __init__(self, config_repo_path: str) -> None:
        self.config_repo_path = config_repo_path
        self.version_file_path = os.path.join(
            self.config_repo_path, "configurations", VersionUtils.VERSION_FILE
        )

    def version_file_exists(self) -> bool:
        return os.path.isfile(self.version_file_path)

    def count_config_version_files(self) -> int:
        """
        Scans the entire config repo for files named (VERSION_FILE).
        Returns the number of these files that were found.
        :return: the number of files named (VERSION_FILE)
        """
        return CommonUtils.count_files_with_name(self.config_repo_path, VersionUtils.VERSION_FILE)

    def get_version(self) -> str:
        with open(self.version_file_path) as f:
            return f.readline().strip()

    @staticmethod
    def versions_similar(version1: str, version2: str) -> bool:
        return all(v1 == v2 for v1, v2 in zip(version1.split("."), version2.split(".")))

    @staticmethod
    def convert_release_to_tag_name(major: int, minor: int = 0, patch: int = 0) -> str:
        return "v{maj}.{min}.{patch}".format(maj=int(major), min=int(minor), patch=int(patch))

    @staticmethod
    def extract_release_numbers_from_string(version: str) -> list[int]:
        version_split = version.split(".", maxsplit=3)[0:3]
        return [int(_x) for _x in version_split]
