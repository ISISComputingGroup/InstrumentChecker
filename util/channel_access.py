import binascii
import json
import zlib
from builtins import object
from enum import Enum

from genie_python.channel_access_exceptions import ReadAccessException, UnableToConnectToPVException
from genie_python.genie_cachannel_wrapper import CaChannelWrapper

# Some instruments may not be available. If this is the case, we don't want to wait too long for the response which
# will never come (which would slow down the tests)
CHANNEL_ACCESS_TIMEOUT = 5


class ChannelAccessUtils(object):
    """
    Class containing utility methods for interacting with a PV
    """

    def __init__(self, pv_prefix=""):
        self.pv_prefix = pv_prefix

    def get_value(self, pv):
        """
        Gets the value of the PV. Returns None if PV is unavailable.
        :return: The PV value as a string, or None if there was an error
        """
        try:
            return CaChannelWrapper.get_pv_value(
                "{}{}".format(
                    self.pv_prefix,
                    pv,
                ),
                timeout=CHANNEL_ACCESS_TIMEOUT,
            )
        except (UnableToConnectToPVException, ReadAccessException):
            return None

    @staticmethod
    def _dehex_and_decompress(data):
        """
        Converts the raw data from a PV to a decompressed string.
        :param data: The raw data from the PV. It is a string of numbers representing the bytes of the raw data of the
        PV.
        :return: The data of the PV in the form of a decompressed and decoded string.
        """
        return zlib.decompress(binascii.unhexlify(data))

    def get_inst_list(self):
        """
        Gets a list with all instruments running on IBEX from CS:INSTLIST.
        :return: a list of strings of instrument names.
        """
        pv_value = self.get_value("CS:INSTLIST")
        return {} if pv_value is None else json.loads(self._dehex_and_decompress(pv_value))

    def get_interesting_pvs(self):
        """
        Returns all PVs with high or medium interest status from the corresponding instrument PV. The
        instrument for which it returns the list depends on the prefix assigned to this class, which needs to be in the
        format IN:NAME_OF_INSTRUMENT.
        :return: A python set with the names of all the PVs with a high or medium interest status.
        """
        all_interesting_pvs = (
            self._get_pvs_by_interesting_level(PvInterestingLevel.HIGH)
            + self._get_pvs_by_interesting_level(PvInterestingLevel.MEDIUM)
            + self._get_pvs_by_interesting_level(PvInterestingLevel.LOW)
            + self._get_pvs_by_interesting_level(PvInterestingLevel.FACILITY)
        )
        interesting_pvs = {pv for pv in all_interesting_pvs}

        return interesting_pvs

    def _get_pvs_by_interesting_level(self, interesting_level):
        """
        Returns the list of all PVs with the specified interesting level from the corresponding instrument PV. The
        instrument for which it returns the list depends on the prefix assigned to this class, which needs to be in the
        format IN:NAME_OF_INSTRUMENT.
        :param interesting_level An enum type representing the interesting level of a PV.
        :return: A python list with the names of all the PVs with the specified interesting level.
        """

        pv_value = self.get_value("CS:BLOCKSERVER:PVS:INTEREST:" + interesting_level.value)
        if pv_value is None:
            return []
        else:
            interesting_pvs = json.loads(self._dehex_and_decompress(pv_value))
            pv_names = [pv[0] for pv in interesting_pvs]

            return pv_names

    def get_valid_iocs(self):
        """
        Gets the names of all valid IOCS from the PV of IOCs of the instrument.
        :return: a list of strings representing IOC names.
        """
        pv_value = self.get_value("CS:BLOCKSERVER:IOCS")
        return None if pv_value is None else json.loads(self._dehex_and_decompress(pv_value)).keys()

    def get_protected_iocs(self):
        """
        Gets the names of all protected IOCS from the PV of IOCs of the instrument. Protected IOCs are IOCs that a user
        is not allowed to stop.
        :return: a list of strings representing IOC names.
        """
        pv_value = self.get_value("CS:BLOCKSERVER:IOCS_NOT_TO_STOP")
        return None if pv_value is None else json.loads(self._dehex_and_decompress(pv_value))

    def get_version_string(self):
        """
        Gets the version of IBEX server running.
        :return: a compressed and hex encoded string representing the version.
        """
        return self.get_value("CS:VERSION:SVN:REV")


class PvInterestingLevel(Enum):
    """
    Enumerated type representing the possible interesting levels a PV can have.
    """

    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    FACILITY = "FACILITY"
