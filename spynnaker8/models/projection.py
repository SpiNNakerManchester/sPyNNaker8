import logging
import numpy

from pyNN import common as pynn_common, recording
from pyNN.space import Space as PyNNSpace

from spynnaker8.models.connectors import FromListConnector
from spynnaker8.models.synapse_dynamics import SynapseDynamicsStatic
from spynnaker8._version import __version__

from spynnaker.pyNN.models.pynn_projection_common import PyNNProjectionCommon
from spinn_front_end_common.utilities import globals_variables
from spynnaker.pyNN.exceptions import InvalidParameterType

from spinn_front_end_common.utilities.exceptions import ConfigurationException
import functools

logger = logging.getLogger(__name__)


class Projection(PyNNProjectionCommon):
    """ spynnaker 8 projection class

    """

    _simulator = None
    _static_synapse_class = SynapseDynamicsStatic

    def __init__(
            self, pre_synaptic_population, post_synaptic_population,
            connector, synapse_type=None, source=None,
            receptor_type=None, space=None, label=None):

        if source is not None:
            raise InvalidParameterType(
                "spynnaker8 {} does not yet support multi-compartmental "
                "cells.".format(__version__))

        # set space object if not set
        if space is None:
            space = PyNNSpace()

        # set the simulator object correctly.
        self._simulator = globals_variables.get_simulator()

        if synapse_type is None:
            synapse_type = SynapseDynamicsStatic()

        # move weights and delays over to the connector to satisfy PyNN 8
        # and 7 compatibility
        connector.set_weights_and_delays(
            synapse_type.weight, synapse_type.delay)
        connector.set_space(space)

        # as a from list connector can have plastic parameters, grab those (
        # if any and add them to the synapse dynamics object)
        if isinstance(connector, FromListConnector):
            synapse_plastic_parameters = connector.get_extra_parameters()
            if synapse_plastic_parameters is not None:
                for parameter in synapse_plastic_parameters.dtype.names:
                    synapse_type.set_value(
                        parameter, synapse_plastic_parameters[:, parameter])

        # set rng if needed
        rng = None
        if hasattr(connector, "rng"):
            rng = connector.rng

        PyNNProjectionCommon.__init__(
            self, connector=connector, synapse_dynamics_stdp=synapse_type,
            target=receptor_type, spinnaker_control=self._simulator,
            pre_synaptic_population=pre_synaptic_population,
            post_synaptic_population=post_synaptic_population, rng=rng,
            machine_time_step=self._simulator.machine_time_step,
            user_max_delay=self._simulator.max_delay, label=label,
            time_scale_factor=self._simulator.time_scale_factor)

    def __len__(self):
        raise NotImplementedError

    def set(self, **attributes):
        raise NotImplementedError

    def get(self, attribute_names, format,  # @ReservedAssignment
            gather=True, with_address=True, multiple_synapses='last'):
        """ get a parameter for pynn 0.8

        :param attribute_names: list of attributes to gather
        :type attribute_names: basestring or iterable of basestring
        :param format: "list" or "array"
        :param gather: gather over all nodes (defaulted to true on spinnaker)
        :param with_address: True if the source and target are to be included
        :param multiple_synapses:\
            What to do with the data if format="array" and if the multiple\
            source-target pairs with the same values exist.  Currently only\
            "last" is supported
        :return: values selected
        """
        if not gather:
            logger.warn("Spynnaker always gathers from every core.")

        return self._get_data(
            attribute_names, format, with_address, multiple_synapses)

    def _get_data(
            self, attribute_names, format,  # @ReservedAssignment
            with_address, multiple_synapses='last',
            notify=None):
        """ Internal data getter to add notify option
        """

        if multiple_synapses != 'last':
            raise ConfigurationException(
                "Spynnaker only recognises multiple_synapses == last")

        # fix issue with 1 versus many
        if isinstance(attribute_names, basestring):
            attribute_names = [attribute_names]

        data_items = list()
        if format != "list":
            with_address = False
        if with_address:
            data_items.append("source")
            data_items.append("target")

        # Split out attributes in to standard versus synapse dynamics data
        fixed_values = list()
        for attribute in attribute_names:
            # if with address set to true, we have decided the end user is
            # being stupid if they request source and/or target then they get
            # it twice
            data_items.append(attribute)
            if attribute not in {"source", "target", "weight", "delay"}:
                value = self._synapse_information.synapse_dynamics.get_value(
                    attribute)
                fixed_values.append((attribute, value))

        # Return the connection data
        return self._get_synaptic_data(
            format == "list", data_items, fixed_values, notify=notify)

    def __iter__(self):
        raise NotImplementedError

    def getWeights(self, format='list',  # @ReservedAssignment
                   gather=True):
        logger.warn("getWeights is deprecated.  Use get('weight') instead")
        return self.get('weight', format, gather, with_address=False)

    def getDelays(self, format='list',  # @ReservedAssignment
                  gather=True):
        logger.warn("getDelays is deprecated.  Use get('delay') instead")
        return self.get('delay', format, gather, with_address=False)

    def getSynapseDynamics(self, parameter_name,
                           format='list',  # @ReservedAssignment
                           gather=True):
        logger.warn(
            "getSynapseDynamics is deprecated.  Use get(parameter_name)"
            " instead")
        return self.get(parameter_name, format, gather, with_address=False)

    def saveConnections(self, file,  # @ReservedAssignment
                        gather=True,
                        compatible_output=True):  # @UnusedVariable
        logger.warn("saveConnections is deprecated.  Use save('all') instead")
        self.save('all', file, format='list', gather=gather)

    def printWeights(self, file, format='list',  # @ReservedAssignment
                     gather=True):
        logger.warn("printWeights is deprecated.  Use save('weight') instead")
        self.save('weight', file, format, gather)

    def printDelays(self, file, format='list',  # @ReservedAssignment
                    gather=True):
        """
        Print synaptic weights to file. In the array format, zeros are printed
        for non-existent connections.
        """
        logger.warn("printDelays is deprecated.  Use save('delay') instead")
        self.save('delay', file, format, gather)

    def weightHistogram(self, min=None, max=None,  # @ReservedAssignment
                        nbins=10):
        """
        Return a histogram of synaptic weights.
        If min and max are not given, the minimum and maximum weights are
        calculated automatically.
        """
        logger.warn(
            "weightHistogram is deprecated.  Use numpy.histogram function"
            " instead")
        pynn_common.Projection.weightHistogram(min=min, max=max, nbins=nbins)

    def _save_callback(
            self, save_file, format,  # @ReservedAssignment
            metadata, data):
        data_file = save_file
        if isinstance(data_file, basestring):
            data_file = recording.files.StandardTextFile(save_file, mode='wb')
        if format == 'array':
            data = [
                numpy.where(numpy.isnan(values), 0.0, values)
                for values in data]
        data_file.write(data, metadata)
        data_file.close()

    def save(
            self, attribute_names, file, format='list',  # @ReservedAssignment
            gather=True, with_address=True):
        """
        Print synaptic attributes (weights, delays, etc.) to file. In the array
        format, zeros are printed for non-existent connections.
        Values will be expressed in the standard PyNN units (i.e. millivolts,
        nanoamps, milliseconds, microsiemens, nanofarads, event per second).
        """

        if attribute_names in ('all', 'connections'):
            attribute_names = \
                self._projection_edge.post_vertex.synapse_dynamics.\
                get_parameter_names()
        metadata = {"columns": attribute_names}
        if with_address:
            metadata["columns"] = ["i", "j"] + list(metadata["columns"])
        self._get_data(
            attribute_names, format, gather, with_address,
            notify=functools.partial(
                self._save_callback, args=[file, format, metadata]))

    def __repr__(self):
        return "projection {}".format(self._projection_edge.label)
