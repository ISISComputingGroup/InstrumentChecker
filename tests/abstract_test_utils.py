import unittest
from abc import ABCMeta, abstractmethod

from settings import Settings
from util.channel_access import ChannelAccessUtils


class AbstractSingleTests(unittest.TestCase):
    """
    Abstract class for tests to be run exactly one regardless of how many components/configurations exist. It is meant
    to be extended by classes for configurations and for components.
    """
    __metaclass__ = ABCMeta

    def setUp(self):
        """
        This only initializes a utils object that should be instantiated as ComponentUtils or ConfigurationUtils or
        anything else in a subclass.
        :return: nothing.
        """
        self.utils = None

    def test_GIVEN_an_instrument_THEN_all_block_pvs_are_interesting(self):
        interesting_pvs = ChannelAccessUtils(Settings.pv_prefix).get_interesting_pvs()

        if len(interesting_pvs) == 0:
            self.skipTest("Set of interesting PVs is empty, this is probably because the instrument {} is off. Since "
                          "we do not know interesting pvs, {}s are not checked for non interesting block pvs test is "
                          "terminated early.".format(Settings.pv_prefix, self.get_config_type()))

        non_interesting_block_pvs = [block_pv for block_pv in self.utils.get_set_of_block_pvs_for_all_configs(
                                        ) if block_pv not in interesting_pvs]
        num_non_interesting_block_pvs = len(non_interesting_block_pvs)

        if num_non_interesting_block_pvs != 0:
            print("\nWARNING! The instrument {} has {} non-interesting pvs that have a block on them in {}s".
                  format(Settings.pv_prefix, len(non_interesting_block_pvs), self.get_config_type()))
            self.print_total_non_interesting_block_pvs(num_non_interesting_block_pvs)
            print(non_interesting_block_pvs)

    @abstractmethod
    def print_total_non_interesting_block_pvs(self, num_non_interesting_block_pvs):
        """
        This class should monitor the number of non interesting block pvs discovered so far for
        components/configurations and print it to the screen.
        :param num_non_interesting_block_pvs: the number of non interesting block pvs for all instruments so far.
        :return: nothing.
        """
        pass

    @abstractmethod
    def get_config_type(self):
        """
        This method is used for printing messages to the screen where the only difference is the word
        configuration/component.
        :return: configuration for ConfigurationSingleTests, component for ComponentsSingleTests
        """
        pass

