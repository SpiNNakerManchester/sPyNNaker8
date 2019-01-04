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
runtime = 10000
clamps_voltage = numpy.arange(-55,-105,-5)
clamps_number = len(clamps_voltage)
clamp_protocol = [[-65.0, clamps_voltage[i], -65.0 ] for i in range(clamps_number)]
changes = len(clamp_protocol[0])

# Spike source to send spike via plastic synapse
AMPA_src = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': [runtime/10, 6 * runtime/10]}, label="src1")

clamp_pops = []
# Post-synapse population
for i in range(clamps_number):
    pop_exc = p.Population(changes, p.extra_models.HillTononi(), label="population %d"%i) 
    pop_exc.set(v_reset = clamp_protocol[i]) 
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

def additional_input_get_input_value_as_current(m, membrane_voltage):
    g_H = 0.015
    m_inf = 1 / (1 + np.exp((membrane_voltage+75)/5.5))
    e_to_t_on_tau_m = np.exp(-1.0 *
                (np.exp(-14.59 - 0.086 * membrane_voltage)
                 + np.exp(-1.87 + 0.0701 * membrane_voltage)))    
    m_factor = m_inf + (m - m_inf)
    m = m_inf + (m - m_inf) * e_to_t_on_tau_m
    I_H = g_H * m * (membrane_voltage - -43)
    return m, I_H
#    return m, m
#    return m, e_to_t_on_tau_m
#    return m, m_factor
#    return m, m_inf

I_h =[[] for clamp in range(clamps_number)]

for clamp in range(clamps_number):
    m = 1 / (1 + np.exp((hold_voltage + 75) / 5.5))
    for time in np.arange(0, runtime, dt):
        if time >  runtime/10 + 2 and time < 3+runtime * 6 /10:
                membrane_voltage = clamps_voltage[clamp]
        else: 
            membrane_voltage = hold_voltage
        m, current = additional_input_get_input_value_as_current(m, membrane_voltage)
        I_h[clamp].append(current )

new = [map(lambda x: x.magnitude.flatten(), clamps[i]) for i in range(clamps_number)]

plt.subplot(1, 2, 1)
plt.plot(np.transpose(I_h[0]), color='black', linestyle='dotted', label='Floating-point')
plt.plot(np.transpose(new[0])[0], color='black', linestyle='dashed', label='SpiNNaker Fixed-point')
plt.plot(np.transpose(I_h), linestyle='dotted')
plt.plot(np.transpose(new)[0], linestyle='dashed')
plt.legend(loc='lower right');
plt.xlabel('Time (ms)');
plt.ylabel('I_h (mV)');
plt.title('I_h current')
plt.subplot(1, 2, 2)
plt.plot(np.transpose(new)[0] - np.transpose(I_h), linestyle='solid')
plt.xlabel('Time (ms)');
plt.ylabel('I_h (mV)');
plt.title('I_h current')
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

print('-->> this simulation was ran using test_pacemaker_impl_current.py')
