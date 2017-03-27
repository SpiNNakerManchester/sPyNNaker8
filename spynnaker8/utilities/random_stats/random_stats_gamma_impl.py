from spynnaker.pyNN.utilities.random_stats.abstract_random_stats \
    import AbstractRandomStats

from scipy.stats import gamma


class RandomStatsGammaImpl(AbstractRandomStats):
    """ An implementation of AbstractRandomStats for normal distributions\
        (as scipy.stats.norm takes slightly different parameters to\
        numpy.random.norm)
    """

    def _get_params(self, dist):
        return [dist.parameters['k'], dist.parameters['theta']]

    def cdf(self, dist, v):
        return gamma.cdf(v, *self._get_params(dist))

    def ppf(self, dist, p):
        return gamma.ppf(p, *self._get_params(dist))

    def mean(self, dist):
        return gamma.mean(*self._get_params(dist))

    def std(self, dist):
        return gamma.std(*self._get_params(dist))

    def var(self, dist):
        return gamma.var(*self._get_params(dist))
