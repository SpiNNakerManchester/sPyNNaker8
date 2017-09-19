from spynnaker.pyNN.utilities.random_stats import AbstractRandomStats

from scipy.stats import norm


class RandomStatsNormalImpl(AbstractRandomStats):
    """ An implementation of AbstractRandomStats for normal distributions
    """

    def _get_params(self, dist):
        return [dist.parameters['mu'], dist.parameters['sigma']]

    def cdf(self, dist, v):
        return norm.cdf(v, *self._get_params(dist))

    def ppf(self, dist, p):
        return norm.ppf(p, *self._get_params(dist))

    def mean(self, dist):
        return norm.mean(*self._get_params(dist))

    def std(self, dist):
        return norm.std(*self._get_params(dist))

    def var(self, dist):
        return norm.var(*self._get_params(dist))

    def high(self, dist):
        return None

    def low(self, dist):
        return None
