from spynnaker.pyNN.models.neural_projections.connectors. \
    from_list_connector import FromListConnector as CommonFromListConnector
from pyNN.connectors import FromListConnector as PyNNFromListConnector


class FromListConnector(CommonFromListConnector, PyNNFromListConnector):
    """ Make connections according to a list.

    :param: conn_list:
        a list of tuples, one tuple for each connection. Each
        tuple should contain::

         (pre_idx, post_idx, weight, delay)

        where pre_idx is the index (i.e. order in the Population,
        not the ID) of the presynaptic neuron, and post_idx is
        the index of the postsynaptic neuron.
    """

    def __init__(
            self, conn_list, safe=True, verbose=False, column_names=None,
            callback=None):
        """
        Creates a new FromListConnector.
        """
        CommonFromListConnector.__init__(
            self, conn_list=None, safe=safe, verbose=verbose)
        PyNNFromListConnector.__init__(
            self, conn_list=conn_list, column_names=column_names, safe=safe,
            callback=callback)

    @property
    def conn_list(self):
        return self._conn_list

    @conn_list.setter
    def conn_list(self, new_value):
        self._conn_list = new_value
