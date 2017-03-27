from spynnaker.pyNN.utilities.random_stats.abstract_random_stats \
    import AbstractRandomStats

from scipy.stats import lognorm


class RandomStatsLogNormalImpl(AbstractRandomStats):
    """ An implementation of AbstractRandomStats for normal distributions\
        (as scipy.stats.norm takes slightly different parameters to\
        numpy.random.norm)
    """

    def _get_params(self, dist):
        return [dist.parameters['mu'], dist.parameters['sigma']]

    def cdf(self, dist, v):
        return lognorm.cdf(v, *self._get_params(dist))

    def ppf(self, dist, p):
        return lognorm.ppf(p, *self._get_params(dist))

    def mean(self, dist):
        return lognorm.mean(*self._get_params(dist))

    def std(self, dist):
        return lognorm.std(*self._get_params(dist))

    def var(self, dist):
        return lognorm.var(*self._get_params(dist))
