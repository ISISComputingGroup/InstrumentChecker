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

    def test_GIVEN_a_synoptic_xml_with_no_component_type_WHEN_parsed_THEN_raises_value_error(self):
        xml = """<?xml version="1.0" ?>
                    <instrument xmlns="http://www.isis.stfc.ac.uk//instrument">
                        <name>He_Level_Meter</name>
                        <components>
                            <component>
                                <name>Helium Level Meter</name>
                                <target>
                                    <name>HLG</name>
                                </target>
                                <pvs/>
                                <components/>
                            </component>
                        </components>
                    </instrument>
                    """

        # Assert that an appropriate exception is raised
        with self.assertRaises(ValueError) as cm:
            self.synoptic_utils.get_type_target_pairs(xml)

        # Assert that the exception contains some kind of useful information
        self.assertIn("Helium Level Meter", cm.exception.message)
        self.assertIn("HLG", cm.exception.message)

    def test_GIVEN_a_synoptic_xml_with_no_target_name_WHEN_parsed_THEN_it_is_ignored(self):
        xml = """<?xml version="1.0" ?>
                    <instrument xmlns="http://www.isis.stfc.ac.uk//instrument">
                        <name>He_Level_Meter</name>
                        <components>
                            <component>
                                <name>Helium Level Meter</name>
                                <type>HE_LEVEL_GAUGE</type>
                                <pvs/>
                                <components/>
                            </component>
                        </components>
                    </instrument>
                    """

        self.assertListEqual(self.synoptic_utils.get_type_target_pairs(xml), [])
