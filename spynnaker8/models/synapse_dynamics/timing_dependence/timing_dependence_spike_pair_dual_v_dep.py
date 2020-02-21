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

from spynnaker.pyNN.models.neuron.plasticity.stdp.timing_dependence import (
    TimingDependenceSpikePairDualVDep as
    _BaseClass)

#_defaults = _BaseClass.default_parameters


class TimingDependenceSpikePairDualVDep(_BaseClass):
    __slots__ = [
        "__a_plus",
        "__a_minus"]

    def __init__(
            self, alpha_exc, alpha_inh, tau_exc=20.0, tau_inh=20.0, A_plus=0.01, A_minus=0.01):
        super(TimingDependenceSpikePairDualVDep, self).__init__(tau_exc=tau_exc, tau_inh=tau_inh,
                                                                  alpha_exc=alpha_exc, alpha_inh=alpha_inh)
        self.__a_plus = A_plus
        self.__a_minus = A_minus

    @property
    def A_plus(self):
        return self.__a_plus

    @A_plus.setter
    def A_plus(self, new_value):
        self.__a_plus = new_value

    @property
    def A_minus(self):
        return self.__a_minus

    @A_minus.setter
    def A_minus(self, new_value):
        self.__a_minus = new_value
