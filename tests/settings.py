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
        raise NotImplementedError("Do not create an instance of this class.")
