from pyNN.random import RandomDistribution

from spinn_utilities.ranged.range_dictionary import RangeDictionary


def test_uniform():
    rd = RangeDictionary(10)
    rd["a"] = RandomDistribution("uniform", parameters_pos=[-65.0, -55.0])
    ranges = rd["a"].get_ranges()
    assert 10 == len(ranges)
