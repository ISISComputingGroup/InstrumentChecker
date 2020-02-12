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
        self.assertIn("Helium Level Meter", str(cm.exception))
        self.assertIn("HLG", str(cm.exception))

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

    def test_GIVEN_a_synoptic_xml_with_pv_address_WHEN_parsed_THEN_name_and_address_identified_as_in_XML(self):
        name = "Test PV"
        address = "TE:PV:1"
        xml = """<?xml version="1.0" ?>
                    <instrument xmlns="http://www.isis.stfc.ac.uk//instrument">
                        <name>Name</name>
                        <components>
                            <component>
                                <name>Name</name>
                                <type>HE_LEVEL_GAUGE</type>
                                <target>
                                    <name>HLG</name>
                                </target>
                                <pvs>
                                    <pv>
                                        <displayname>{name}</displayname>
                                        <address>{address}</address>
                                    </pv>
                                </pvs>
                            </component>
                        </components>
                    </instrument>
                    """.format(name=name, address=address)

        expected_pvs = {name: address}
        self.assertEqual(expected_pvs, self.synoptic_utils.get_pv_addresses(xml))

    def test_GIVEN_a_synoptic_xml_with_empty_pv_address_WHEN_parsed_THEN_name_matches_xml_address_is_none(self):
        name = "Test PV"
        xml = """<?xml version="1.0" ?>
                    <instrument xmlns="http://www.isis.stfc.ac.uk//instrument">
                        <name>Name</name>
                        <components>
                            <component>
                                <name>Name</name>
                                <type>HE_LEVEL_GAUGE</type>
                                <target>
                                    <name>HLG</name>
                                </target>
                                <pvs>
                                    <pv>
                                        <displayname>{name}</displayname>
                                        <address/>
                                    </pv>
                                </pvs>
                            </component>
                        </components>
                    </instrument>
                    """.format(name=name)

        expected_pvs = {name: None}
        self.assertEqual(expected_pvs, self.synoptic_utils.get_pv_addresses(xml))

    def test_GIVEN_a_synoptic_xml_with_a_mix_of_undefined_and_defined_pv_addresses_WHEN_parsed_THEN_extracted_names_and_addresses_match_XML_input(self):

        name_1 = "Test PV 1"
        address_1 = "TE:PV:1"
        name_2 = "Test PV 2"
        address_2 = "TE:PV:2"
        name_3 = "Test PV 3"

        xml = """<?xml version="1.0" ?>
                    <instrument xmlns="http://www.isis.stfc.ac.uk//instrument">
                        <name>Name</name>
                        <components>
                            <component>
                                <name>Name</name>
                                <type>HE_LEVEL_GAUGE</type>
                                <target>
                                    <name>HLG</name>
                                </target>
                                <pvs>
                                    <pv>
                                        <displayname>{name_1}</displayname>
                                        <address>{address_1}</address>
                                    </pv>
                                    <pv>
                                        <displayname>{name_2}</displayname>
                                        <address>{address_2}</address>
                                    </pv>
                                    <pv>
                                        <displayname>{name_3}</displayname>
                                        <address/>
                                    </pv>
                                </pvs>
                            </component>
                        </components>
                    </instrument>
                    """.format(name_1=name_1, address_1=address_1, name_2=name_2, address_2=address_2, name_3=name_3)

        expected_pvs = {name_1: address_1, name_2: address_2, name_3: None}
        self.assertEqual(expected_pvs, self.synoptic_utils.get_pv_addresses(xml))
