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
from pyNN import common as pynn_common
from spinn_front_end_common.utilities import globals_variables
from .population_view import PopulationView
from .population import Population

logger = logging.getLogger(__name__)


class Assembly(pynn_common.Assembly):

    @property
    def _simulator(self):
        return globals_variables.get_simulator()

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
            if not element in self.populations:
                self.populations.append(element)
            else:
                logging.warning('Adding a Population twice in an Assembly is not possible')
