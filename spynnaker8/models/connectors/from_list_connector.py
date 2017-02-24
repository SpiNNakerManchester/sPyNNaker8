from pyNN.random import RandomDistribution
from spynnaker.pyNN.models.neural_projections.connectors. \
    from_list_connector import FromListConnector as CommonFromListConnector
from pyNN.connectors import FromListConnector as PyNNFromListConnector
import numpy

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
        self._weight = None
        self._delay = None

    def convert_into_numpy(self):
        if self._conn_list is None or len(self._conn_list) == 0:
            self._conn_list = numpy.zeros(0, dtype=self.CONN_LIST_DTYPE)
        else:
            weights = self._convert_parameter(self._weight)
            delays = self._convert_parameter(self._delay)
            temp_conn_list = list()
            for index in range(0, len(self._conn_list)):
                temp_conn_list.append(
                    (self._conn_list[index][0], self._conn_list[index][1],
                     weights[index], delays[index]))
            self._conn_list = numpy.array(
                temp_conn_list, dtype=self.CONN_LIST_DTYPE)

    def _convert_parameter(self, param):
        if isinstance(self._weight, RandomDistribution):
            if len(self._conn_list) > 1:
                params = param.next(n=len(self._conn_list))
            else:
                params = [param.next(n=len(self._conn_list))]
        elif not hasattr(param, '__iter__'):
            params = [
                param for _ in range(0, len(self._conn_list))]
        else:
            params = param
        return params

    @property
    def weights(self):
        return self._weight

    @weights.setter
    def weights(self, new_value):
        self._weight = new_value

    @property
    def delays(self):
        return self._delay

    @delays.setter
    def delays(self, new_value):
        self._delay = new_value
