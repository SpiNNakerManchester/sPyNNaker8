from spynnaker.pyNN.utilities.random_stats.abstract_random_stats \
    import AbstractRandomStats

from scipy.stats import expon


class RandomStatsExponentialImpl(AbstractRandomStats):
    """ An implementation of AbstractRandomStats for normal distributions\
        (as scipy.stats.norm takes slightly different parameters to\
        numpy.random.norm)
    """

    def _get_params(self, dist):
        return [dist.parameters['beta']]

    def cdf(self, dist, v):
        return expon.cdf(v, *self._get_params(dist))

    def ppf(self, dist, p):
        return expon.ppf(p, *self._get_params(dist))

    def mean(self, dist):
        return expon.mean(*self._get_params(dist))

    def std(self, dist):
        return expon.std(*self._get_params(dist))

    def var(self, dist):
        return expon.var(*self._get_params(dist))
