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

import scipy.stats
from spinn_utilities.overrides import overrides
from spynnaker.pyNN.utilities.random_stats import AbstractRandomStats


class RandomStatsScipyImpl(AbstractRandomStats):
    """ A Random Statistics object that uses scipy directly
    """

    def __init__(self, distribution_type):
        self._scipy_stats = getattr(scipy.stats, distribution_type)

    @overrides(AbstractRandomStats.cdf)
    def cdf(self, dist, v):
        return self._scipy_stats.cdf(v, *dist.parameters)

    @overrides(AbstractRandomStats.ppf)
    def ppf(self, dist, p):
        return self._scipy_stats.ppf(p, *dist.parameters)

    @overrides(AbstractRandomStats.mean)
    def mean(self, dist):
        return self._scipy_stats.mean(*dist.parameters)

    @overrides(AbstractRandomStats.std)
    def std(self, dist):
        return self._scipy_stats.std(*dist.parameters)

    @overrides(AbstractRandomStats.var)
    def var(self, dist):
        return self._scipy_stats.var(*dist.parameters)

    @overrides(AbstractRandomStats.high)
    def high(self, dist):
        if "high" in dist.parameters:
            return dist.parameters['high']
        return None

    @overrides(AbstractRandomStats.low)
    def low(self, dist):
        if "low" in dist.parameters:
            return dist.parameters['low']
        return None
