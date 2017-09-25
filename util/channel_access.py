import json


class ChannelAccessUtils(object):
    """
    Class containing utility methods for interacting with channel access
    """

    @staticmethod
    def _get_instlist_pv():
        return """
        [
            {"name": "LARMOR", "hostName": "NDXLARMOR", "pvPrefix": "IN:LARMOR:"},
            {"name": "DEMO", "hostName": "NDXDEMO", "pvPrefix": "IN:DEMO:"},
            {"name": "IRIS", "hostName": "NDXIRIS", "pvPrefix": "IN:IRIS:"}
        ]"""

    @staticmethod
    def get_instlist():
        return json.loads(ChannelAccessUtils._get_instlist_pv())
