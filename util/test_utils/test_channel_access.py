import unittest

from util.channel_access import PvInterestingLevel, ChannelAccessUtils


class ChannelAccessTests(unittest.TestCase):

    def setUp(self):
        def mock_get_value(pv):
            if pv == 'CS:BLOCKSERVER:PVS:INTEREST:HIGH':
                return """[["IN:DEMO:PV_HIGH_INTEREST_1", "longin", "Current pump speed", "WM323_02"],\
                ["IN:DEMO:PV_HIGH_INTEREST_2", "bi", "Pump running status", "WM323_02"]]"""
            elif pv == 'CS:BLOCKSERVER:PVS:INTEREST:MEDIUM':
                return """[["IN:DEMO:PV_MEDIUM_INTEREST_1", "mbbi", "Pumping Program Phase's function",\
                "ALDN1000_01"], ["IN:DEMO:PV_MEDIUM_INTEREST_2", "bo",\
                "Set infused volume dispensed to 0.0", "ALDN1000_01"]]"""
            elif pv == 'CS:BLOCKSERVER:PVS:INTEREST:LOW':
                return """[["IN:DEMO:PV_LOW_INTEREST_1", "bo", "Set withdrawn volume dispensed to 0.0",\
                "ALDN1000_01"], ["IN:DEMO:PV_LOW_INTEREST_2", "mbbi", "Error in pressure readback",\
                "AMINT2L_01"]]"""
            else:
                raise ValueError('pv argument needs to be HIGH, MEDIUM or LOW instrument PV for list of pvs by '
                                 'interesting level')

        def mock_dehex_and_decompress(data):
            return data

        self.channel_access = ChannelAccessUtils()
        self.channel_access.get_value = mock_get_value
        self.channel_access._dehex_and_decompress = mock_dehex_and_decompress

    def test_GIVEN_interesting_level_WHEN_disconnected_pv_THEN_empty_list_returned(self):
        def mock_get_value_none(pv):
            return None

        self.channel_access.get_value = mock_get_value_none
        self.assertListEqual(self.channel_access._get_pvs_by_interesting_level(PvInterestingLevel.HIGH), [])

    def test_GIVEN_interesting_level_WHEN_high_THEN_correct_high_pvs_returned(self):
        self.assertListEqual(self.channel_access._get_pvs_by_interesting_level(PvInterestingLevel.HIGH),
                             ["IN:DEMO:PV_HIGH_INTEREST_1", "IN:DEMO:PV_HIGH_INTEREST_2"])

    def test_GIVEN_interesting_level_WHEN_medium_THEN_correct_medium_pvs_returned(self):
        self.assertListEqual(self.channel_access._get_pvs_by_interesting_level(PvInterestingLevel.MEDIUM),
                             ["IN:DEMO:PV_MEDIUM_INTEREST_1", "IN:DEMO:PV_MEDIUM_INTEREST_2"])

    def test_GIVEN_interesting_level_WHEN_low_THEN_correct_low_pvs_returned(self):
        self.assertListEqual(self.channel_access._get_pvs_by_interesting_level(PvInterestingLevel.LOW),
                             ["IN:DEMO:PV_LOW_INTEREST_1", "IN:DEMO:PV_LOW_INTEREST_2"])
