import itertools
import os


class CommonUtils(object):
    """
    Class containing utility methods common to several other utilities
    """
    MOTOR_IOCS = ["{}_{:02d}".format(p, i) for p, i in
                  itertools.product(["GALIL", "MCLENNAN", "LINMOT", "SM300"], range(1, 11))]

    @staticmethod
    def get_directory_contents_as_list(path):
        if os.path.isdir(path):
            return os.listdir(path)
        else:
            return []

    @staticmethod
    def get_folders_in_directory_as_list(path):
        if os.path.isdir(path):
            return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        else:
            return []

    @staticmethod
    def count_files_with_name(path, name):
        """
        Scans the given directory for files with a given name. Returns the number of these files that were found.
        :return:
        """
        return sum(len([f for f in files if f == name]) for _, _, files in os.walk(path))
