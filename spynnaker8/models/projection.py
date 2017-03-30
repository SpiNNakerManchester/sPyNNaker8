import logging
import numpy
import deprecation

from pyNN import common as pynn_common
from pyNN.space import Space as PyNNSpace

from spynnaker8 import FromListConnector
from spynnaker8.models.synapse_dynamics.synapse_dynamics_static \
    import SynapseDynamicsStatic
from spynnaker8._version import __version__

from spynnaker.pyNN.models.pynn_projection_common import PyNNProjectionCommon
from spynnaker.pyNN.utilities import globals_variables
from spynnaker.pyNN import exceptions

from spinn_front_end_common.utilities import exceptions as common_exceptions

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
            raise exceptions.InvalidParameterType(
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
                    synapse_type.set(
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

    def get(self, attribute_names, format, gather=True, with_address=False,
            multiple_synapses='sum'):

        if with_address:
            raise common_exceptions.ConfigurationException(
                "Spynnaker only recongises with_address=False")

        # fix issue with 1 vs many
        if isinstance(attribute_names, basestring):
            attribute_names = [attribute_names]

        data_pile = list()

        attribute_names.insert(0, 'source')
        attribute_names.insert(1, 'target')


        # gather all the attributes, but format of pynn is source,
        # destination, attribute. so will need to delete source and dest
        #  from each atrtibute after the first.
        for attribute in attribute_names:
            data_pile.append(PyNNProjectionCommon.get(
                self, attribute, format, gather))

        return numpy.dstack(data_pile)[0]

    def __iter__(self):
        raise NotImplementedError

    @deprecation.deprecated(
        deprecated_in="1.0.0", current_version=__version__,
        details="Use get('weight', format, gather) function instead")
    def getWeights(self, format='list', gather=True):
        return self.get('weight', format, gather, with_address=False)

    @deprecation.deprecated(
        deprecated_in="1.0.0", current_version=__version__,
        details="Use get('delay', format, gather) function instead")
    def getDelays(self, format='list', gather=True):
        return self.get('delay', format, gather, with_address=False)

    @deprecation.deprecated(
        deprecated_in="1.0.0", current_version=__version__,
        details="Use get(parameter_name, format, gather) function instead")
    def getSynapseDynamics(self, parameter_name, format='list', gather=True):
        return self.get(parameter_name, format, gather, with_address=False)

    @deprecation.deprecated(
        deprecated_in="1.0.0", current_version=__version__,
        details="Use save('all', file, format='list', gather=gather) function"
                " instead")
    def saveConnections(self, file, gather=True, compatible_output=True):
        self.save('all', file, format='list', gather=gather)

    @deprecation.deprecated(
        deprecated_in="1.0.0", current_version=__version__,
        details="Use save('weight', file, format, gather) function instead")
    def printWeights(self, file, format='list', gather=True):
        self.save('weight', file, format, gather)

    @deprecation.deprecated(
        deprecated_in="1.0.0", current_version=__version__,
        details="Use save('delay', file, format, gather) function instead")
    def printDelays(self, file, format='list', gather=True):
        """
        Print synaptic weights to file. In the array format, zeros are printed
        for non-existent connections.
        """
        self.save('delay', file, format, gather)

    @deprecation.deprecated(
        deprecated_in="1.0.0", current_version=__version__,
        details="Use numpy.histogram() function instead")
    def weightHistogram(self, min=None, max=None, nbins=10):
        """
        Return a histogram of synaptic weights.
        If min and max are not given, the minimum and maximum weights are
        calculated automatically.
        """
        pynn_common.Projection.weightHistogram(min=min, max=max, nbins=nbins)

    def _get_attributes_as_list(self, names):
        """ internally forced upon us call from pynn. Is getting synaptic data

        :param names: name of the attributes whose values are wanted, or a
        list of such names. an example is ['delay', 'weight']
        :return: a array of tuples, each containing the named data's per
        connection
        """

        logger.info("Downloading synaptic matrices for projection %s",
                    self.label)
        return self._get_synaptic_data(True, names)

    def __repr__(self):
        return "projection {}".format(self._projection_edge.label)
