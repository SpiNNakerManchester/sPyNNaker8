from spynnaker.pyNN.utilities.random_stats import AbstractRandomStats

from scipy.stats import truncnorm


class RandomStatsNormalClippedImpl(AbstractRandomStats):
    """ An implementation of AbstractRandomStats for normal distributions that\
        are clipped to a boundary (redrawn)
    """

    def _get_params(self, dist):
        return [dist.parameters['low'], dist.parameters['high'],
                dist.parameters['mu'], dist.parameters['sigma']]

    def cdf(self, dist, v):
        return truncnorm.cdf(v, *self._get_params(dist))

    def ppf(self, dist, p):
        return truncnorm.ppf(p, *self._get_params(dist))

    def mean(self, dist):
        return truncnorm.mean(*self._get_params(dist))

    def std(self, dist):
        return truncnorm.std(*self._get_params(dist))

    def var(self, dist):
        return truncnorm.var(*self._get_params(dist))

    def high(self, dist):
        return dist.parameters['high']

    def low(self, dist):
        return dist.parameters['low']
