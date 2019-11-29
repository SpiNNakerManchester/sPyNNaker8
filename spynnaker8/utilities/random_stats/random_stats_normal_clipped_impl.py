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

from scipy.stats import truncnorm
from spinn_utilities.overrides import overrides
from spynnaker.pyNN.utilities.random_stats import AbstractRandomStats


class RandomStatsNormalClippedImpl(AbstractRandomStats):
    """ An implementation of AbstractRandomStats for normal distributions that\
        are clipped to a boundary (redrawn)
    """

    def _get_params(self, dist):
        low = ((dist.parameters['low'] - dist.parameters['mu']) /
               dist.parameters['sigma'])
        high = ((dist.parameters['high'] - dist.parameters['mu']) /
                dist.parameters['sigma'])
        return [low, high,
                dist.parameters['mu'], dist.parameters['sigma']]

    @overrides(AbstractRandomStats.cdf)
    def cdf(self, dist, v):
        return truncnorm.cdf(v, *self._get_params(dist))

    @overrides(AbstractRandomStats.ppf)
    def ppf(self, dist, p):
        return truncnorm.ppf(p, *self._get_params(dist))

    @overrides(AbstractRandomStats.mean)
    def mean(self, dist):
        return truncnorm.mean(*self._get_params(dist))

    @overrides(AbstractRandomStats.std)
    def std(self, dist):
        return truncnorm.std(*self._get_params(dist))

    @overrides(AbstractRandomStats.var)
    def var(self, dist):
        return truncnorm.var(*self._get_params(dist))

    @overrides(AbstractRandomStats.high)
    def high(self, dist):
        return dist.parameters['high']

    @overrides(AbstractRandomStats.low)
    def low(self, dist):
        return dist.parameters['low']
