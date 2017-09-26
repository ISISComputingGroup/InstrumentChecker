import xml.etree.ElementTree as ET
import os


class SynopticUtils(object):
    """
    Utility methods for interacting with a synoptic.
    """

    SCHEMA = "{http://www.isis.stfc.ac.uk//instrument}"

    def __init__(self, config_repo_path):
        self.synoptics_path = os.path.join(config_repo_path, "configurations", "synoptics")

    def get_synoptics_filenames(self):
        return [f for f in os.listdir(self.synoptics_path) if f.endswith(".xml")]

    def get_type_target_pairs(self, synoptic_xml):
        """
        Returns a set of type, target pairs used in this synoptic
        :param synoptic_xml: the string version of the xml
        """

        root = ET.fromstring(synoptic_xml)
        result = []

        for component in root.iter("{schema}component".format(schema=SynopticUtils.SCHEMA)):
            type = component.find("./{schema}type".format(schema=SynopticUtils.SCHEMA)).text
            target = component.find("./{schema}target/{schema}name".format(schema=SynopticUtils.SCHEMA)).text

            if type is not None and target is not None:
                result.append((type, target))

        return result

    def get_xml(self, file_name):
        return open(os.path.join(self.synoptics_path, file_name), "r").read()

    def should_be_ignored(self, type, target):
        return (type == "UNKNOWN" and target == "NONE") or type == "DAE"
