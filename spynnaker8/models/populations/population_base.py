import logging
from pyNN import random
import numpy
from six import add_metaclass
from spinn_utilities.abstract_base import AbstractBase, abstractmethod, \
    abstractproperty

logger = logging.getLogger(__name__)


@add_metaclass(AbstractBase)
class PopulationBase(object):
    """ Shared methods between Populations and Poluation views.

    Mainly pass through and not implemented

    """

    @property
    def local_cells(self):
        """
        An array containing the cell ids of those neurons in the Population
            that exist on the local MPI node.
        """
        logger.warning("local calls do not really make sense on sPyNNaker so "
                       "local_cells just returns all_cells")
        return self.all_cells

    @abstractproperty
    def all_cells(self):
        """  An array containing the cell ids of all neurons in the
            Population(all MPI nodes). """

    def __add__(other):
        """ A Population / PopulationView can be added to another
            Population, PopulationView or Assembly, returning an Assembly.
        """
        raise NotImplementedError

    def getSpikes(self, *args, **kwargs):
        """ Deprecated.Use get_data('spikes') instead. """
        if len(args) > 0:
            raise NotImplementedError('Use get_data("spikes") instead')
        if len(kwargs) > 0:
            raise NotImplementedError('Use get_data("spikes") instead')
        return self.get_data("spikes")

    @abstractmethod
    def get_data(self, variables='all', gather=True, clear=False):
        """
        Return a Neo Block containing the data(spikes, state variables)
            recorded from the Population.

        variables - either a single variable name or a list of variable names

        Variables must have been previously recorded,
            otherwise an Exception will be raised.

        For parallel simulators, if gather is True, all data will be
            gathered to all nodes and the Neo Block will contain data
            from all nodes.
        Otherwise, the Neo Block will contain only data from the cells
            simulated on the local node.

        If clear is True, recorded data will be deleted from the Population.
        """

    def get_gsyn(self, *args, **kwargs):
        """ Deprecated.Use get_data(['gsyn_exc', 'gsyn_inh']) instead."""
        if len(args) > 0:
            raise NotImplementedError(
                "Use get_data(['gsyn_exc', 'gsyn_inh']) instead")
        if len(kwargs) > 0:
            raise NotImplementedError(
                "Use get_data(['gsyn_exc', 'gsyn_inh']) instead")
        return self.get_data(['gsyn_exc', 'gsyn_inh'])

    @abstractmethod
    def get_spike_counts(self, gather=True):
        """ Returns a dict containing the number of spikes for each neuron.

        The dict keys are neuron IDs, not indices.
        """

    def get_v(self, *args, **kwargs):
        """ Deprecated.Use get_data('v') instead. """
        if len(args) > 0:
            raise NotImplementedError('Use get_data("v") instead')
        if len(kwargs) > 0:
            raise NotImplementedError('Use get_data("v") instead')
        return self.get_data("v")

    def inject(self, current_source):
        """ Connect a current source to all cells in the Population."""
        # TODO:
        raise NotImplementedError

    def is_local(self, id):
        """
        Indicates whether the cell with the given ID exists on the
            local MPI node.
        """
        logger.warning("local calls do not really make sense on sPyNNaker so "
                       "is_local always returns True")
        return True

    @property
    def local_size(self):
        """
        Return the number of cells in the population on the local MPI node
        """
        logger.warning("local calls do not really make sense on sPyNNaker so "
                       "is_local always returns size")
        return len(self)

    def meanSpikeCount(self, *args, **kwargs):
        """ Deprecated. Use mean_spike_count() instead. """
        return self.mean_spike_count(*args, **kwargs)

    def mean_spike_count(self, gather=True):
        """ Returns the mean number of spikes per neuron. """
        sum = 0
        counts = self.get_spike_counts()
        for count in counts.itervalues():
            sum += count
        return sum / len(counts)

    def nearest(self, position):
        """ Return the neuron closest to the specified position."""
        raise NotImplementedError

    @property
    def position_generator(self):
        """ NO PyNN description of this method """
        raise NotImplementedError

    @property
    def positions(self):
        """ NO PyNN description of this method """
        raise NotImplementedError

    def printSpikes(self, *args, **kwargs):
        """ Deprecated. Use write_data(file, 'spikes') instead. """
        raise NotImplementedError("Use write_data(file, 'spikes') instead.")

    def print_gsyn(self, *args, **kwargs):
        """
        Deprecated. Use write_data(file, ['gsyn_exc', 'gsyn_inh']) instead.

       """
        raise NotImplementedError(
            "Use write_data(file, ['gsyn_exc', 'gsyn_inh']) instead.")

    def print_v(self, *args, **kwargs):
        """  Deprecated. Use write_data(file, 'v') instead."""
        raise NotImplementedError("Use write_data(file, 'v') instead.")

    def receptor_types(self):
        """ NO PyNN description of this method """
        raise NotImplementedError

    def record_gsyn(self, *args, **kwargs):
        """ Deprecated. Use record(['gsyn_exc', 'gsyn_inh']) instead. """
        if len(args) > 0:
            raise NotImplementedError(
                "Use record(['gsyn_exc', 'gsyn_inh']) instead.")
        if len(kwargs) > 0:
            raise NotImplementedError(
                "Use record(['gsyn_exc', 'gsyn_inh']) instead")
        return self.record(['gsyn_exc', 'gsyn_inh'])

    def record_v(self, *args, **kwargs):
        """ Deprecated. Use record('v') instead. """
        if len(args) > 0:
            raise NotImplementedError(
                "Use record('v') instead.")
        if len(kwargs) > 0:
            raise NotImplementedError(
                "Use record('v']) instead")
        return self.record('v')

    def rset(self, *args, **kwargs):
        """ Deprecated. Use set(parametername=rand_distr) instead. """
        raise NotImplementedError(
            " Use set(parametername=rand_distr) instead.")

    def save_positions(self, file):
        """ Save positions to file. The output format is index x y z """
        raise NotImplementedError

    @property
    def structure(self):
        """ The spatial structure of the parent Population. """
        raise NotImplementedError

    def tset(self, *args, **kwargs):
        """ Deprecated. Use set(parametername=value_array) instead. """
        raise NotImplementedError("Use set(parametername=value_array) instead.")
