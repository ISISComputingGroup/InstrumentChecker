import binascii
import json
import unittest
import zlib

from tests.settings import Settings
from util.channel_access import ChannelAccessUtils
from util.common import skip_on_instruments


class GuiTests(unittest.TestCase):
    def setUp(self):
        self.ca = ChannelAccessUtils(Settings.pv_prefix)

    @skip_on_instruments(["HRPD", "EMMA-A", "EMMA-B"], "These instruments use a streaming DAE")
    @skip_on_instruments(
        [
            "CRYOLAB_R80",
            "DCLAB",
            "DETMON",
            "HYDROGEN1",
            "HYDROGEN2",
            "IBEXGUITEST",
            "MOTION",
            "SCIDEMO",
            "SELAB",
            "SELAB2",
            "SOFTMAT",
        ],
        "Lab/test machines without a DAE at all",
    )
    def test_GIVEN_streaming_dae_perspective_exists_THEN_it_is_set_to_not_shown_on_instruments_which_dont_use_a_streaming_dae(
        self,
    ):
        raw_value = self.ca.get_value("CS:PERSP:SETTINGS")
        assert isinstance(raw_value, str | None)
        if raw_value is None or raw_value == "":
            self.skipTest("Instrument is unavailable")

        version = self.ca.get_version_string()
        if version is None or version == "":
            self.skipTest("Instrument is unavailable")

        version_major = int(version.split(".")[0])
        version_minor = int(version.split(".")[1])

        if (version_major, version_minor) < (26, 8):
            self.skipTest("Instrument is on a version without streaming DAE perspective")

        perspectives = json.loads(zlib.decompress(binascii.unhexlify(raw_value.encode("ascii"))))

        self.assertFalse(
            perspectives.get(
                "uk.ac.stfc.isis.ibex.client.e4.product.perspective.streamingdae", True
            )
        )
