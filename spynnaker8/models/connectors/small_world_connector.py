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

from spynnaker.pyNN.models.neural_projections.connectors import (
    SmallWorldConnector as
    _BaseClass)


class SmallWorldConnector(_BaseClass):
    """ Create a connector that uses connection statistics based on the\
        Small World network connectivity model. Note that this is typically\
        used from a population to itself.
    """
    __slots__ = []

    def __init__(
            self, degree, rewiring, allow_self_connections=True,
            safe=True, verbose=False, n_connections=None):
        """
        :param float degree: the region length where nodes will be connected\
            locally
        :param float rewiring: the probability of rewiring each edge
        :param bool allow_self_connections: \
            if the connector is used to connect a Population to itself, this\
            flag determines whether a neuron is allowed to connect to itself,\
            or only to other neurons in the Population.
        :param bool safe: \
            Whether to check that weights and delays have valid values.\
            If False, this check is skipped.
        :param bool verbose: \
            Whether to output extra information about the connectivity to a\
            CSV file
        :param n_connections: \
            if specified, the number of efferent synaptic connections per\
            neuron
        :type n_connections: int or None
        """
        # pylint: disable=too-many-arguments
        super(SmallWorldConnector, self).__init__(
            degree=degree, rewiring=rewiring,
            allow_self_connections=allow_self_connections,
            safe=safe, verbose=verbose, n_connections=n_connections)
