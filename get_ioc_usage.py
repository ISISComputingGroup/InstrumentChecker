from __future__ import absolute_import, print_function

import argparse
import os

from run_tests import setup_instrument_tests
from tests.settings import Settings
from util.channel_access import ChannelAccessUtils
from util.configurations import ComponentUtils, ConfigurationUtils, DeviceUtils


def calc_iocs_on_intruments(instruments):
    """
    :return: Dictionary of instruments containing a set of IOCs on that instrument
    """

    instrument_configs = {}
    instrument_device_screens = {}

    for instrument in instruments:
        instrument_name = instrument["name"]

        instrument_configs[instrument_name] = set()
        setup_instrument_tests(instrument)
        config_utils = ConfigurationUtils(Settings.config_repo_path)
        for config in ConfigurationUtils(Settings.config_repo_path).get_configurations_as_list():
            iocs_in_config = set(config_utils.get_iocs(config_utils.get_iocs_xml(config)))
            instrument_configs[instrument_name] = instrument_configs[instrument_name].union(
                iocs_in_config
            )

        component_utils = ComponentUtils(Settings.config_repo_path)
        for component in ComponentUtils(Settings.config_repo_path).get_configurations_as_list():
            iocs_in_component = set(
                component_utils.get_iocs(component_utils.get_iocs_xml(component))
            )
            instrument_configs[instrument_name] = instrument_configs[instrument_name].union(
                iocs_in_component
            )

        device_utils = DeviceUtils(Settings.config_repo_path)
        try:
            device_screens = device_utils.get_device_screens(
                device_utils.get_device_screens_from_xml()
            )
        except Exception:
            # Instrument does not have device screen directory
            device_screens = []

        instrument_device_screens[instrument_name] = set(device_screens)

    return instrument_configs, instrument_device_screens


def print_iocs_on_instruments(instrument_configs):
    """
    Print iocs that are on each instrument
    :param instrument_configs: instrument ioc config dictionary
    """

    for instrument, iocs in instrument_configs.items():
        print(instrument)
        print("    - {}\n".format("\n    - ".join(sorted(iocs))))


def print_instruments_with_ioc(instrument_configs, ioc_name):
    """
    Print instruments with an ioc starting with a string
    :param instrument_configs: instrument ioc config dictionary
    :param ioc_name: name of the ioc
    """
    print("Instruments containing IOCs starting with {}".format(ioc_name))
    for instrument, iocs in instrument_configs.items():
        for ioc in iocs:
            if ioc.lower().startswith(ioc_name.lower()):
                print("{} has {}".format(instrument, ioc))


def print_device_screens_on_instrument(instrument_device_screens):
    """
    Print device screens that are on each instrument
    """
    print("\n Instruments Device Screens: \n")
    for instrument, devices in instrument_device_screens.items():
        print(instrument)
        print("    - {}\n".format("\n    - ".join(sorted(devices))))


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="""Looks through all configurations for IOCS configured to run.
                                            Note: all repositories used by this script will be forcibly cleaned and 
                                            reset while the tests are running.
                                            Do not point this script at any repository where you have changes you want 
                                            to keep!""",
    )

    parser.add_argument(
        "--configs_repo_path",
        required=True,
        type=str,
        help="The path to the configurations repository.",
    )
    parser.add_argument(
        "--gui_repo_path", required=True, type=str, help="The path to the GUI repository."
    )
    parser.add_argument(
        "--instruments",
        type=str,
        nargs="+",
        default=None,
        help="Instruments to look at. If defined, will only be run on the "
        "given instruments. If not defined, tests will be run on all instruments.",
    )
    parser.add_argument(
        "--ioc",
        type=str,
        default=None,
        help="If specified show instruments with IOC starting with"
        "this string, otherwise show all iocs on the instruments",
    )
    parser.add_argument(
        "--device_screens", help="Print device screens present on instrument/s", action="store_true"
    )

    args = parser.parse_args()

    instruments = ChannelAccessUtils().get_inst_list()
    if len(instruments) == 0:
        raise IOError(
            "No instruments found. This is probably because the instrument list PV is unavailable."
        )

    if args.instruments is not None:
        instruments = [x for x in instruments if x["name"] in args.instruments]
        if len(instruments) < len(args.instruments):
            raise ValueError(
                "Some instruments specified could not be found in the instrument list."
            )

    Settings.set_repo_paths(
        os.path.abspath(args.configs_repo_path), os.path.abspath(args.gui_repo_path)
    )

    instrument_configs, instrument_device_screens = calc_iocs_on_intruments(instruments)

    if args.ioc is None:
        print_iocs_on_instruments(instrument_configs)
    else:
        print_instruments_with_ioc(instrument_configs, args.ioc)

    if args.device_screens:
        print_device_screens_on_instrument(instrument_device_screens)


if __name__ == "__main__":
    main()
