import unittest
import concurrent.futures
from util.channel_access import ChannelAccessUtils
from tests.settings import Settings

MAX_CONTROLLER = 16
MAX_MOTOR = 8


class MotorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ca = ChannelAccessUtils(Settings.pv_prefix)

    def test_beckhoffs_have_nonzero_delay(self) -> None:
        """
        Beckhoff axes must have a non-zero motor record delay set in order to reliably perform retargeted moves.

        Generally .DLY must be set to something around 0.5s for reliable moves on virtual axes, for real axes
        0.2s may be sufficient.

        This test ensures that .DLY is not set to zero (the motor record default) for any beckhoff axes.
        """
        def check_nonzero_delay(controller, motor) -> str | None:
            prefix = f"MOT:MTR{controller:02d}{motor:02d}"
            controller_type = self.ca.get_value(f"{prefix}_IOCNAME")

            if controller_type is not None and controller_type.startswith("TC_"):
                delay = self.ca.get_value(f"{prefix}.DLY")
                if delay == 0:
                    return f"Delay is zero on Beckhoff axis {self.ca.pv_prefix}{prefix}"

            return None

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_MOTOR * MAX_CONTROLLER) as executor:
            futures = []
            for controller in range(1, MAX_CONTROLLER+1):
                for motor in range(1, MAX_MOTOR+1):
                    futures.append(executor.submit(check_nonzero_delay, controller, motor))

            for fut in concurrent.futures.as_completed(futures):
                result = fut.result()
                with self.subTest():
                    self.assertIsNone(result)
