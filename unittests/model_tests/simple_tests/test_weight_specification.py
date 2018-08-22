import spynnaker8 as p
import numpy
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

p.setup(0.1) # set simulation timestep (ms)
runtime = 200


# Post-synapse population
neuron_params = {
#     "v_thresh": -50,
#     "v_reset": -70,
    "i_offset": 0,
                 }

# pop_exc = p.Population(1, p.Izhikevich(**neuron_params),  label="LIF Neuron")

pop_exc = p.Population(1, p.extra_models.IFCurrCombExp2E2I(**neuron_params),  label="LIF Neuron")


spike_times = [1] # 15, 17, 19, 21]
# Spike source to send spike via synapse
pop_src1 = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': spike_times}, label="src1")


# Learning Parameters:
accDecayPerSecond      = 1.0
# Excitatory:
potentiationRateExcit  = 1.0 # was 0.5 # 1.0 # SD! was 0.8
accPotThresholdExcit   = 6 # was 6
depressionRateExcit    = 0.0 # was 0.11 # 0.0  # was 0.4
accDepThresholdExcit   = -6
meanPreWindowExcit     = 12.0 # 8
meanPostWindowExcit    = 8.0 # 8
maxWeightExcit         = 0.5 # was 0.175
minWeightExcit         = 0.00
# Excitatory2:
potentiationRateExcit2 = 0.0 # 1.0 # SD! was 0.8
accPotThresholdExcit2  = 7
depressionRateExcit2   = 0.0 # was 0.11 # 0.0  # was 0.4
accDepThresholdExcit2  = -7
meanPreWindowExcit2    = 11.0 # 8
meanPostWindowExcit2   = 12.0 # 8
maxWeightExcit2        = 31.00
minWeightExcit2        = 0.00
# Inhibitory:
potentiationRateInhib  = 9.0
accPotThresholdInhib   = 7
depressionRateInhib    = 10.0
accDepThresholdInhib   = -7
meanPreWindowInhib     = 6.0
meanPostWindowInhib    = 7.0
maxWeightInhib         = 0.00  # was 0.1
minWeightInhib         = 0.00
# Inhibitory2:
potentiationRateInhib2 = 13.0
accPotThresholdInhib2  = 7
depressionRateInhib2   = 14.0
accDepThresholdInhib2  = -7
meanPreWindowInhib2    = 10.0
meanPostWindowInhib2   = 10.0
inhib2PotIncrement     = 0.0
inhib2DepDecrement     = 0.0


maxWeightInhib2        = 0.0  # was 0.1
minWeightInhib2        = 0.






stdp_model = p.STDPMechanism(
    timing_dependence=p.extra_models.TimingDependenceCyclic(accum_decay = accDecayPerSecond,
            accum_dep_thresh_excit  = accDepThresholdExcit, accum_pot_thresh_excit  = accPotThresholdExcit,
               pre_window_tc_excit  = meanPreWindowExcit,     post_window_tc_excit  = meanPostWindowExcit,
            accum_dep_thresh_excit2 = accDepThresholdExcit2, accum_pot_thresh_excit2 = accPotThresholdExcit2,
               pre_window_tc_excit2 = meanPreWindowExcit2,     post_window_tc_excit2 = meanPostWindowExcit2,
            accum_dep_thresh_inhib  = accDepThresholdInhib, accum_pot_thresh_inhib  = accPotThresholdInhib,
               pre_window_tc_inhib  = meanPreWindowInhib,     post_window_tc_inhib  = meanPostWindowInhib,
            accum_dep_thresh_inhib2 = accDepThresholdInhib2, accum_pot_thresh_inhib2 = accPotThresholdInhib2,
               pre_window_tc_inhib2 = meanPreWindowInhib2,     post_window_tc_inhib2 = meanPostWindowInhib2),
    weight_dependence = p.extra_models.WeightDependenceCyclic(w_min_excit = minWeightExcit, w_max_excit = maxWeightExcit, A_plus_excit = potentiationRateExcit, A_minus_excit = depressionRateExcit,
       w_min_excit2 = minWeightExcit2, w_max_excit2 = maxWeightExcit2, A_plus_excit2 = potentiationRateExcit2, A_minus_excit2 = depressionRateExcit2,
       w_min_inhib = minWeightInhib, w_max_inhib = maxWeightInhib, A_plus_inhib = potentiationRateInhib, A_minus_inhib = depressionRateInhib,
       w_min_inhib2 = minWeightInhib2, w_max_inhib2 = maxWeightInhib2, A_plus_inhib2 = potentiationRateInhib2, A_minus_inhib2 = depressionRateInhib2),
    weight = 1.0, delay = 3)

proj = p.Projection(pop_src1, pop_exc, p.OneToOneConnector(), receptor_type='excitatory', synapse_type=stdp_model)



# Create projection
synapse = p.Projection(
    pop_src1, pop_exc, p.OneToOneConnector(0.6),
    p.StaticSynapse(weight=2, delay=10), receptor_type="excitatory")

pop_exc.record("all")
p.run(runtime)
weights = []

weights.append(proj.get(attribute_names=['weight'], format='list'))

print "Weight = {}".format(weights[0])