import numpy
from pyNN.connectors import Connector
from spynnaker.pyNN.models.neural_projections.connectors import (
    FromListConnector as CommonFromListConnector)
from spynnaker8.utilities.exceptions import InvalidParameterType


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
        # to avoid overwriting with the synapse values if possible
        if weights is not None or delays is not None:
            self.create_weights_and_delays_from_list(weights, delays)

    def get_extra_parameters(self):
        """ Getter for the extra parameters.

        :return:
        """
        return self._extra_conn_data

    @staticmethod
    def _split_conn_list(conn_list, column_names):
        """ Separate the connection list into the blocks needed.
        :param conn_list: the original connection list
        :param column_names: the column names if exist
        :return: source dest list, weights list, delays list, extra list
        """

        # weights and delay index
        weight_index = None
        delay_index = None

        # conn lists
        weights = None
        delays = None

        # locate weights and delay index in the listings
        if "weight" in column_names:
            weight_index = column_names.index("weight")
        if "delay" in column_names:
            delay_index = column_names.index("delay")
        element_index = list(range(2, len(column_names)))

        # figure out where other stuff is
        conn_list = numpy.array(conn_list)
        source_destination_conn_list = conn_list[:, [0, 1]]

        if weight_index is not None:
            element_index.remove(weight_index)
            weights = conn_list[:, weight_index]
        if delay_index is not None:
            element_index.remove(delay_index)
            delays = conn_list[:, delay_index]

        # build other data element conn list (with source and destination)
        other_conn_list = None
        other_element_column_names = list()
        for element in element_index:
            other_element_column_names.append(column_names[element])
        if element_index:
            other_conn_list = conn_list[:, element_index]
            other_conn_list.dtype.names = other_element_column_names

        # hand over split data
        return source_destination_conn_list, weights, delays, other_conn_list

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
