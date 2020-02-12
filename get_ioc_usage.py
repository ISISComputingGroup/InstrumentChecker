from __future__ import print_function
from __future__ import absolute_import
import os
import argparse

from run_tests import setup_instrument_tests
from tests.settings import Settings

from util.channel_access import ChannelAccessUtils
from util.configurations import ConfigurationUtils, ComponentUtils


def calc_iocs_on_intruments(instruments):
    """
    :return: Dictionary of instruments containing a set of IOCs on that instrument
    """

    instrument_configs = {}

    for instrument in instruments:
        instrument_name = instrument["name"]

        instrument_configs[instrument_name] = set()
        setup_instrument_tests(instrument)
        config_utils = ConfigurationUtils(Settings.config_repo_path)
        for config in ConfigurationUtils(Settings.config_repo_path).get_configurations_as_list():
            iocs_in_config = set(config_utils.get_iocs(config_utils.get_iocs_xml(config)))
            instrument_configs[instrument_name] = instrument_configs[instrument_name].union(iocs_in_config)

        component_utils = ComponentUtils(Settings.config_repo_path)
        for component in ComponentUtils(Settings.config_repo_path).get_configurations_as_list():
            iocs_in_component = set(component_utils.get_iocs(component_utils.get_iocs_xml(component)))
            instrument_configs[instrument_name] = instrument_configs[instrument_name].union(iocs_in_component)

    return instrument_configs


def print_iocs_on_instruments(instrument_configs):
    """
    Print iocs that are on each instrument
    :param instrument_configs: instrument ioc config dictionary
    """

    for instrument, iocs in list(instrument_configs.items()):
        print(instrument)
        print("    - {}\n".format("\n    - ".join(sorted(iocs))))


def print_instruments_with_ioc(instrument_configs, ioc_name):
    """
    Print instruments with an ioc starting with a string
    :param instrument_configs: instrument ioc config dictionary
    :param ioc_name: name of the ioc
    """
    print("All those having the {}".format(ioc_name))
    for instrument, iocs in list(instrument_configs.items()):

        for ioc in iocs:
            if ioc.lower().startswith(ioc_name.lower()):
                print(instrument)
                break


def main():

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description="""Looks through all configurations for IOCS configured to run.
                                            Note: all repositories used by this script will be forcibly cleaned and 
                                            reset while the tests are running.
                                            Do not point this script at any repository where you have changes you want 
                                            to keep!""")

    parser.add_argument("--configs_repo_path", required=True, type=str,
                        help="The path to the configurations repository.")
    parser.add_argument("--gui_repo_path", required=True, type=str,
                        help="The path to the GUI repository.")
    parser.add_argument("--instruments", type=str, nargs="+", default=None,
                        help="Instruments to look at. If defined, will only be run on the "
                             "given instruments. If not defined, tests will be run on all instruments.")
    parser.add_argument("--ioc", type=str, default=None, help="If specified show instruments with IOC starting with"
                                                              "this string, otherwise show all iocs on the instruments")

    args = parser.parse_args()

    instruments = ChannelAccessUtils().get_inst_list()
    if len(instruments) == 0:
        raise IOError("No instruments found. This is probably because the instrument list PV is unavailable.")

    if args.instruments is not None:
        instruments = list([x for x in instruments if x["name"] in args.instruments])
        if len(instruments) < len(args.instruments):
            raise ValueError("Some instruments specified could not be found in the instrument list.")

    Settings.set_repo_paths(os.path.abspath(args.configs_repo_path), os.path.abspath(args.gui_repo_path))

    instrument_configs = calc_iocs_on_intruments(instruments)

    if args.ioc is None:
        print_iocs_on_instruments(instrument_configs)
    else:
        print_instruments_with_ioc(instrument_configs, args.ioc)


if __name__ == "__main__":
    main()
