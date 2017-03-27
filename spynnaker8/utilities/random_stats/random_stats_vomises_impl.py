from spynnaker.pyNN.utilities.random_stats.abstract_random_stats \
    import AbstractRandomStats

from scipy.stats import vonmises


class RandomStatsVonmisesImpl(AbstractRandomStats):
    """ An implementation of AbstractRandomStats for normal distributions\
        (as scipy.stats.norm takes slightly different parameters to\
        numpy.random.norm)
    """

    def _get_params(self, dist):
        return [dist.parameters['mu'], dist.parameters['kappa']]

    def cdf(self, dist, v):
        return vonmises.cdf(v, *self._get_params(dist))

    def ppf(self, dist, p):
        return vonmises.ppf(p, *self._get_params(dist))

    def mean(self, dist):
        return vonmises.mean(*self._get_params(dist))

    def std(self, dist):
        return vonmises.std(*self._get_params(dist))

    def var(self, dist):
        return vonmises.var(*self._get_params(dist))
