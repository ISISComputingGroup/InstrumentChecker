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
