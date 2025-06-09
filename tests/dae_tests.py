import unittest

from tests.settings import Settings
from util.channel_access import ChannelAccessUtils


class DaeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ca = ChannelAccessUtils(Settings.pv_prefix)

    def test_dae_run_number_digits_suffecient(self) -> None:
        """
        Check if the current run number is close to exceeding the available number of digits.

        We define the number of digits in the run number in C:\Instrument\Settings\labview modules\dae\icp_config.xml
        It is easier to simply access the current run number and check the nuber of digits in against the current number
        than to check this xml.
        """
        failure_threshold_percent = 90
        current_run_number = self.ca.get_value("DAE:RUNNUMBER")
        assert isinstance(current_run_number, str)

        # current_run_number will be none if instrument off
        if current_run_number is None:
            self.skipTest("No run number, likely instrument is off")

        with self.subTest():
            self.assertGreater(
                failure_threshold_percent / 100 * (10 ** len(current_run_number)),
                int(current_run_number),
                f"The current run number is within {failure_threshold_percent}% ({100 * int(current_run_number) / (10 ** len(current_run_number)):.1f}%)of the maximum run number",
            )
