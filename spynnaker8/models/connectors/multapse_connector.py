import numpy
from spynnaker.pyNN.models.neural_projections.connectors import (
    MultapseConnector as _BaseClass)


class MultapseConnector(_BaseClass):
    """
    Create a multapse connector. The size of the source and destination\
    populations are obtained when the projection is connected. The number of\
    synapses is specified. when instantiated, the required number of synapses\
    is created by selecting at random from the source and target populations\
    with replacement. Uniform selection probability is assumed.

    :param n: This is the total number of synapses in the connection.
    :type n: int
    :param allow_self_connections:
        Bool. Allow a neuron to connect to itself or not.
    :type allow_self_connections: bool
    :param with_replacement:
        Bool. When selecting, allow a neuron to be re-selected or not.
    :type with_replacement: bool
    """
    __slots__ = []

    def __init__(self, n, allow_self_connections=True,
                 with_replacement=True, safe=True, verbose=False,
                 rng=None):
        super(MultapseConnector, self).__init__(
            num_synapses=n, allow_self_connections=allow_self_connections,
            with_replacement=with_replacement, safe=safe, verbose=verbose,
            rng=rng)

    def get_rng_next(self, num_synapses, prob_connect):
        # Below is how numpy does multinomial internally...
        size = len(prob_connect)
        multinomial = numpy.zeros(size, int)
        total = 1.0
        dn = num_synapses
        for j in range(0, size - 1):
            multinomial[j] = self._rng.next(
                1, distribution="binomial",
                parameters={'n': dn, 'p': prob_connect[j] / total})
            dn = dn - multinomial[j]
            if dn <= 0:
                break
            total = total - prob_connect[j]
        if dn > 0:
            multinomial[size - 1] = dn

        return multinomial
