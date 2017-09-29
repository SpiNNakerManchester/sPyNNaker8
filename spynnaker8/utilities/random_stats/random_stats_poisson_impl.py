from spynnaker.pyNN.utilities.random_stats import AbstractRandomStats

from scipy.stats import poisson


class RandomStatsPoissonImpl(AbstractRandomStats):
    """ An implementation of AbstractRandomStats for poisson distributions
    """

    def _get_params(self, dist):
        return [dist.parameters['mu'], dist.parameters['lambda_']]

    def cdf(self, dist, v):
        return poisson.cdf(v, *self._get_params(dist))

    def ppf(self, dist, p):
        return poisson.ppf(p, *self._get_params(dist))

    def mean(self, dist):
        return poisson.mean(*self._get_params(dist))

    def std(self, dist):
        return poisson.std(*self._get_params(dist))

    def var(self, dist):
        return poisson.var(*self._get_params(dist))

    def high(self, dist):
        return None

    def low(self, dist):
        return None
