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

import logging
try:
    basestring
except NameError:
    basestring = str

from spinn_front_end_common.utilities import globals_variables
from .population_view import PopulationView
from .population import Population

logger = logging.getLogger(__name__)


class Assembly(object):
    """
    A group of neurons, may be heterogeneous, in contrast to a Population where
    all the neurons are of the same type.

    Arguments:
        populations:
            Populations or PopulationViews
        kwargs:
            May contain a keyword argument 'label'
    """

    __slots__ = ("__label", "__populations")

    __count = 0

    #@property
    #def _simulator(self):
    #    return globals_variables.get_simulator()

    def __init__(self, *populations, **kwargs):
        """
        Create an Assembly of Populations and/or PopulationViews.
        """
        if kwargs:
            assert list(kwargs.keys()) == ['label']
        self.__populations = []
        for p in populations:
            self._insert(p)
        self.__label = kwargs.get('label', 'assembly%d' % Assembly.__count)
        assert isinstance(self.__label, basestring), \
            "label must be a string or unicode"
        Assembly.__count += 1

    def __add__(self, other):
        """
        An Assembly may be added to a Population, PopulationView or Assembly
        with the '+' operator, returning a new Assembly, e.g.::

            a2 = a1 + p
        """
        if isinstance(other, Population):
            return self.__class__(*(self.__populations + [other]))
        elif isinstance(other, Assembly):
            return self.__class__(*(self.__populations + other.__populations))
        else:
            raise TypeError(
                "can only add a Population or another Assembly to an Assembly")

    def __repr__(self):
        return "Assembly(*%r, label=%r)" % (self.populations, self.label)

    def __len__(self):
        """Return the total number of cells in the population (all nodes)."""
        return self.size

    @property
    def size(self):
        return sum(p.size for p in self.__populations)

    @property
    def populations(self):
        return self.__populations

    @property
    def label(self):
        return self.__label

    def _insert(self, element):
        if isinstance(element, PopulationView):
            #if not element.parent in self.populations:
            #    double = False
            #    for p in self.populations:
            #        data = numpy.concatenate((p.all_cells, element.all_cells))
            #        if len(numpy.unique(data)) != len(p.all_cells) + len(element.all_cells):
            #            logging.warning('Adding a PopulationView to an Assembly containing elements already present is not posible')
            #            double = True  # Should we automatically remove duplicated IDs ?
            #            break
            #    if not double:
            #        self.populations.append(element)
            #else:
            #    logging.warning('Adding a PopulationView to an Assembly when parent Population is there is not possible')
            raise NotImplementedError(
                "Adding views to Assemblies not yet suppurted")
        if isinstance(element, Population):
            if not element in self.__populations:
                self.__populations.append(element)
            else:
                logging.warning('Adding a Population twice in an Assembly is not possible')
