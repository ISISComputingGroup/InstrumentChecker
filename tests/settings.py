from util.channel_access import ChannelAccessUtils


class Settings(object):
    """
    Class that holds settings for each test suite to use, for example which instrument is currently being tested

    Should be used in a static way only.

    These variables are set from the main test runner and read from the test classes when the tests run.
    """

    name = ""
    hostname = ""
    config_repo_path = ""
    gui_repo_path = ""
    pv_prefix = ""
    valid_iocs = None
    protected_iocs = None

    def __init__(self):
        raise RuntimeError("Do not create an instance of this class.")

    @staticmethod
    def set_instrument(name, hostname, pv_prefix):
        Settings.name = name
        Settings.hostname = hostname
        Settings.pv_prefix = pv_prefix

        ca = ChannelAccessUtils(pv_prefix)
        Settings.valid_iocs = ca.get_valid_iocs()
        Settings.protected_iocs = ca.get_protected_iocs()

    @staticmethod
    def set_repo_paths(config_repo_path, gui_repo_path):
        Settings.config_repo_path = config_repo_path
        Settings.gui_repo_path = gui_repo_path
