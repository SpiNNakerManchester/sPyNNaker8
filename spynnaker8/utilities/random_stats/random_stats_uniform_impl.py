from scipy.stats import uniform
from spynnaker.pyNN.utilities.random_stats import AbstractRandomStats


class RandomStatsUniformImpl(AbstractRandomStats):
    """ An implementation of AbstractRandomStats for uniform distributions
    """

    def _get_params(self, dist):
        return [dist.parameters['low'],
                dist.parameters['high'] - dist.parameters['low']]

    def cdf(self, dist, v):
        return uniform.cdf(v, *self._get_params(dist))

    def ppf(self, dist, p):
        return uniform.ppf(p, *self._get_params(dist))

    def mean(self, dist):
        return uniform.mean(*self._get_params(dist))

    def std(self, dist):
        return uniform.std(*self._get_params(dist))

    def var(self, dist):
        return uniform.var(*self._get_params(dist))

    def high(self, dist):
        return dist.parameters['high']

    def low(self, dist):
        return dist.parameters['low']
