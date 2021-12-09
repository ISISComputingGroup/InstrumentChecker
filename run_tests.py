from __future__ import print_function
from __future__ import absolute_import
import typing
from builtins import str
import os
from json import loads, JSONDecodeError
import sys
import unittest
from xmlrunner import XMLTestRunner
import argparse
import traceback
import os

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
from util.gui import GuiUtils
from util.synoptic import SynopticUtils
from util.version import VersionUtils


def run_instrument_tests(inst_name, reports_path):
    """
    Runs the test suite
    :param inst_name: The name of the instrument to run tests on,
                    used to sort the test reports folder into instrument-specific reports
    :param reports_path: The path to store test reports
    :return: True if the tests passed, false otherwise
    """
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    for case in [ScriptingDirectoryTests, GlobalsTests, VersionTests, ConfigurationsSingleTests, ComponentsSingleTests]:
        suite.addTests(loader.loadTestsFromTestCase(case))

    # Add configs test suite a dynamic number of times with an argument of the config name.
    # unittest's test loader is unable to take arguments to test classes by default so have
    # to use the getTestCaseNames() syntax and explicitly add the argument ourselves.

    try:
        configs = ConfigurationUtils(Settings.config_repo_path).get_configurations_as_list()
        components = ComponentUtils(Settings.config_repo_path).get_configurations_as_list()
        synoptics = SynopticUtils(Settings.config_repo_path).get_synoptics_filenames()
    except IOError as e:
        print("Failed to build tests for instrument {}: exception occured while generating tests.".format(inst_name))
        traceback.print_exc(e)
        return False

    for config in configs:
        suite.addTests([ConfigurationsTests(test, config) for test in loader.getTestCaseNames(ConfigurationsTests)])

    for component in components:
        suite.addTests([ComponentsTests(test, component) for test in loader.getTestCaseNames(ComponentsTests)])

    for synoptic in synoptics:
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
    try:
        Settings.set_instrument(name, hostname, pv_prefix)
    except Exception:
        print("Unable to set instrument to {} because {}".format(name, traceback.format_exc()))
        return False
    
    print("\n\nChecking out git repository for {} ({})...".format(name, hostname))
    config_repo_update_successful = GitUtils(Settings.config_repo_path).update_branch(hostname)

    version_utils = VersionUtils(Settings.config_repo_path)

    if version_utils.version_file_exists():
        GuiUtils(Settings.gui_repo_path).get_gui_repo_at_release(version_utils.get_version())
    else:
        print("Warning: could not determine GUI version for instrument {}".format(instrument))
    return config_repo_update_successful


def run_self_tests(reports_path):
    """
    Runs our own unit tests.
    :return: True if all tests passed, False otherwise
    """
    print("Running self-tests...")
    suite = unittest.TestLoader().discover(os.path.join("util", "test_utils"))
    return XMLTestRunner(output=str(reports_path), stream=sys.stdout).run(suite).wasSuccessful()


def get_excluded_list_of_instruments() -> typing.List[str]:
    """
    Gets the excluded list of instruments by getting the value of the environment variable `DISABLE_CHECK_INST`.
    This needs to be in the format of a JSON list, for example:
    ["SANS2D", "DEMO"]
    """
    excluded_list_env_var = os.environ.get("DISABLE_CHECK_INST")
    print(f"Excluded instruments: {excluded_list_env_var}")
    try:
        return loads(excluded_list_env_var)
    except (JSONDecodeError, TypeError):
        return []


def run_all_tests(reports_path, instruments):
    """
    Runs all of the tests (including our own unit tests)
    :return: True if all tests succeeded, False otherwise.
    """

    # Run our own unit tests first, before the configuration tests.
    if not run_self_tests(reports_path):
        print("Unit tests failed!")
        return False

    return_values = []
    excluded_instruments = get_excluded_list_of_instruments()
    # Now run the configuration tests
    for instrument in instruments:
        if instrument not in excluded_instruments:
            if setup_instrument_tests(instrument):
                return_values.append(run_instrument_tests(instrument['name'], reports_path))
            else:
                return_values.append(False)
        else: 
            print(f"Skipping instrument {instrument}")

    _print_test_run_end_messages()

    return all(value for value in return_values)


def _print_test_run_end_messages():
    """
    Method used to print any messages that should be printed at the end of the all instruments test run.
    """
    print("{} non interesting component block pvs in total across all instruments".format(
        ComponentsSingleTests.TOTAL_NON_INTERESTING_PVS_IN_BLOCKS))
    print("{} non interesting configuration block pvs in total across all instruments".format(
        ConfigurationsSingleTests.TOTAL_NON_INTERESTING_PVS_IN_BLOCKS))


def main():

    # We can't put this in the batch file as it is overwritten by genie_python.bat. Increasing it in genie_python.bat
    # would increase it for all instruments, which may be undesirable.
    # The higher limit is required for DETMON as it has a huge number of blocks.
    os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = str(1000000)

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
        instruments = [x for x in instruments if x["name"] in args.instruments]
        if len(instruments) < len(args.instruments):
            raise ValueError("Some instruments specified could not be found in the instrument list.")

## the following will exclude down instruments for testing
## change instruments -> instruments_up in run_all_tests below
#    inst_names = [x["name"] for x in instruments]
#    inst_up = []
#    for inst in inst_names:
#        if ChannelAccessUtils("IN:{}:".format(inst)).get_value("CS:BLOCKSERVER:GET_CURR_CONFIG_DETAILS") is not None:
#            inst_up.append(inst)
#        else:
#            print("Skipping {} as instrument down (no blockserver)".format(inst))
#    instruments_up = [x for x in instruments if x["name"] in inst_up]

    reports_path = os.path.abspath(args.reports_path)
    Settings.set_repo_paths(os.path.abspath(args.configs_repo_path), os.path.abspath(args.gui_repo_path))

    success = run_all_tests(reports_path, instruments)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()