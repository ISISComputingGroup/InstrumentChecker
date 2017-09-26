from util.synoptic import SynopticUtils
import unittest


class SynopticTests(unittest.TestCase):

    def setUp(self):
        self.synoptic_utils = SynopticUtils("")

    def test_GIVEN_a_valid_synoptic_xml_WHEN_parsed_THEN_can_extract_components(self):
        xml = """<?xml version="1.0" ?>
                    <instrument xmlns="http://www.isis.stfc.ac.uk//instrument">
                        <name>He_Level_Meter</name>
                        <components>
                            <component>
                                <name>Helium Level Meter</name>
                                <type>HE_LEVEL_GAUGE</type>
                                <target>
                                    <name>HLG</name>
                                </target>
                                <pvs/>
                                <components/>
                            </component>
                        </components>
                    </instrument>
                    """

        self.assertListEqual(self.synoptic_utils.get_type_target_pairs(xml), [("HE_LEVEL_GAUGE", "HLG")])

    def test_GIVEN_a_valid_synoptic_xml_WHEN_parsed_THEN_can_extract_nested_components(self):
        xml = """<?xml version="1.0" ?>
                    <instrument xmlns="http://www.isis.stfc.ac.uk//instrument">
                        <name>He_Level_Meter</name>
                        <components>
                            <component>
                                <name>Helium Level Meter</name>
                                <type>HE_LEVEL_GAUGE</type>
                                <target>
                                    <name>HLG</name>
                                </target>
                                <pvs/>
                                <components>
                                    <component>
                                        <name>Chopper</name>
                                        <type>CHOPPER</type>
                                        <target>
                                            <name>Mk3 Chopper</name>
                                        </target>
                                        <pvs/>
                                        <components/>
                                    </component>
                                </components>
                            </component>
                        </components>
                    </instrument>
                    """

        self.assertListEqual(self.synoptic_utils.get_type_target_pairs(xml),
                             [("HE_LEVEL_GAUGE", "HLG"), ("CHOPPER", "Mk3 Chopper")])


