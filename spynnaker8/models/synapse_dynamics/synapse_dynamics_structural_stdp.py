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

from pyNN.standardmodels.synapses import StaticSynapse as PyNNStaticSynapse
from spynnaker.pyNN.models.neuron.synapse_dynamics \
    import SynapseDynamicsStructuralSTDP as STDPStructuralBaseClass
from spynnaker.pyNN.models.neuron.synapse_dynamics \
    import SynapseDynamicsStructuralCommon as CommonSP
from spinn_front_end_common.utilities import globals_variables


class SynapseDynamicsStructuralSTDP(STDPStructuralBaseClass):

    __slots__ = []

    def __init__(
            self, partner_selection, formation, elimination,
            timing_dependence=None, weight_dependence=None,
            voltage_dependence=None, dendritic_delay_fraction=1.0,
            f_rew=CommonSP.DEFAULT_F_REW,
            initial_weight=CommonSP.DEFAULT_INITIAL_WEIGHT,
            initial_delay=CommonSP.DEFAULT_INITIAL_DELAY,
            s_max=CommonSP.DEFAULT_S_MAX, seed=None,
            weight=PyNNStaticSynapse.default_parameters['weight'], delay=None,
            backprop_delay=True):
        """
        :param partner_selection: The partner selection rule
        :type partner_selection: \
            ~spynnaker.pyNN.models.neuron.structural_plasticity.synaptogenesis.partner_selection.AbstractPartnerSelection
        :param formation: The formation rule
        :type formation: \
            ~spynnaker.pyNN.models.neuron.structural_plasticity.synaptogenesis.formation.AbstractFormation
        :param elimination: The elimination rule
        :type elimination: \
            ~spynnaker.pyNN.models.neuron.structural_plasticity.synaptogenesis.elimination.AbstractElimination
        :param timing_dependence:
        :type timing_dependence: \
            ~spynnaker.pyNN.models.neuron.plasticity.stdp.timing_dependence.AbstractTimingDependence
        :param weight_dependence:
        :type weight_dependence: \
            ~spynnaker.pyNN.models.neuron.plasticity.stdp.weight_dependence.AbstractWeightDependence
        :param voltage_dependence: The STDP voltage dependence (unsupported)
        :type voltage_dependence: None
        :param dendritic_delay_fraction: The STDP dendritic delay fraction
        :type dendritic_delay_fraction: float
        :param f_rew: How many rewiring attempts will be done per second.
        :type f_rew: int
        :param initial_weight: Weight assigned to a newly formed connection
        :type initial_weight: float
        :param initial_delay:\
            Delay assigned to a newly formed connection; a single value means\
            a fixed delay value, or a tuple of two values means the delay will\
            be chosen at random from a uniform distribution between the given\
            values
        :type initial_delay: float or tuple(float, float)
        :param s_max: Maximum fan-in per target layer neuron
        :type s_max: int
        :param seed: seed the random number generators
        :type seed: int
        :param weight: The weight of connections formed by the connector
        :type weight: float
        :param delay: The delay of connections formed by the connector
        :type delay: float or None
        """

        # move data from timing to weight dependence over as needed to reflect
        # standard structure underneath
        a_plus = timing_dependence.A_plus
        a_minus = timing_dependence.A_minus
        weight_dependence.set_a_plus_a_minus(a_plus=a_plus, a_minus=a_minus)

        if delay is None:
            delay = globals_variables.get_simulator().min_delay

        STDPStructuralBaseClass.__init__(
            self, partner_selection, formation, elimination,
            timing_dependence=timing_dependence,
            weight_dependence=weight_dependence,
            voltage_dependence=voltage_dependence,
            dendritic_delay_fraction=dendritic_delay_fraction, f_rew=f_rew,
            initial_weight=initial_weight, initial_delay=initial_delay,
            s_max=s_max, seed=seed, weight=weight, delay=delay,
            backprop_delay=backprop_delay)
