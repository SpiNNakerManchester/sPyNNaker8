from pyNN.random import RandomDistribution
from spynnaker.pyNN.utilities.ranged import SpynnakerRangeDictionary
import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase


class TestRanged(BaseTestCase):

    def test_uniform(self):
        # Need to do setup to get a pynn version
        p.setup(10)
        rd = SpynnakerRangeDictionary(10)
        rd["a"] = RandomDistribution("uniform", parameters_pos=[-65.0, -55.0])
        ranges = rd["a"].get_ranges()
        assert 10 == len(ranges)
