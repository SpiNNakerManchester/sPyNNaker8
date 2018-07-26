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
clamps_voltage = numpy.arange(-55,-105,-5)
clamps_number = len(clamps_voltage)
# Spike source to send spike via plastic synapse
AMPA_src = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': [runtime/10,8 * runtime/10]}, label="src1")

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

# begin implementation of sodium current


def sodium_additional_input_get_input_value_as_current(membrane_voltage):
    g_NaP = 0.007
    m_inf = 1 / (1 + np.exp(-(membrane_voltage+55.7) * 0.12987))
    I_NaP = g_NaP * m_inf * m_inf * m_inf * (membrane_voltage - 45)
    return I_NaP

I_NaP =[[] for clamp in range(clamps_number)]

for clamp in range(clamps_number):
    for time in np.arange(0, runtime, dt):
        if time >  runtime/10 + 2 and time < 3+runtime * 8 /10:
                membrane_voltage = clamps_voltage[clamp]
        else: 
            membrane_voltage = hold_voltage
        current = sodium_additional_input_get_input_value_as_current( membrane_voltage)
        I_NaP[clamp].append(current )

new = map(lambda x: x.magnitude.flatten(), clamps)
plt.subplot(1, 2, 1)
plt.plot(np.transpose(I_NaP[0]), color='black', linestyle='dotted', label='Floating-point')
plt.plot(np.transpose(new[0]), color='black', linestyle='dashed', label='SpiNNaker Fixed-point')
plt.plot(np.transpose(I_NaP), linestyle='dotted')
plt.plot(np.transpose(new), linestyle='dashed')
plt.legend(loc='lower right');
plt.xlabel('Time (ms)');
plt.ylabel('I_NaP (mV)');
plt.title('I_NaP current')
#plt.show()
plt.subplot(1, 2, 2)
plt.plot(np.transpose(new)-np.transpose(I_NaP), linestyle='solid')
plt.xlabel('Time (ms)');
plt.ylabel('I_NaP (mV)');
plt.title('difference (error)')
plt.show()

#end simulator
p.end()

print('-->> this simulation was ran using test_sodium_current.py')

