from spynnaker.pyNN.models.neural_projections.connectors \
    import FixedNumberPreConnector as CommonFixedNumberPreConnector
from pyNN.connectors import FixedNumberPreConnector as \
    PyNNFixedNumberPreConnector

import logging

logger = logging.getLogger(__file__)


class FixedNumberPreConnector(CommonFixedNumberPreConnector,
                              PyNNFixedNumberPreConnector):
    """ Connects a fixed number of pre-synaptic neurons selected at random,\
        to all post-synaptic neurons
    """
    __slots__ = []

    def __init__(
            self, n, allow_self_connections=True, safe=True, verbose=False,
            with_replacement=False, rng=None, callback=None):
        """
        :param n: \
            number of random pre-synaptic neurons connected to output
        :type n: int
        :param allow_self_connections: \
            if the connector is used to connect a Population to itself, this\
            flag determines whether a neuron is allowed to connect to itself,\
            or only to other neurons in the Population.
        :type allow_self_connections: bool
        :param safe: \
            Whether to check that weights and delays have valid values.\
            If False, this check is skipped.
        :type safe: bool
        :param verbose: \
            Whether to output extra information about the connectivity to a\
            CSV file
        :type verbose: bool
        :param with_replacement:\
            if False, once a connection is made, it can't be made again; if\
            True, multiple connections between the same pair of neurons are\
            allowed
        :type with_replacement: bool
        :param rng:
        :param callback:
        """
        # pylint: disable=too-many-arguments
        super(FixedNumberPreConnector, self).__init__(
            n=n, allow_self_connections=allow_self_connections,
            with_replacement=with_replacement, safe=safe, verbose=verbose,
            rng=rng)

    @property
    def n(self):
        return self._n_pre

    @n.setter
    def n(self, new_value):
        self._n_pre = new_value
