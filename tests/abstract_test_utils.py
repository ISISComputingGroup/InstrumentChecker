import unittest
from abc import ABCMeta, abstractmethod

from settings import Settings
from util.channel_access import ChannelAccessUtils


class AbstractSingleTests(unittest.TestCase):
    __metaclass__ = ABCMeta

    def setUp(self):
        self.utils = None

    def test_GIVEN_an_instrument_THEN_all_block_pvs_are_interesting(self):
        interesting_pvs = ChannelAccessUtils(Settings.pv_prefix).get_interesting_pvs()

        if len(interesting_pvs) == 0:
            print("Set of interesting PVs is empty, this is probably because the instrument {} is off. Since we do not "
                  "know interesting pvs, {}s are not checked for non interesting block pvs test is terminated "
                  "early.".format(Settings.pv_prefix, self.get_config_type()))

            # exiting the function early will still make the test pass automatically
            return

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
        raise NotImplementedError("You need to implement this abstract method!")
        pass

    @abstractmethod
    def get_config_type(self):
        raise NotImplementedError("You need to implement this abstract method!")
        pass

