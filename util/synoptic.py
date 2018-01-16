import xml.etree.ElementTree as ET
import os


class SynopticUtils(object):
    """
    Utility methods for interacting with a synoptic.
    """

    SCHEMA = "{http://www.isis.stfc.ac.uk//instrument}"

    def __init__(self, config_repo_path):
        self.synoptics_path = os.path.join(config_repo_path, "configurations", "synoptics")

    def _prefix_schema(self, tag):
        return "{schema}{tag}".format(schema=SynopticUtils.SCHEMA, tag=tag)

    def get_synoptics_filenames(self):
        return [f for f in os.listdir(self.synoptics_path) if f.endswith(".xml")]

    def get_type_target_pairs(self, synoptic_xml):
        """
        Returns a set of type, target pairs used in this synoptic
        :param synoptic_xml: the string version of the xml
        """

        root = ET.fromstring(synoptic_xml)
        result = []

        for component in root.iter(self._prefix_schema("component")):
            type = component.find("./{}".format(self._prefix_schema("type")))
            target = component.find("./{}/{}".format(self._prefix_schema("target"), self._prefix_schema("name")))

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
        with open(os.path.join(self.synoptics_path, file_name)) as f:
            return f.read()

    def type_should_be_ignored(self, type):
        return type in ["UNKNOWN", "DAE"]

    def target_should_be_ignored(self, target):
        return target == "NONE"

    def get_pv_addresses(self, synoptic_xml):
        names_with_no_address = list()
        valid_addresses = dict()

        for pv in ET.fromstring(synoptic_xml).iter(self._prefix_schema("pv")):
            address = pv.find(self._prefix_schema("address")).text
            name = pv.find(self._prefix_schema("displayname")).text
            if address is None:
                names_with_no_address.append(name)
            else:
                valid_addresses[name] = address

        if len(names_with_no_address) > 0:
            msg = "The synoptic contains PVs with no associated address:\n    " + "\n    ".join(names_with_no_address)
            raise ValueError(msg)

        return valid_addresses
