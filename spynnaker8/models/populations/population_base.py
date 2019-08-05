# Copyright (c) 2017-2019 The University of Manchester
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division
import logging
from six import add_metaclass, itervalues
from spinn_utilities.abstract_base import (
    AbstractBase, abstractmethod, abstractproperty)

logger = logging.getLogger(__name__)


@add_metaclass(AbstractBase)
class PopulationBase(object):
    """ Shared methods between Populations and Population views.

    Mainly pass through and not implemented
    """
    __slots__ = []

    @property
    def local_cells(self):
        """ An array containing the cell IDs of those neurons in the\
            Population that exist on the local MPI node.
        """
        logger.warning("local calls do not really make sense on sPyNNaker so "
                       "local_cells just returns all_cells")
        return self.all_cells

    @abstractproperty
    def all_cells(self):
        """ An array containing the cell IDs of all neurons in the\
            Population (all MPI nodes).
        """

    def __add__(self, other):
        """ A Population / PopulationView can be added to another\
            Population, PopulationView or Assembly, returning an Assembly.
        """
        raise NotImplementedError  # pragma: no cover

    def getSpikes(self, *args, **kwargs):
        """
        .. warning::
            Deprecated. Use `get_data('spikes')` instead.
        """
        logger.warning(
            'getSpikes is deprecated. Call transfered to get_data("spikes") '
            'without additional arguments')
        return self.get_data("spikes")

    @abstractmethod
    def get_data(self, variables='all', gather=True, clear=False):
        """ Return a Neo Block containing the data(spikes, state variables)\
            recorded from the Population.

        :param variables: either a single variable name or a list of variable\
            names. Variables must have been previously recorded,\
            otherwise an Exception will be raised.
        :param gather: For parallel simulators, if this is True, all data will\
            be gathered to all nodes and the Neo Block will contain data\
            from all nodes. Otherwise, the Neo Block will contain only data\
            from the cells simulated on the local node.
        :param clear: If this is True, recorded data will be deleted from the\
            Population.
        """

    def get_gsyn(self, *args, **kwargs):
        """
        .. warning::
            Deprecated. Use `get_data(['gsyn_exc', 'gsyn_inh'])` instead.
        """
        logger.warning(
            'get_gsy is deprecated. '
            'Call transfered to get_data(["gsyn_exc", "gsyn_inh"]) '
            'without additional arguements')
        return self.get_data(['gsyn_exc', 'gsyn_inh'])

    @abstractmethod
    def get_spike_counts(self, gather=True):
        """ Returns a dict containing the number of spikes for each neuron.

        The dict keys are neuron IDs, not indices.
        """

    def get_v(self, *args, **kwargs):
        """
        .. warning::
            Deprecated. Use `get_data('v')` instead.
        """
        logger.warning(
            'getSpikes is deprecated. '
            'Call transfered to get_data("v") without additional arguements')
        return self.get_data("v")

    def inject(self, current_source):
        """ Connect a current source to all cells in the Population.
        """
        # TODO:
        raise NotImplementedError  # pragma: no cover

    def is_local(self, id):  # @ReservedAssignment
        """ Indicates whether the cell with the given ID exists on the\
            local MPI node.
        """
        logger.warning("local calls do not really make sense on sPyNNaker so "
                       "is_local always returns True")
        return True

    @property
    def local_size(self):
        """ Return the number of cells in the population on the local MPI node.
        """
        logger.warning("local calls do not really make sense on sPyNNaker so "
                       "is_local always returns size")
        return len(self)

    def meanSpikeCount(self, *args, **kwargs):
        """
        .. warning::
            Deprecated. Use `mean_spike_count()` instead.
        """
        logger.warning(
            'meanSpikeCount is deprecated. '
            'Call transfered to mean_spike_count with additional arguements')
        return self.mean_spike_count(*args, **kwargs)

    def mean_spike_count(self, gather=True):
        """ Returns the mean number of spikes per neuron.
        """
        counts = self.get_spike_counts()
        return sum(itervalues(counts)) / len(counts)

    def nearest(self, position):
        """ Return the neuron closest to the specified position.
        """
        raise NotImplementedError  # pragma: no cover

    @property
    def position_generator(self):
        """
        .. warning::
            NO PyNN description of this method.
        """
        raise NotImplementedError   # pragma: no cover

    @property
    def positions(self):
        """
        .. warning::
            NO PyNN description of this method.
        """
        raise NotImplementedError   # pragma: no cover

    @abstractmethod
    def write_data(self, io, variables='all', gather=True, clear=False,
                   annotations=None):
        """ Write recorded data to file, using one of the file formats\
            supported by Neo.

        :param io: \
            a Neo IO instance, or a string for where to put a Neo instance
        :type io: neo instance or str
        :param variables: \
            either a single variable name or a list of variable names.\
            Variables must have been previously recorded, otherwise an\
            Exception will be raised.
        :type variables: str or list(str)
        :param gather: pointless on sPyNNaker
        :param clear: \
            clears the storage data if set to true after reading it back
        :param annotations: annotations to put on the Neo block
        """
        # pylint: disable=too-many-arguments

    def printSpikes(self, filename, gather=True):
        """
        .. warning::
            Deprecated. Use `write_data(file, 'spikes')` instead.

        .. note::
            Method signature is the PyNN0.7 one
        """
        logger.warning(
            'printSpikes is deprecated. '
            'Call transfered to write_data(file, "spikes", gatherer) instead.')
        self.write_data(filename, 'spikes', gather=True)

    def print_gsyn(self, filename, gather=True):
        """
        .. warning::
            Deprecated. Use `write_data(file, ['gsyn_exc', 'gsyn_inh'])`\
            instead.

        .. note::
            Method signature is the PyNN0.7 one
        """
        logger.warning(
            'print_gsyn is deprecated. Call transfered to '
            'write_data(file, ["gsyn_exc", "gsyn_inh"], gatherer) instead.')
        self.write_data(filename, ['gsyn_exc', 'gsyn_inh'], gather=True)

    def print_v(self, filename, gather=True):
        """
        .. warning::
            Deprecated. Use `write_data(file, 'v')` instead.

        .. note::
            Method signature is the PyNN0.7 one
        """
        logger.warning(
            'print_v is deprecated. '
            'Call transfered to write_data(file, "v", gatherer) instead.')
        self.write_data(filename, 'v', gather=True)

    def receptor_types(self):
        """ NO PyNN description of this method.
        """
        raise NotImplementedError   # pragma: no cover

    @abstractmethod
    def record(self, variables, to_file=None, sampling_interval=None,
               indexes=None):
        """ Record the specified variable or variables for all cells in the\
            Population or view.

        :param variables: either a single variable name or a list of variable\
            names. For a given celltype class, `celltype.recordable` contains\
            a list of variables that can be recorded for that celltype.
        :type variables: str or list(str)
        :param to_file: a file to automatically record to (optional).\
            `write_data()` will be automatically called when `end()` is called.
        :type to_file: a Neo IO instance
        :param sampling_interval: a value in milliseconds, and an integer\
            multiple of the simulation timestep.
        """

    def record_gsyn(self, sampling_interval=1, indexes=None, to_file=None):
        """
        .. warning::
            Deprecated. Use `record(['gsyn_exc', 'gsyn_inh'])` instead.

        .. note::
            Method signature is the PyNN 0.7 one\
            with the extra non-PyNN `sampling_interval` and `indexes`
        """
        logger.warning(
            'record_gsyn is deprecated. Call transfered to '
            'record(["gsyn_exc", "gsyn_inh"], tofile) instead.')
        return self.record(
            ['gsyn_exc', 'gsyn_inh'], to_file=to_file,
            sampling_interval=sampling_interval, indexes=indexes)

    def record_v(self, sampling_interval=1, indexes=None, to_file=None):
        """
        .. warning::
            Deprecated. Use `record('v')` instead.

        .. note::
            Method signature is the PyNN 0.7 one\
            with the extra non-PyNN `sampling_interval` and `indexes`
        """
        logger.warning('record_v is deprecated. '
                       'Call transfered to record(["v"], .....) instead.')
        return self.record(
            'v', to_file=to_file,
            sampling_interval=sampling_interval, indexes=indexes)

    def rset(self, *args, **kwargs):
        """
        .. warning::
            Deprecated. Use `set(parametername=rand_distr)` instead.
        """
        raise NotImplementedError(
            " Use set(parametername=rand_distr) instead.")   # pragma: no cover

    def save_positions(self, file):
        """ Save positions to file. The output format is index x y z
        """
        raise NotImplementedError   # pragma: no cover

    @property
    def structure(self):
        """ The spatial structure of the parent Population.
        """
        raise NotImplementedError   # pragma: no cover

    def tset(self, *args, **kwargs):
        """
        .. warning::
            Deprecated. Use `set(parametername=value_array)` instead.
        """
        raise NotImplementedError(
            "Use set(parametername=value_array) instead.")   # pragma: no cover
