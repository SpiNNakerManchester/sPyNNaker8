from spynnaker.pyNN.models.neural_projections.connectors \
    import FromListConnector as CommonFromListConnector
from spynnaker.pyNN.utilities.utility_calls import convert_param_to_numpy
import numpy
from spynnaker8.utilities.exceptions import InvalidParameterType

from pyNN.connectors import Connector


class FromListConnector(CommonFromListConnector, Connector):
    """ Make connections according to a list.
    """
    __slots__ = [
        "_extra_conn_data",
        "_converted_weights_and_delays",
        "_conn_list"]

    def __init__(
            self, conn_list, safe=True, verbose=False, column_names=None,
            callback=None):
        """ Creates a new FromListConnector.

        :param: conn_list: \
            a list of tuples, one tuple for each connection. Each tuple\
            should contain: (pre_idx, post_idx, p1, p2, ..., pn) where\
            pre_idx is the index (i.e. order in the Population, not the ID)\
            of the presynaptic neuron, post_idx is the index of the\
            postsynaptic neuron, and p1, p2, etc. are the synaptic parameters\
            (e.g. weight, delay, plasticity parameters).
        :param column_names: \
            the names of the parameters p1, p2, etc. If not provided, it is\
             assumed the parameters are weight, delay (for\
             backwards compatibility).
        :param safe: \
            if True, check that weights and delays have valid values. If\
            False, this check is skipped.
        :param callback:
            if True, display a progress bar on the terminal.
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

        # supports setting these at different times
#        self._weights = None
#        self._delays = None
        self._converted_weights_and_delays = False

        if column_names is None:
            # if no column names, but more not the expected
            if n_columns == 4:
                column_names = ('pre_idx', 'post_idx', 'weight', 'delay')
                conn_list, weights, delays, self._extra_conn_data = \
                    CommonFromListConnector._split_conn_list(
                        conn_list, column_names)
            elif n_columns != 2:
                raise TypeError("Argument 'column_names' is required.")
        else:
            # separate conn list to pre, source, weight, delay and the
            # other things
            conn_list, weights, delays, self._extra_conn_data = \
                CommonFromListConnector._split_conn_list(
                    conn_list, column_names)

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

#     # replicate the PyNN 0.8 "feature" where the connector overwrites
#     # the weights and delays in the synapse if both are specified
#     def set_weights_and_delays(self, weights, delays):
#         """ allows setting of the weights and delays at separate times to the\
#             init, also sets the dtypes correctly.....
#
#         :param weights:
#         :param delays:
#         :return:
#         """
#         # set the data if not already set (supports none overriding via
#         # synapse data)
#         print("set_weights_and_delays")
#         weight = convert_param_to_numpy(weights, len(self._conn_list))
#         delay = convert_param_to_numpy(delays, len(self._conn_list))
#
#         # if got data, build connlist with correct dtypes
#         if (weight is not None and delay is not None and not
#                 self._converted_weights_and_delays):
#             # add weights and delays to the conn list
#             temp_conn_list = numpy.dstack(
#                 (self._conn_list[:, 0], self._conn_list[:, 1],
#                  weight, delay))[0]
#
#             self._conn_list = list()
#             for element in temp_conn_list:
#                 self._conn_list.append((element[0], element[1], element[2],
#                                         element[3]))
#
#             # set dtypes (cant we just set them within the array?)
#             self._conn_list = numpy.asarray(self._conn_list,
#                                             dtype=self.CONN_LIST_DTYPE)
#             self._converted_weights_and_delays = True
#
#         # send the conn_list to the common connector
#         CommonFromListConnector.set_conn_list(self, self._conn_list)

    def get_extra_parameters(self):
        """ getter for the extra parameters

        :return:
        """
        return self._extra_conn_data

    def _verify_extra_data_meets_constraints(self):
        """ safety check for current impl, stops extra params to be\
            variable per atom

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
