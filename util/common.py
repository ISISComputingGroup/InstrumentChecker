import functools
import itertools
import os
import unittest
from builtins import object, range

from tests.settings import Settings


class CommonUtils(object):
    """
    Class containing utility methods common to several other utilities
    """

    MOTOR_IOCS = [
        "{}_{:02d}".format(p, i)
        for p, i in itertools.product(["GALIL", "MCLENNAN", "LINMOT", "SM300"], range(1, 11))
    ]

    @staticmethod
    def get_directory_contents_as_list(path):
        if os.path.isdir(path):
            return os.listdir(path)
        else:
            raise IOError("Path '{}' is not a directory.".format(path))

    @staticmethod
    def get_folders_in_directory_as_list(path):
        if os.path.isdir(path):
            return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        else:
            raise IOError("Path '{}' is not a directory.".format(path))

    @staticmethod
    def count_files_with_name(path, name):
        """
        Scans the given directory for files with a given name. Returns the number of these files that were found.
        :return:
        """
        if not os.path.isdir(path):
            raise IOError("Path '{}' is not a directory.".format(path))
        return sum(len([f for f in files if f == name]) for _, _, files in os.walk(path))


def skip_on_instruments(instruments_to_skip, skip_reason):
    """
    Decorator to skip a given test on the provided list of instruments

    Usage:

    @skip_on_instruments(["DEMO"], "Demo does not foo the bar correctly")
    def test_xyz(self):
        ...
    """

    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            if Settings.name in instruments_to_skip:
                raise unittest.SkipTest(skip_reason)
            else:
                return func(*args, **kwargs)

        return _wrapper

    return _decorator
