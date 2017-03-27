from spynnaker.pyNN.utilities.random_stats.abstract_random_stats \
    import AbstractRandomStats

from scipy.stats import randint


class RandomStatsRandIntImpl(AbstractRandomStats):
    """ An implementation of AbstractRandomStats for normal distributions\
        (as scipy.stats.norm takes slightly different parameters to\
        numpy.random.norm)
    """

    def _get_params(self, dist):
        return [dist.parameters['low'], dist.parameters['high']]

    def cdf(self, dist, v):
        return randint.cdf(v, *self._get_params(dist))

    def ppf(self, dist, p):
        return randint.ppf(p, *self._get_params(dist))

    def mean(self, dist):
        return randint.mean(*self._get_params(dist))

    def std(self, dist):
        return randint.std(*self._get_params(dist))

    def var(self, dist):
        return randint.var(*self._get_params(dist))
