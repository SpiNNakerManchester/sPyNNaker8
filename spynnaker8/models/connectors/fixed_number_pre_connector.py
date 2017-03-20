from pyNN.space import Space

from spynnaker.pyNN.models.neural_projections.connectors. \
    fixed_number_pre_connector import FixedNumberPreConnector as \
    CommonFixedNumberPreConnector
from pyNN.connectors import FixedNumberPreConnector as \
    PyNNFixedNumberPreConnector

import logging

logger = logging.getLogger(__file__)


class FixedNumberPreConnector(
    CommonFixedNumberPreConnector, PyNNFixedNumberPreConnector):
    """ Connects a fixed number of pre-synaptic neurons selected at random,
        to all post-synaptic neurons
    """

    def __init__(
            self, n, allow_self_connections=True, safe=True, verbose=False,
            with_replacement=False, rng=None, callback=None):
        """
        :param n:
            number of random pre-synaptic neurons connected to output
        :param allow_self_connections:
            if the connector is used to connect a
            Population to itself, this flag determines whether a neuron is
            allowed to connect to itself, or only to other neurons in the
            Population.
        :param `pyNN.Space` space:
            a Space object, needed if you wish to specify distance-
            dependent weights or delays - not implemented
        :param safe: if True, check that weights and delays have valid values.
        If False, this check is skipped.
        :param verbose:
        :param with_replacement:
        :param rng:
        :param callback:
        """
        CommonFixedNumberPreConnector.__init__(
            self, n=n, safe=safe,
            allow_self_connections=allow_self_connections, verbose=verbose)
        PyNNFixedNumberPreConnector.__init__(
            self, n=n, allow_self_connections=allow_self_connections,
            with_replacement=with_replacement, rng=rng, safe=safe,
            callback=callback)

    @property
    def n(self):
        return self._n_pre

    @n.setter
    def n(self, new_value):
        self._n_pre = new_value
