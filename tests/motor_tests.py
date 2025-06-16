import concurrent.futures
import unittest

from tests.settings import Settings
from util.channel_access import ChannelAccessUtils

MAX_CONTROLLER = 16
MAX_MOTOR = 8


class MotorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ca = ChannelAccessUtils(Settings.pv_prefix)

    def test_beckhoffs_have_nonzero_delay(self) -> None:
        """
        Beckhoff axes must have a non-zero motor record delay set in order to reliably perform retargeted moves.

        Generally an appropriate .DLY is 0.25 seconds, which is just a little bit longer than one beckhoff poll period
        which is 0.2s.

        This test ensures that .DLY is not set to zero (the motor record default) for any beckhoff axes.
        """

        def check_nonzero_delay(controller, motor) -> str | None:
            prefix = f"MOT:MTR{controller:02d}{motor:02d}"
            controller_type = self.ca.get_value(f"{prefix}_IOCNAME", timeout=30)

            if controller_type is not None and controller_type.startswith("TC_"):
                delay = self.ca.get_value(f"{prefix}.DLY", timeout=30)
                if delay == 0:
                    return f"Delay is zero on Beckhoff axis {self.ca.pv_prefix}{prefix}"

            return None

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=MAX_MOTOR * MAX_CONTROLLER
        ) as executor:
            futures = []
            for controller in range(1, MAX_CONTROLLER + 1):
                for motor in range(1, MAX_MOTOR + 1):
                    futures.append(executor.submit(check_nonzero_delay, controller, motor))

            for fut in concurrent.futures.as_completed(futures):
                result = fut.result()
                with self.subTest():
                    self.assertIsNone(result)

    def test_galils_have_nonzero_encoder_sync_tolerance(self) -> None:
        """
        Closed-loop galil axes must have a non-zero motor-encoder sync tolerance set.

        This only applies to closed-loop axes; it is not meaningful for open-loop axes.

        Generally an appropriate _MOT_ENC_SYNC_TOL_SP is ~ERES, this will cause motor and encoder
        to resync before a move if they differ by more than one encoder step.

        This test ensures that ._MOT_ENC_SYNC_TOL_SP is not set to zero
        for any closed-loop galil axes.
        """

        def check_nonzero_mot_enc_sync_tol(controller, motor) -> str | None:
            prefix = f"MOT:MTR{controller:02d}{motor:02d}"
            controller_type = self.ca.get_value(f"{prefix}_IOCNAME", timeout=30)

            if controller_type is not None and controller_type.startswith("GALIL_"):
                mot_enc_sync_tol = self.ca.get_value(f"{prefix}_MOT_ENC_SYNC_TOL_SP", timeout=30)
                ueip = self.ca.get_value(f"{prefix}.UEIP", timeout=30)
                if ueip and mot_enc_sync_tol == 0:
                    return f"Motor-encoder sync tolerance is zero on closed-loop axis {self.ca.pv_prefix}{prefix}"

            return None

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=MAX_MOTOR * MAX_CONTROLLER
        ) as executor:
            futures = []
            for controller in range(1, MAX_CONTROLLER + 1):
                for motor in range(1, MAX_MOTOR + 1):
                    futures.append(
                        executor.submit(check_nonzero_mot_enc_sync_tol, controller, motor)
                    )

            for fut in concurrent.futures.as_completed(futures):
                result = fut.result()
                with self.subTest():
                    self.assertIsNone(result)
