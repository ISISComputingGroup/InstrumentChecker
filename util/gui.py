from builtins import object
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
        version = VersionUtils.extract_release_numbers_from_string(version)
        branch_name = VersionUtils.convert_release_to_branch_name(*version)
        if not self.git.update_branch(branch_name):
            raise IOError("Couldn't check out GUI branch corresponding to release {}".format(version))

    def get_valid_types(self, xml):
        root = ET.fromstring(xml)
        result = []

        for component in root.iter("entry"):
            type = component.find("./value/type").text

            if type is not None:
                result.append(type)

        return result

    def get_valid_targets(self, xml):
        root = ET.fromstring(xml)
        result = []

        for component in root.iter("entry"):
            target = component.find("./key").text

            if target is not None:
                result.append(target)

        return result

    def get_opi_info_xml(self):
        with open(os.path.join(self.path, "base", "uk.ac.stfc.isis.ibex.opis", "resources", "opi_info.xml")) as f:
            return f.read()
