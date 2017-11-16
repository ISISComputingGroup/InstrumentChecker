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


def run_instrument_tests(inst_name, reports_path):
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
    for config in ConfigurationUtils(Settings.config_repo_path).get_configurations_as_list():
        suite.addTests([ConfigurationsTests(test, config) for test in loader.getTestCaseNames(ConfigurationsTests)])

    for component in ComponentUtils(Settings.config_repo_path).get_configurations_as_list():
        suite.addTests([ComponentsTests(test, component) for test in loader.getTestCaseNames(ComponentsTests)])

    for synoptic in SynopticUtils(Settings.config_repo_path).get_synoptics_filenames():
        suite.addTests([SynopticTests(test, synoptic) for test in loader.getTestCaseNames(SynopticTests)])

    runner = XMLTestRunner(output=str(os.path.join(reports_path, inst_name)), stream=sys.stdout)
    return runner.run(suite).wasSuccessful()


def setup_instrument_tests(instrument):
    """
    Sets up the settings class and configurations repository to point at the given instrument.

    :param instrument: A dictionary representing the properties of an instrument as per the CS:INSTLIST PV.
    :return: True if successful, False otherwise.
    """
    name, hostname, pv_prefix = instrument['name'], instrument['hostName'], instrument['pvPrefix']
    Settings.set_instrument(name, hostname, pv_prefix)

    print("\n\nChecking out git repository for {} ({})...".format(name, hostname))
    if not GitUtils(Settings.config_repo_path).update_branch(hostname):
        return False

    return True


def run_self_tests(reports_path):
    """
    Runs our own unit tests.
    :return: True if all tests passed, False otherwise
    """
    print("Running self-tests...")
    suite = unittest.TestLoader().discover(os.path.join("util", "test_utils"))
    return XMLTestRunner(output=str(reports_path), stream=sys.stdout).run(suite).wasSuccessful()


def run_all_tests(reports_path, instruments):
    """
    Runs all of the tests (including our own unit tests)
    :return: True if all tests succeeded, False otherwise.
    """

    # Run our own unit tests first, before the configuration tests.
    return_values = [run_self_tests(reports_path)]

    # Now run the configuration tests
    for instrument in instruments:
        if setup_instrument_tests(instrument):
            return_values.append(run_instrument_tests(instrument['name'], reports_path))
        else:
            return_values.append(False)

    return all(value for value in return_values)


def main():

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
    parser.add_argument("--instruments", type=str, nargs="+", default=None,
                        help="Instruments to run tests on. If defined, configuration tests will only be run on the "
                             "given instruments. If not defined, tests will be run on all instruments.")

    args = parser.parse_args()

    instruments = ChannelAccessUtils().get_inst_list()
    if len(instruments) == 0:
        raise IOError("No instruments found. This is probably because the instrument list PV is unavailable.")

    if args.instruments is not None:
        instruments = list(filter(lambda x: x["name"] in args.instruments, instruments))
        if len(instruments) < len(args.instruments):
            raise ValueError("Some instruments specified could not be found in the instrument list.")

    reports_path = os.path.abspath(args.reports_path)
    Settings.set_repo_paths(os.path.abspath(args.configs_repo_path), os.path.abspath(args.gui_repo_path))

    success = run_all_tests(reports_path, instruments)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
