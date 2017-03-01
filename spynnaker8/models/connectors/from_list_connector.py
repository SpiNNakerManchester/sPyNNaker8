from spynnaker.pyNN.models.neural_projections.connectors. \
    from_list_connector import FromListConnector as CommonFromListConnector
import numpy
from spynnaker8.utilities import exceptions


class FromListConnector(CommonFromListConnector):
    """ Make connections according to a list.
    """

    def __init__(
            self, conn_list, safe=True, verbose=False, column_names=None,
            callback=None):
        """Creates a new FromListConnector.
        :param: conn_list:
            a list of tuples, one tuple for each connection. Each tuple
            should contain: (pre_idx, post_idx, p1, p2, ..., pn) where pre_idx
            is the index (i.e. order in the Population, not the ID) of the
             presynaptic neuron, post_idx is the index of the postsynaptic
             neuron, and p1, p2, etc. are the synaptic parameters (e.g.
             weight, delay, plasticity parameters).
        :param column_names:
            the names of the parameters p1, p2, etc. If not provided, it is
             assumed the parameters are weight, delay (for
             backwards compatibility).
        :param safe:
            if True, check that weights and delays have valid values. If
            False, this check is skipped.
        :param callback:
            if True, display a progress bar on the terminal.
        """

        temp_conn_list = numpy.array(conn_list)
        extra_data = dict()

        n_columns = 0
        if len(temp_conn_list) > 0:
            n_columns = temp_conn_list.shape[1]

        if column_names is None:
            if n_columns == 2:
                new_conn_list = list()
                for element in conn_list:
                    new_conn_list.append((element[0], element[1], 0, 1))
                conn_list = new_conn_list
            elif n_columns != 4:
                raise TypeError("Argument 'column_names' is required.")
        else:
            # separate conn list to pre, source, weight, delay and the
            # other things
            conn_list, extra_data = self._split_conn_list(
                conn_list, column_names)

        # store other data for future
        self._extra_conn_data = extra_data

        self._verify_extra_data_meets_constraints()

        # build common from list
        CommonFromListConnector.__init__(
            self, conn_list=conn_list, safe=safe, verbose=verbose)

    def _verify_extra_data_meets_constraints(self):
        for data_key in self._extra_conn_data.keys():
            first_data = None
            for (_, _, data) in self._extra_conn_data[data_key]:
                if first_data is None:
                    first_data = data
                elif data != first_data:
                    raise exceptions.InvalidParameterType(
                        "The parameter {} needs top have a consistent value"
                            .format(data_key))

    @staticmethod
    def _split_conn_list(conn_list, column_names):
        new_conn_list = list()
        other_conn_list = dict()

        # locate weights and delays
        weight_index = column_names.index("weight") + 2
        delay_index = column_names.index("delay") + 2
        element_index = range(2, len(column_names) + 2)

        # figure out where other stuff is
        element_index.remove(weight_index)
        element_index.remove(delay_index)

        # build new conn list
        for element in conn_list:
            new_conn_list.append(
                (element[0], element[1], element[weight_index],
                 element[delay_index]))

        # build other data conn list
        for element in conn_list:
            data_element = list()
            for index in element_index:
                other_conn_list[column_names[index - 2]] = list()
                other_conn_list[column_names[index - 2]].append(
                    (element[0], element[1], element[index]))

        return new_conn_list, other_conn_list
