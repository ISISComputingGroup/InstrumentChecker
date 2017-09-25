import json
import zlib
from genie_python.genie_cachannel_wrapper import CaChannelWrapper


class ChannelAccessUtils(object):
    """
    Class containing utility methods for interacting with a PV
    """

    def __init__(self, pv):
        self.pv = pv

    def get_value(self):
        return CaChannelWrapper.get_pv_value(self.pv, to_string=True)

    def _dehex_and_decompress(self, data):
        return zlib.decompress(data.decode('hex'))

    def get_from_compressed_json(self):
        return json.loads(self._dehex_and_decompress(self.get_value()))
