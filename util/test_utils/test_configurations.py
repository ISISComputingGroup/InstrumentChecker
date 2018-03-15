from util.configurations import ConfigurationUtils
import unittest


class ConfigurationTests(unittest.TestCase):
    def setUp(self):
        self.config_utils = ConfigurationUtils("")

    def test_GIVEN_ioc_xml_WHEN_parsed_THEN_can_extract_a_single_ioc(self):
        xml = """<?xml version="1.0" ?>
                    <iocs xmlns="http://epics.isis.rl.ac.uk/schema/iocs/1.0" 
                    xmlns:ioc="http://epics.isis.rl.ac.uk/schema/iocs/1.0" xmlns:xi="http://www.w3.org/2001/XInclude">
                        <ioc autostart="true" name="SIMPLE" restart="false" simlevel="none">
                            <macros/>
                            <pvs/>
                            <pvsets/>
                        </ioc>
                    </iocs>
                    """

        self.assertListEqual(self.config_utils.get_iocs(xml), ["SIMPLE"])

    def test_GIVEN_ioc_xml_WHEN_parsed_THEN_can_extract_multiple_iocs(self):
        xml = """<?xml version="1.0" ?>
                    <iocs xmlns="http://epics.isis.rl.ac.uk/schema/iocs/1.0" 
                    xmlns:ioc="http://epics.isis.rl.ac.uk/schema/iocs/1.0" xmlns:xi="http://www.w3.org/2001/XInclude">
                        <ioc autostart="true" name="SIMPLE_01" restart="false" simlevel="none">
                            <macros/>
                            <pvs/>
                            <pvsets/>
                        </ioc>
                        <ioc autostart="true" name="SIMPLE_02" restart="false" simlevel="none">
                            <macros/>
                            <pvs/>
                            <pvsets/>
                        </ioc>
                    </iocs>
                    """

        self.assertListEqual(self.config_utils.get_iocs(xml), ["SIMPLE_01", "SIMPLE_02"])

    def test_GIVEN_ioc_xml_WHEN_macros_requested_for_ioc_that_exists_THEN_macro_information_matches_xml(self):
        name_1 = "macro1"
        value_1_01 = "1"
        value_1_02 = "Hello, world!"

        name_2 = "macro2"
        value_2_01 = "3.45"
        value_2_02 = "0x2a"

        xml = """<?xml version="1.0" ?>
                    <iocs xmlns="http://epics.isis.rl.ac.uk/schema/iocs/1.0" 
                    xmlns:ioc="http://epics.isis.rl.ac.uk/schema/iocs/1.0" xmlns:xi="http://www.w3.org/2001/XInclude">
                        <ioc autostart="true" name="SIMPLE_01" restart="false" simlevel="none">
                            <macros>
                                <macro name="{name_1}" value="{value_1_01}"/>
                                <macro name="{name_2}" value="{value_2_01}"/>
                            </macros>
                            <pvs/>
                            <pvsets/>
                        </ioc>
                        <ioc autostart="true" name="SIMPLE_02" restart="false" simlevel="none">
                            <macros>
                                <macro name="{name_1}" value="{value_1_02}"/>
                                <macro name="{name_2}" value="{value_2_02}"/>
                            </macros>
                            <pvs/>
                            <pvsets/>
                        </ioc>
                    </iocs>
                    """.format(name_1=name_1, name_2=name_2,
                               value_1_01=value_1_01, value_1_02=value_1_02,
                               value_2_01=value_2_01, value_2_02=value_2_02)

        macros_1 = self.config_utils.get_ioc_macros(xml, "SIMPLE_01", "test_config")
        self.assertEqual(macros_1[name_1], value_1_01)
        self.assertEqual(macros_1[name_2], value_2_01)

        macros_2 = self.config_utils.get_ioc_macros(xml, "SIMPLE_02", "test_config")
        self.assertEqual(macros_2[name_1], value_1_02)
        self.assertEqual(macros_2[name_2], value_2_02)

    def test_GIVEN_ioc_xml_WHEN_macros_requested_for_ioc_that_does_not_exist_THEN_returns_no_data(self):

        xml = """<?xml version="1.0" ?>
                    <iocs xmlns="http://epics.isis.rl.ac.uk/schema/iocs/1.0" 
                    xmlns:ioc="http://epics.isis.rl.ac.uk/schema/iocs/1.0" xmlns:xi="http://www.w3.org/2001/XInclude">
                        <ioc autostart="true" name="SIMPLE_01" restart="false" simlevel="none" />
                    </iocs>
                    """

        self.assertEqual(len(self.config_utils.get_ioc_macros(xml, "SIMPL", "test_config").values()), 0)

    def test_GIVEN_ioc_xml_WHEN_simlevel_is_not_none_THEN_returns_false(self):

        xml = """<?xml version="1.0" ?>
                    <iocs xmlns="http://epics.isis.rl.ac.uk/schema/iocs/1.0" 
                    xmlns:ioc="http://epics.isis.rl.ac.uk/schema/iocs/1.0" xmlns:xi="http://www.w3.org/2001/XInclude">
                        <ioc autostart="true" name="SIMPLE_01" restart="false" simlevel="none">
                            <macros/>
                            <pvs/>
                            <pvsets/>
                        </ioc>
                        <ioc autostart="true" name="SIMPLE_02" restart="false" simlevel="none">
                            <macros/>
                            <pvs/>
                            <pvsets/>
                        </ioc>
                    </iocs>
                    """
        self.assertFalse(self.config_utils.get_ioc_in_sim_mode(xml, "SIMPLE_01"))

    def test_GIVEN_ioc_xml_WHEN_simlevel_is_none_THEN_returns_true(self):

        xml = """<?xml version="1.0" ?>
                    <iocs xmlns="http://epics.isis.rl.ac.uk/schema/iocs/1.0" 
                    xmlns:ioc="http://epics.isis.rl.ac.uk/schema/iocs/1.0" xmlns:xi="http://www.w3.org/2001/XInclude">
                        <ioc autostart="true" name="SIMPLE_01" restart="false" simlevel="true">
                            <macros/>
                            <pvs/>
                            <pvsets/>
                        </ioc>
                        <ioc autostart="true" name="SIMPLE_02" restart="false" simlevel="none">
                            <macros/>
                            <pvs/>
                            <pvsets/>
                        </ioc>
                    </iocs>
                    """
        self.assertTrue(self.config_utils.get_ioc_in_sim_mode(xml, "SIMPLE_01"))
