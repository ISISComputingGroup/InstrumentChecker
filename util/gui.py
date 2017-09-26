from util.git_wrapper import GitUtils
import xml.etree.ElementTree as ET
import os

from util.version import VersionUtils


class GuiUtils(object):
    """
    Class containing utility methods for interacting with the gui repository.
    """

    def __init__(self, path):
        self.git = GitUtils(path)
        self.path = path

    def get_gui_repo_at_release(self, version):
        self.git.force_clean_checkout(
            VersionUtils.convert_release_to_branch_name(*VersionUtils.extract_release_numbers_from_string(version)))

    def get_type_target_pairs(self, xml):
        """
        Returns a set of type, target pairs defined in the opi_info xml
        :param xml: string version of the xml
        """
        root = ET.fromstring(xml)
        result = []

        for component in root.iter("entry"):
            target = component.find("./key").text
            type = component.find("./value/type").text

            if type is not None and target is not None:
                result.append((type, target))

        return result

    def get_opi_info_xml(self):
        return open(os.path.join(self.path, "base",
                                 "uk.ac.stfc.isis.ibex.opis", "resources", "opi_info.xml"), "r").read()

