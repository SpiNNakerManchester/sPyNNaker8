from spynnaker.pyNN.models.neural_projections.connectors \
    import FromListConnector as CommonFromListConnector
import numpy
from spynnaker8.utilities.exceptions import InvalidParameterType

from pyNN.connectors import Connector


class FromListConnector(CommonFromListConnector, Connector):
    """ Make connections according to a list.
    """
    __slots__ = [
        "_extra_conn_data",
        "_conn_list"]

    def __init__(
            self, conn_list, safe=True, verbose=False, column_names=None,
            callback=None):
        """
        :param conn_list: \
            a list of tuples, one tuple for each connection. Each tuple\
            should contain: `(pre_idx, post_idx, p1, p2, ..., pn)` where\
            `pre_idx` is the index (i.e. order in the Population, not the ID)\
            of the presynaptic neuron, `post_idx` is the index of the\
            postsynaptic neuron, and `p1`, `p2`, etc. are the synaptic\
            parameters (e.g., weight, delay, plasticity parameters).
        :param column_names: \
            the names of the parameters p1, p2, etc. If not provided, it is\
            assumed the parameters are weight, delay (for\
            backwards compatibility).
        :param safe: \
            if True, check that weights and delays have valid values. If\
            False, this check is skipped.
        :param callback: \
            if given, a callable that display a progress bar on the terminal.
        """
        # pylint: disable=too-many-arguments
        if conn_list is None or not len(conn_list):
            raise InvalidParameterType(
                "The connection list for the FromListConnector must contain"
                " at least a list of tuples, each of which should contain at "
                "least: (pre_idx, post_idx)")

        conn_list = numpy.array(conn_list)

        n_columns = 0
        if conn_list.size:
            n_columns = conn_list.shape[1]

        weights = None
        delays = None
        self._extra_conn_data = None

        if column_names is None:
            # if no column names, but more not the expected
            if n_columns == 4:
                column_names = ('pre_idx', 'post_idx', 'weight', 'delay')
                conn_list, weights, delays, self._extra_conn_data = \
                    self._split_conn_list(conn_list, column_names)
            elif n_columns != 2:
                raise TypeError("Argument 'column_names' is required.")
        else:
            # separate conn list to pre, source, weight, delay and the
            # other things
            conn_list, weights, delays, self._extra_conn_data = \
                self._split_conn_list(conn_list, column_names)

        # verify that the rest of the parameters are constant, as we don't
        # support synapse params changing per atom yet
        self._verify_extra_data_meets_constraints()

        # build common from list
        CommonFromListConnector.__init__(
            self, conn_list=conn_list, safe=safe, verbose=verbose)
        Connector.__init__(self, safe=safe, callback=callback)

        # set weights and / or delays if given in list,
        # to avoid overwriting the synapse values if possible
        if weights is not None or delays is not None:
            self.set_weights_and_delays(weights, delays)

    def get_extra_parameters(self):
        """ Getter for the extra parameters.

        :return:
        """
        return self._extra_conn_data

    def _verify_extra_data_meets_constraints(self):
        """ Safety check for current implementation, stops extra parameters\
            from being variable per atom.

        :return:  None
        :raises InvalidParameterType: when the parameters are not constant
        """
        if self._extra_conn_data is not None:
            for data_key in self._extra_conn_data.keys():
                first_data = None
                for (_, _, data) in self._extra_conn_data[data_key]:
                    if first_data is None:
                        first_data = data
                    elif data != first_data:
                        raise InvalidParameterType(
                            "The parameter {} needs top have a consistent "
                            "value".format(data_key))
