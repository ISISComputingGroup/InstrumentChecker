import os
import xml.etree.ElementTree as ET
from builtins import object

from util.git_wrapper import GitUtils
from util.version import VersionUtils


class GuiUtils(object):
    """
    Class containing utility methods for interacting with the gui repository.
    """

    def __init__(self, path: str) -> None:
        self.git = GitUtils(path)
        self.path = path

    def get_gui_repo_at_release(self, version_str: str) -> None:
        version: list[int] = VersionUtils.extract_release_numbers_from_string(version_str)
        branch_name: str = VersionUtils.convert_release_to_tag_name(*version)
        if not self.git.update_branch(branch_name, True):
            raise IOError(
                "Couldn't check out GUI branch corresponding to release {}".format(version)
            )

    def get_valid_types(self, xml: str) -> list[str]:
        root = ET.fromstring(xml)
        result = []

        for component in root.iter("entry"):
            type_element: ET.Element | None = component.find("./value/type")
            assert type_element is not None
            type = type_element.text

            if type is not None:
                result.append(type)

        return result

    def get_valid_targets(self, xml: str) -> list[str]:
        root = ET.fromstring(xml)
        result = []

        for component in root.iter("entry"):
            target_element: ET.Element | None = component.find("./key")
            assert target_element is not None
            target = target_element.text

            if target is not None:
                result.append(target)

        return result

    def get_opi_info_xml(self) -> str:
        with open(
            os.path.join(
                self.path, "base", "uk.ac.stfc.isis.ibex.opis", "resources", "opi_info.xml"
            )
        ) as f:
            return f.read()
