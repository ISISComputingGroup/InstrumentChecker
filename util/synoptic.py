from __future__ import absolute_import

import os
import xml.etree.ElementTree as ET
from builtins import object

from .common import CommonUtils


class SynopticUtils(object):
    """
    Utility methods for interacting with a synoptic.
    """

    SCHEMA = "{http://www.isis.stfc.ac.uk//instrument}"

    def __init__(self, config_repo_path: str) -> None:
        self.synoptics_path = os.path.join(config_repo_path, "configurations", "synoptics")

    def _prefix_schema(self, tag: str) -> str:
        return "{schema}{tag}".format(schema=SynopticUtils.SCHEMA, tag=tag)

    def get_synoptics_filenames(self) -> list[str]:
        return [
            f
            for f in CommonUtils.get_directory_contents_as_list(self.synoptics_path)
            if f.endswith(".xml")
        ]

    def get_type_target_pairs(self, synoptic_xml: str) -> list[tuple[str, str]]:
        """
        Returns a set of type, target pairs used in this synoptic
        :param synoptic_xml: the string version of the xml
        """

        root = ET.fromstring(synoptic_xml)
        result = []

        for component in root.iter(self._prefix_schema("component")):
            type: ET.Element | None = component.find("./{}".format(self._prefix_schema("type")))
            target: ET.Element | None = component.find(
                "./{}/{}".format(self._prefix_schema("target"), self._prefix_schema("name"))
            )

            if target is None and type is not None:
                # This is allowed but should be ignored
                continue

            if type is not None and target is not None:
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
                assert target is not None
                message += "\n Component target name is: {}".format(target.text)

                raise ValueError(message)

        return result

    def get_xml(self, file_name: str) -> str:
        with open(os.path.join(self.synoptics_path, file_name)) as f:
            return f.read()

    def type_should_be_ignored(self, type: str) -> bool:
        return type in ["UNKNOWN", "DAE", "BEAMSTOP"]

    def target_should_be_ignored(self, target: str) -> bool:
        return target == "NONE"

    def get_pv_addresses(self, synoptic_xml: str) -> dict[str, str]:
        pv_addresses = dict()

        for pv in ET.fromstring(synoptic_xml).iter(self._prefix_schema("pv")):
            address_element: ET.Element | None = pv.find(self._prefix_schema("address"))
            assert address_element is not None
            address = address_element.text
            name_element: ET.Element | None = pv.find(self._prefix_schema("displayname"))
            assert name_element is not None
            name = name_element.text
            pv_addresses[name] = address

        return pv_addresses
