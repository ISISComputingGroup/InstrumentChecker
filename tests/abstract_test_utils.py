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
        This initializes a utils object on which testing will be done. It should be instantiated as ComponentUtils or
        ConfigurationUtils in a subclass. Also initializes type of the SingleTests class, which should be "components"
        or "configurations" .
        """
        self.utils = None
        self.type = None

    def test_GIVEN_an_instrument_THEN_all_block_pvs_are_interesting(self):
        interesting_pvs = ChannelAccessUtils(Settings.pv_prefix).get_interesting_pvs()

        if len(interesting_pvs) == 0:
            self.skipTest("Set of interesting PVs is empty, this is probably because the instrument {} is off. Since "
                          "we do not know interesting pvs, {} are not checked for non interesting block pvs test is "
                          "terminated early.".format(Settings.pv_prefix, self.type))

        non_interesting_block_pvs = [block_pv for block_pv in self.utils.get_set_of_block_pvs_for_all_configs(
                                        ) if block_pv not in interesting_pvs]
        num_non_interesting_block_pvs = len(non_interesting_block_pvs)

        if num_non_interesting_block_pvs != 0:
            print("\nWARNING! The instrument {} has {} non-interesting pvs that have a block on them in {}".
                  format(Settings.pv_prefix, len(non_interesting_block_pvs), self.type))
            self.update_total_non_interesting_block_pvs(num_non_interesting_block_pvs)
            print(non_interesting_block_pvs)

    @abstractmethod
    def update_total_non_interesting_block_pvs(self, num_non_interesting_block_pvs):
        """
        This method should monitor the number of non interesting block pvs discovered so far for
        components/configurations and print it to the screen.
        :param num_non_interesting_block_pvs: the number of non interesting block pvs for all instruments so far.
        """
        pass
