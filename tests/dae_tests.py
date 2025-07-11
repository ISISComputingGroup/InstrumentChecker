import unittest

from tests.settings import Settings
from util.channel_access import ChannelAccessUtils


class DaeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ca = ChannelAccessUtils(Settings.pv_prefix)

    def test_dae_run_number_digits_sufficient(self) -> None:
        """
        Check if the current run number is close to exceeding the available number of digits.

        We define the number of digits in the run number in C:\Instrument\Settings\labview modules\dae\icp_config.xml
        It is easier to simply access the current run number and check the nuber of digits in against the current number
        than to check this xml.
        """
        if Settings.name == "GEM":
            failure_threshold_percent = 99.5
        else:
            failure_threshold_percent = 90
        current_run_number = self.ca.get_value("DAE:RUNNUMBER")
        # current_run_number will be none if instrument off
        if current_run_number is None:
            self.skipTest("No run number, likely instrument is off")
        assert isinstance(current_run_number, str)

        self.assertGreater(
            failure_threshold_percent / 100 * (10 ** len(current_run_number)),
            int(current_run_number),
            f"The current run number is within {failure_threshold_percent}% ({100 * int(current_run_number) / (10 ** len(current_run_number)):.1f}%)of the maximum run number",
        )
