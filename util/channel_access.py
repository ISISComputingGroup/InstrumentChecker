import json
import zlib
from genie_python.genie_cachannel_wrapper import CaChannelWrapper
from genie_python.channel_access_exceptions import UnableToConnectToPVException, ReadAccessException


class ChannelAccessUtils(object):
    """
    Class containing utility methods for interacting with a PV
    """

    def __init__(self, pv_prefix):
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
        return zlib.decompress(data.decode('hex'))

    def get_inst_list(self):
        pv_value = self.get_value("CS:INSTLIST")
        return None if pv_value is None else json.loads(self._dehex_and_decompress(pv_value))

    def get_valid_iocs(self):
        pv_value = self.get_value("CS:BLOCKSERVER:IOCS")
        return None if pv_value is None else json.loads(self._dehex_and_decompress(pv_value)).keys()

    def get_protected_iocs(self):
        pv_value = self.get_value("CS:BLOCKSERVER:IOCS_NOT_TO_STOP")
        return None if pv_value is None else json.loads(self._dehex_and_decompress(pv_value))

    def get_version_string(self):
        return self.get_value("CS:VERSION:SVN:REV")
