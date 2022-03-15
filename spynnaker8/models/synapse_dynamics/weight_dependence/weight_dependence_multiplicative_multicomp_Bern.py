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

from spynnaker.pyNN.models.neuron.plasticity.stdp.weight_dependence import (
    WeightDependenceMultiplicativeMulticompBern as
    _BaseClass)


class WeightDependenceMultiplicativeMulticompBern(_BaseClass):
    def __init__(self, w_min=0.0, w_max=1.0, learning_rate=1.0):
        super(WeightDependenceMultiplicativeMulticompBern, self).__init__(
            w_max=w_max, w_min=w_min, learning_rate=learning_rate)