from pyNN.random import RandomDistribution

from spinn_utilities.ranged.range_dictionary import RangeDictionary


def test_uniform():
    rd = RangeDictionary(10)
    rd["a"] = RandomDistribution("uniform", parameters_pos=[-65.0, -55.0])
    ranges = rd["a"].get_ranges()
    assert 10 == len(ranges)


def test_check():
    import inspect
    a = RandomDistribution("uniform", parameters_pos=[-65.0, -55.0])
    arg_spec = inspect.getargspec(a.next)
    assert "n" in arg_spec.args

