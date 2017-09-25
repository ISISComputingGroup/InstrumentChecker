import json
import os


class CommonUtils(object):
    """
    Class containing utility methods common to several other utilities
    """

    @staticmethod
    def get_directory_contents_as_list(path):
        if os.path.isdir(path):
            return os.listdir(path)
        else:
            return []
