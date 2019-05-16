import scipy.stats
from spynnaker.pyNN.utilities.random_stats import AbstractRandomStats


class RandomStatsScipyImpl(AbstractRandomStats):
    """ A Random Statistics object that uses scipy directly
    """

    def __init__(self, distribution_type):
        self._scipy_stats = getattr(scipy.stats, distribution_type)

    def cdf(self, dist, v):
        return self._scipy_stats.cdf(v, *dist.parameters)

    def ppf(self, dist, p):
        return self._scipy_stats.ppf(p, *dist.parameters)

    def mean(self, dist):
        return self._scipy_stats.mean(*dist.parameters)

    def std(self, dist):
        return self._scipy_stats.std(*dist.parameters)

    def var(self, dist):
        return self._scipy_stats.var(*dist.parameters)

    def high(self, dist):
        if "high" in dist.parameters:
            return dist.parameters['high']
        return None

    def low(self, dist):
        if "low" in dist.parameters:
            return dist.parameters['low']
        return None
