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
            type = component.find("./{schema}type".format(schema=SynopticUtils.SCHEMA))
            target = component.find("./{schema}target/{schema}name".format(schema=SynopticUtils.SCHEMA))

            if target is None and type is not None:
                # This is allowed but should be ignored
                continue

            if type is not None:
                result.append((type.text, target.text))
            else:
                message = "Couldn't find ./type or ./target/name in component.".format()

                name = component.find("./{schema}name".format(schema=SynopticUtils.SCHEMA))
                if name is not None:
                    message += "\n Component name is: {}".format(name.text)
                else:
                    message += "\n Component name could not be extracted."

                if type is not None:
                    message += "\n Component type is: {}".format(type.text)
                else:
                    message += "\n Component type could not be extracted."

                # Target name is already guaranteed not to be None
                message += "\n Component target name is: {}".format(target.text)

                raise ValueError(message)

        return result

    def get_xml(self, file_name):
        return open(os.path.join(self.synoptics_path, file_name), "r").read()

    def should_be_ignored(self, type, target):
        return (type == "UNKNOWN" and target == "NONE") or type == "DAE"
