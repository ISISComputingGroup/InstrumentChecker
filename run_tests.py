import os
import sys
import unittest
from xmlrunner import XMLTestRunner
import argparse

from tests.configuration_tests import ConfigurationsTests, ConfigurationsSingleTests
from tests.component_tests import ComponentsTests, ComponentsSingleTests
from tests.globals_tests import GlobalsTests
from tests.scripting_directory_tests import ScriptingDirectoryTests
from tests.synoptic_tests import SynopticTests
from tests.version_tests import VersionTests
from tests.settings import Settings

from util.channel_access import ChannelAccessUtils
from util.configurations import ConfigurationUtils, ComponentUtils
from util.git_wrapper import GitUtils
from util.synoptic import SynopticUtils


def run_tests(inst_name):
    """
    Runs the test suite
    :param inst_name: The name of the instrument to run tests on,
                    used to sort the test reports folder into instrument-specific reports
    :return: True if the tests passed, false otherwise
    """
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    suite.addTests(loader.loadTestsFromTestCase(ScriptingDirectoryTests))
    suite.addTests(loader.loadTestsFromTestCase(GlobalsTests))
    suite.addTests(loader.loadTestsFromTestCase(VersionTests))
    suite.addTests(loader.loadTestsFromTestCase(ConfigurationsSingleTests))
    suite.addTests(loader.loadTestsFromTestCase(ComponentsSingleTests))

    # Add configs test suite a dynamic number of times with an argument of the config name.
    # unittest's test loader is unable to take arguments to test classes by default so have
    # to use the getTestCaseNames() syntax and explicitly add the argument ourselves.
    for config in ConfigurationUtils(configs_repo_path).get_configurations_as_list():
        suite.addTests([ConfigurationsTests(test, config) for test in loader.getTestCaseNames(ConfigurationsTests)])

    for component in ComponentUtils(configs_repo_path).get_configurations_as_list():
        suite.addTests([ComponentsTests(test, component) for test in loader.getTestCaseNames(ComponentsTests)])

    for synoptic in SynopticUtils(configs_repo_path).get_synoptics_filenames():
        suite.addTests([SynopticTests(test, synoptic) for test in loader.getTestCaseNames(SynopticTests)])

    return XMLTestRunner(output=str(os.path.join(reports_path, inst_name)), stream=sys.stdout).run(suite).wasSuccessful()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description="""Runs tests against the configuration repositories on instruments.
                                            Note: all repositories used by this script will be forcibly cleaned and 
                                            reset while the tests are running.
                                            Do not point this script at any repository where you have changes you want 
                                            to keep!""")

    parser.add_argument("--configs_repo_path", required=True, type=str,
                        help="The path to the configurations repository.")
    parser.add_argument("--gui_repo_path", required=True, type=str,
                        help="The path to the GUI repository.")
    parser.add_argument("--reports_path", required=True, type=str,
                        help="The folder in which test reports should be stored.")
    parser.add_argument("--instrument", type=str, help="Single instrument to run tests on.", default=None)

    args = parser.parse_args()

    reports_path = os.path.abspath(args.reports_path)
    Settings.config_repo_path = configs_repo_path = os.path.abspath(args.configs_repo_path)
    Settings.gui_repo_path = gui_repo_path = os.path.abspath(args.gui_repo_path)

    instruments = ChannelAccessUtils().get_inst_list()
    assert len(instruments) > 0, "No instruments found. Is the instrument list PV available?"

    if args.instrument is not None:
        instruments = list(filter(lambda x: x["name"] == args.instrument, instruments))
        assert len(instruments) > 0, "No instruments matching name={} found.".format(args.instrument)

    return_values = []

    # Run our own unit tests first, before the configuration tests.
    print("Running self-tests...")
    suite = unittest.TestLoader().discover(os.path.join("util", "test_utils"))
    return_values.append(XMLTestRunner(output=str(reports_path), stream=sys.stdout).run(suite).wasSuccessful())
    print("Self-tests complete.")

    # Now run the configuration tests
    for instrument in instruments:

        Settings.name = name = instrument['name']
        Settings.hostname = hostname = instrument['hostName']
        Settings.pv_prefix = pv_prefix = instrument['pvPrefix']

        ca = ChannelAccessUtils(pv_prefix)
        Settings.valid_iocs = ca.get_valid_iocs()
        Settings.protected_iocs = ca.get_protected_iocs()

        print("\n\nChecking out git repository for {} ({})...".format(name, hostname))

        if not GitUtils(configs_repo_path).update_branch(hostname):
            return_values.append(False)
            continue

        print("Testing {} ({})...".format(name, hostname))
        return_values.append(run_tests(name))

    sys.exit(False in return_values)
