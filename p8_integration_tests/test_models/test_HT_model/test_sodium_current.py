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

# Clamp parameters.
clamps_voltage = numpy.arange(-55,-105,-5)
clamp_start = runtime / 10
clamp_duration = runtime - 2* clamp_start
clamps_number = len(clamps_voltage)

# Spike source to send spike via plastic synapse
# Commented for now because not relevant for voltage clamp results.
#AMPA_src = p.Population(1, p.SpikeSourceArray,
#                        {'spike_times': [runtime/10,8 * runtime/10]}, label="src1")

# Create post-synapse populations, one per clamp voltage.
clamp_pops = []
for i in range(clamps_number):
    pop_exc = p.Population(1, p.extra_models.HillTononi(), label="population %d"%i) 
    pop_exc.set(v_clamp = clamps_voltage[i])
    pop_exc.set(s_clamp = clamp_start)
    pop_exc.set(t_clamp = clamp_duration)
    clamp_pops.append(pop_exc)

# Create projections. 
# Commented for now because not relevant for voltage clamp results.
#    synapse = p.Projection(
#        AMPA_src, clamp_pops[i], p.AllToAllConnector(),
#        p.StaticSynapse(weight=25, delay=1), receptor_type="AMPA")

# Set pops to record.
    clamp_pops[i].record("all")

# Lists to save recorded data.
exc_data = []
clamps = []

# Run simulation.
p.run(runtime)

# Collect recorded data.
for i in range(clamps_number):
    exc_data.append(clamp_pops[i].get_data())
    clamps.append(exc_data[i].segments[0].filter(name='gsyn_inh')[0])
    print "Post-synaptic neuron firing frequency: {} Hz".format(
        len(exc_data[i].segments[0].spiketrains[0]))

# begin simulation of floating point INaP
hold_voltage = -65.0

def sodium_additional_input_get_input_value_as_current(membrane_voltage):
    g_NaP = 0.007
    m_inf = 1 / (1 + np.exp(-(membrane_voltage+55.7) * 0.12987))
    I_NaP = g_NaP * m_inf  * m_inf * m_inf *(membrane_voltage - 45) #g_NaP * m_inf  * m_inf * m_inf * (membrane_voltage - 45)
    return I_NaP

I_NaP =[[] for clamp in range(clamps_number)]

for clamp in range(clamps_number):
    for time in np.arange(0, runtime, dt):
        if time >=  clamp_start and time < clamp_start+clamp_duration:
            membrane_voltage = clamps_voltage[clamp]
        else: 
            membrane_voltage = -65.0
        current = sodium_additional_input_get_input_value_as_current( membrane_voltage)
        I_NaP[clamp].append(current )

# Prepare recorded data for comparisson with floating point results.
I_spinnaker = [map(lambda x: x.magnitude.flatten(), clamps[i]) for i in range(clamps_number)]

# try keep same color code for curves.
NUM_COLORS = clamps_number
cm = plt.get_cmap('tab20')

# Plot SpiNNaker fixed-point vs Python floating-point results and their difference.
ax = plt.subplot(1, 2, 1)
ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
plt.plot(np.transpose(I_NaP[0]), color='black', linestyle='dotted', label='Floating-point')
plt.plot(np.transpose(I_spinnaker[0])[0], color='black', linestyle='dashed', label='SpiNNaker Fixed-point')
plt.plot(np.transpose(I_NaP), linestyle='dotted')
plt.plot(np.transpose(I_spinnaker)[0], linestyle='dashed')
plt.legend(loc='lower left');
plt.xlabel('Time (ms)');
plt.ylabel('I_NaP (nA)');  # TODO: verify it is really nano Ampers
plt.title('I_NaP current (nA)')
plt.subplot(1, 2, 2)
plt.plot(np.transpose(I_spinnaker)[0] - np.transpose(I_NaP), linestyle='solid')
plt.xlabel('Time (ms)');
plt.ylabel('I_NaP (nA)');
plt.title('I_NaP current (nA)')
plt.show()

#end simulator
p.end()

print('-->> this simulation was ran using test_sodium_current.py')

