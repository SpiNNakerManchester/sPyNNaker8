import spynnaker8 as p
import numpy
import numpy as np
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt
from matplotlib import cm

dt=1.0
p.setup(timestep=dt)
runtime = 300
clamps_voltage = numpy.arange(-55,-105,-2)
clamps_number = len(clamps_voltage)

# Spike source to send spike via plastic synapse
AMPA_src = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': [0.5*runtime/10, 2.5 * runtime/10]}, label="src1")

clamp_pops = []
# Post-synapse population
for i in range(clamps_number):
    pop_exc = p.Population(1, p.extra_models.HillTononi(), label="population %d"%i) 
    pop_exc.set(v_reset = clamps_voltage[i])
    clamp_pops.append(pop_exc)

# # Create projections
    synapse = p.Projection(
        AMPA_src, clamp_pops[i], p.AllToAllConnector(),
        p.StaticSynapse(weight=25, delay=1), receptor_type="AMPA")
    clamp_pops[i].record("all")

p.run(runtime)

exc_data = []
for i in range(clamps_number):
    exc_data.append(clamp_pops[i].get_data())
    print "Post-synaptic neuron firing frequency: {} Hz".format(
        len(exc_data[i].segments[0].spiketrains[0]))

clamps = []
for i in range(clamps_number):
    clamps.append(exc_data[i].segments[0].filter(name='gsyn_inh')[0])

# begin simulation of floating point Ih
hold_voltage = -65.0

def calcium_additional_input_get_input_value_as_current(m, h, membrane_voltage):
    g_T = 0.003
    m_inf = 1 / (1 + np.exp(-(membrane_voltage+59) * 0.16129))
    h_inf = 1 / (1 + np.exp((membrane_voltage + 83.0)*0.25))
    e_to_t_on_tau_m = np.exp(-1.0 / (0.13 + 0.22 / (np.exp(-0.05988 * (membrane_voltage+132)) + np.exp(0.054945 * (membrane_voltage + 16.8)))))
    e_to_t_on_tau_h = np.exp(-1.0 / (8.2 + (56.6 + 0.27 * np.exp((membrane_voltage + 115.2) * 0.2)) / (1.0 + np.exp((membrane_voltage + 86.0) * 0.3125))))
    m = m_inf + (m - m_inf) * e_to_t_on_tau_m
    h = h_inf + (h - h_inf) * e_to_t_on_tau_h
    I_T = g_T * m * m * h * (membrane_voltage - 120.);
    return m, h, I_T

I_T =[[] for clamp in range(clamps_number)]

for clamp in range(clamps_number):
    m = 1 / (1 + np.exp(-(hold_voltage+59) * 0.16129)) 
    h = 1 / (1 + np.exp((hold_voltage + 83.0) * 0.25))
    for time in np.arange(0, runtime, dt):
        if time >  0.5 * runtime/10 + 2 and time < 4+runtime * 2.5 /10:
                membrane_voltage = clamps_voltage[clamp]
        else: 
            membrane_voltage = hold_voltage
        m, h, current = calcium_additional_input_get_input_value_as_current(m, h, membrane_voltage)
        I_T[clamp].append(current )

new = map(lambda x: x.magnitude.flatten(), clamps)

plt.subplot(1, 2, 1)
plt.plot(np.transpose(I_T[0]), color='black', linestyle='dotted', label='Floating-point')
plt.plot(np.transpose(new[0]), color='black', linestyle='dashed', label='SpiNNaker Fixed-point')
plt.plot(np.transpose(I_T), linestyle='dotted')
plt.plot(np.transpose(new), linestyle='dashed')
plt.legend(loc='lower right');
plt.xlabel('Time (ms)');
plt.ylabel('I_T (mV)');
plt.title('I_T current')
plt.subplot(1, 2, 2)
plt.plot(np.transpose(new)-np.transpose(I_T), linestyle='solid')
plt.xlabel('Time (ms)');
plt.ylabel('I_T (mV)');
plt.title('I_T current')
plt.show()

#Figure(
#    # plot data for postsynaptic neuron
#    Panel(*clamps, ylabel='Pacemaker Intrinsic Current (?)', xlabel='time (ms)', data_labels = [clamp_pops[i].label for i in range(clamps_number)], yticks=True, xlim=(0,runtime)),
#    annotations="Post-synaptic neuron firing frequency: {} Hz".format(1)
#    
#)
#plt.show()

#end simulator
p.end()
print('-->> this simulation was ran using test_calcium_current.py <<--' )
