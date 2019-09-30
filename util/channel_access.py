import json
import zlib

from enum import Enum
from genie_python.genie_cachannel_wrapper import CaChannelWrapper
from genie_python.channel_access_exceptions import UnableToConnectToPVException, ReadAccessException


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
            return CaChannelWrapper.get_pv_value("{}{}".format(self.pv_prefix, pv, to_string=True))
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
        return zlib.decompress(data.decode('hex'))

    def get_inst_list(self):
        pv_value = self.get_value("CS:INSTLIST")
        return {} if pv_value is None else json.loads(self._dehex_and_decompress(pv_value))

    def get_interesting_pvs(self):
        """
        Returns the list of all PVs with high or medium interest status from the corresponding instrument PV. The
        instrument for which it returns the list depends on the prefix assigned to this class, which needs to be in the
        format IN:NAME_OF_INSTRUMENT.
        :return: A python dictionary with the names of all the PVs with a high or medium interest status. The key
        pointing to a PV name is the hash code of the string name.
        """
        interesting_pvs = set()

        # We just need a set
        for pv in self._get_pvs_by_interesting_level(PvInterestingLevel.HIGH):
            interesting_pvs.add(pv)

        for pv in self._get_pvs_by_interesting_level(PvInterestingLevel.MEDIUM):
            interesting_pvs.add(pv)

        for pv in self._get_pvs_by_interesting_level(PvInterestingLevel.LOW):
            interesting_pvs.add(pv)

        # print('Number of interesting PVs: ' + str(len(interesting_pvs)))
        return interesting_pvs

    def _get_pvs_by_interesting_level(self, interesting_level):
        """
        Returns the list of all PVs with the specified interesting level from the corresponding instrument PV. The
        instrument for which it returns the list depends on the prefix assigned to this class, which needs to be in the
        format IN:NAME_OF_INSTRUMENT.
        :param interesting_level An enum type representing the interesting level of a PV.
        :return: A python list with the names of all the PVs with the specified interesting level.
        """
        if interesting_level == PvInterestingLevel.HIGH:
            pv_value = self.get_value('CS:BLOCKSERVER:PVS:INTEREST:HIGH')
        elif interesting_level == PvInterestingLevel.MEDIUM:
            pv_value = self.get_value('CS:BLOCKSERVER:PVS:INTEREST:MEDIUM')
        else:
            pv_value = self.get_value('CS:BLOCKSERVER:PVS:INTEREST:LOW')

        if pv_value is None:
            return []
        else:
            interesting_pvs = json.loads(self._dehex_and_decompress(pv_value))
            pv_names = []
            for pv in interesting_pvs:
                pv_names.append(pv[0])

            return pv_names

    def get_valid_iocs(self):
        pv_value = self.get_value("CS:BLOCKSERVER:IOCS")
        # self._get_pvs_by_interesting_level(PvInterestingLevel.HIGH)
        return None if pv_value is None else json.loads(self._dehex_and_decompress(pv_value)).keys()

    def get_protected_iocs(self):
        pv_value = self.get_value("CS:BLOCKSERVER:IOCS_NOT_TO_STOP")
        return None if pv_value is None else json.loads(self._dehex_and_decompress(pv_value))

    def get_version_string(self):
        return self.get_value("CS:VERSION:SVN:REV")


class PvInterestingLevel(Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
