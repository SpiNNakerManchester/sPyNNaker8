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
runtime = 200
clamps_voltage = numpy.arange(-5,-105,-5)
clamps_number = len(clamps_voltage)
# Spike source to send spike via plastic synapse
AMPA_src = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': [runtime/10,5 * runtime/10]}, label="src1")

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

#---- begin implementation of potassium current
def potassium_additional_input_get_input_value_as_current(D, membrane_voltage):
    g_DK = 1.25
    e_to_t_on_tau = 0.367879 
    NaInflux = 0.025 / (1. + np.exp(-(membrane_voltage- -10) * 0.2))
    D_infinity = 1250 * NaInflux + 0.001
    D = D_infinity + (D - D_infinity) * e_to_t_on_tau
    m_inf = 1. / (1. + (0.0078125 /(D**3.5))) 
    I_DK = - g_DK * m_inf * (membrane_voltage - -90)
    return D, I_DK

I_DK =[[] for clamp in range(clamps_number)]

for clamp in range(clamps_number):
    NaInflux = 0.025 / (1 + np.exp(-(hold_voltage - -10) * 0.2))
    D = 1250 * NaInflux + 0.001
    for time in np.arange(0, runtime, dt):
        if time >  runtime/10 + 2 and time < 4+runtime * 5 /10:
                membrane_voltage = clamps_voltage[clamp]
        else: 
            membrane_voltage = hold_voltage
        D, current = potassium_additional_input_get_input_value_as_current(D, membrane_voltage)
        I_DK[clamp].append(current )

new = map(lambda x: x.magnitude.flatten(), clamps)
plt.subplot(1, 2, 1)
plt.plot(np.transpose(I_DK[0]), color='black', linestyle='dotted', label='Floating-point')
plt.plot(np.transpose(new[0]), color='black', linestyle='dashed', label='SpiNNaker Fixed-point')
plt.plot(np.transpose(I_DK), linestyle='dotted')
plt.plot(np.transpose(new), linestyle='dashed')
plt.legend(loc='lower right');
plt.xlabel('Time (ms)');
plt.ylabel('I_DK (mV)');
plt.title('I_DK current')
#plt.show()
plt.subplot(1, 2, 2)
plt.plot(np.transpose(new)-np.transpose(I_DK), linestyle='solid')
plt.xlabel('Time (ms)');
plt.ylabel('I_DK (mV)');
plt.title('I_DK current')
plt.show()


p.end()

print('-->>this simulation was ran using test_potassium_current.py')
