from __future__ import print_function
from __future__ import absolute_import
import os
import argparse
import glob

from run_tests import setup_instrument_tests
from tests.settings import Settings

from util.channel_access import ChannelAccessUtils


def get_usage_on_instruments(instruments, functions_to_check):
    """
    :param instruments: list containing the instruments to check
    :param functions_to_check: list containing the functions to check for

    :return: Dictionary of instruments containing a set of IOCs on that instrument
    """

    found_items = {}

    for instrument in instruments:
        instrument_name = instrument["name"]

        found_items[instrument_name] = set()
        setup_instrument_tests(instrument)

        for filename in glob.glob(os.path.join(Settings.config_repo_path, '**/*.py'), recursive=True):
            print("Found python file: {}".format(filename))
            with open(filename, 'r') as f:
                for line_no, line in enumerate(f):
                    for function in functions_to_check:
                        if function in line:
                            found_items[instrument_name].add((filename, line_no, line))

    return found_items


def main():

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description="""Looks through all configurations for IOCS configured to run.
                                            Note: all repositories used by this script will be forcibly cleaned and 
                                            reset while the tests are running.
                                            Do not point this script at any repository where you have changes you want 
                                            to keep!""")

    parser.add_argument("--configs_repo_path", type=str, default="configs",
                        help="The path to the configurations repository.")

    args = parser.parse_args()

    instruments = ChannelAccessUtils().get_inst_list()
    if len(instruments) == 0:
        raise IOError("No instruments found. This is probably because the instrument list PV is unavailable.")

    Settings.set_repo_paths(os.path.abspath(args.configs_repo_path), None)

    functions_to_check = ["check_lowlimit_against_highlimit",
                          "set_title",
                          "set_script_dir",
                          "set_number_soft_periods",
                          "set_sample_par",
                          "set_beamline_par",
                          "set_period",
                          "get_absolute_path"
                          "is_absolute",
                          "get_instrument_py_name"
                          "get_instrument",
                          "send_tcpip",
                          "set_messages_verbosity"]

    found_usages = get_usage_on_instruments(instruments, functions_to_check)

    print("Finished searching")
    print()

    for instrument, found_item in found_usages.items():
        if found_item:
            print("For instrument {}".format(instrument))
            [print(line) for line in found_item]
            print()


if __name__ == "__main__":
    main()
