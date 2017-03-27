from spynnaker.pyNN.utilities.random_stats.abstract_random_stats\
    import AbstractRandomStats
from scipy.stats import binom


class RandomStatsBinomialImpl(AbstractRandomStats):
    """ An implementation of AbstractRandomStats for binomial
        distributions\
        (as scipy.stats.norm takes slightly different parameters to\
        numpy.random.binom)
    """

    def _get_params(self, dist):
        return [dist.parameters['n'], dist.parameters['p']]

    def cdf(self, dist, v):
        return binom.cdf(v, *self._get_params(dist))

    def ppf(self, dist, p):
        return binom.ppf(p, *self._get_params(dist))

    def mean(self, dist):
        return binom.mean(*self._get_params(dist))

    def std(self, dist):
        return binom.std(*self._get_params(dist))

    def var(self, dist):
        return binom.var(*self._get_params(dist))
