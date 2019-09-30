import unittest

from util.channel_access import PvInterestingLevel, ChannelAccessUtils


class ChannelAccessTests(unittest.TestCase):

    def setUp(self):
        def mock_get_value(pv):
            if pv == 'CS:BLOCKSERVER:PVS:INTEREST:HIGH':
                return """[["IN:DEMO:WM323_02:SPEED", "longin", "Current pump speed", "WM323_02"],\
                ["IN:DEMO:WM323_02:STATUS", "bi", "Pump running status", "WM323_02"]]"""
            elif pv == 'CS:BLOCKSERVER:PVS:INTEREST:MEDIUM':
                return """[["IN:DEMO:ALDN1000_01:PROGRAM:FUNCTION", "mbbi", "Pumping Program Phase's function",\
                "ALDN1000_01"], ["IN:DEMO:ALDN1000_01:VOLUME:INF:CLEAR:SP", "bo",\
                 "Set infused volume dispensed to 0.0", "ALDN1000_01"]]"""
            elif pv == 'CS:BLOCKSERVER:PVS:INTEREST:LOW':
                return """[["IN:DEMO:ALDN1000_01:VOLUME:WDR:CLEAR:SP", "bo", "Set withdrawn volume dispensed to 0.0",\
                "ALDN1000_01"], ["IN:DEMO:AMINT2L_01:RANGE:ERROR", "mbbi", "Error in pressure readback",\
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
                             ["IN:DEMO:WM323_02:SPEED", "IN:DEMO:WM323_02:STATUS"])

    def test_GIVEN_interesting_level_WHEN_medium_THEN_correct_medium_pvs_returned(self):
        self.assertListEqual(self.channel_access._get_pvs_by_interesting_level(PvInterestingLevel.MEDIUM),
                             ["IN:DEMO:ALDN1000_01:PROGRAM:FUNCTION", "IN:DEMO:ALDN1000_01:VOLUME:INF:CLEAR:SP"])

    def test_GIVEN_interesting_level_WHEN_low_THEN_correct_low_pvs_returned(self):
        self.assertListEqual(self.channel_access._get_pvs_by_interesting_level(PvInterestingLevel.LOW),
                             ["IN:DEMO:ALDN1000_01:VOLUME:WDR:CLEAR:SP", "IN:DEMO:AMINT2L_01:RANGE:ERROR"])
