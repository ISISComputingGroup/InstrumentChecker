import json
import zlib
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
            print("{}{}".format(self.pv_prefix, pv, to_string=True))
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

    def _get_high_interest_pvs(self):
        pv_value = self.get_value('CS:BLOCKSERVER:PVS:INTEREST:HIGH')
        if pv_value is None:
            return []
        else:
            pv_value = json.loads(self._dehex_and_decompress(pv_value))
            high_pv_names = []
            for high_pv in pv_value:
                high_pv_names.append(high_pv[0])

            print(high_pv_names)
            return high_pv_names

    def _get_medium_interest_pvs(self):
        pv_value = self.get_value('CS:BLOCKSERVER:PVS:INTEREST:MEDIUM')
        if pv_value is None:
            return []
        else:
            pv_value = json.loads(self._dehex_and_decompress(pv_value))
            medium_pv_names = []
            for medium_pv in pv_value:
                medium_pv_names.append(medium_pv[0])

            print(medium_pv_names)
            return medium_pv_names


    def get_valid_iocs(self):
        pv_value = self.get_value("CS:BLOCKSERVER:IOCS")
        self._get_high_interest_pvs()
        return None if pv_value is None else json.loads(self._dehex_and_decompress(pv_value)).keys()

    def get_protected_iocs(self):
        pv_value = self.get_value("CS:BLOCKSERVER:IOCS_NOT_TO_STOP")
        return None if pv_value is None else json.loads(self._dehex_and_decompress(pv_value))

    def get_version_string(self):
        return self.get_value("CS:VERSION:SVN:REV")
