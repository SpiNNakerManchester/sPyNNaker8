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
runtime = 1500

# Clamp parameters.
clamps_voltage = numpy.arange(40,-205,-5)
clamp_start = runtime / 10
clamp_duration = runtime - 6* clamp_start
clamps_number = len(clamps_voltage)

# Spike source to send spike via plastic synapse.
# Commented for now because not relevant for voltage clamp results.
#AMPA_src = p.Population(1, p.SpikeSourceArray,
#                        {'spike_times': [runtime/10, 6 * runtime/10]}, label="src1")

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

# Begin simulation of floating point currents.
hold_voltage = -65.0

# Begin simulation of floating point Ih.
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

I_h =[[] for clamp in range(clamps_number)]

for clamp in range(clamps_number):
    m = 1 / (1 + np.exp((hold_voltage + 75) / 5.5))
    for time in np.arange(0, runtime, dt):
        if time >=  clamp_start and time < clamp_start+clamp_duration: 
                membrane_voltage = clamps_voltage[clamp]
        else: 
            membrane_voltage = hold_voltage
        m, current = additional_input_get_input_value_as_current(m, membrane_voltage)
        I_h[clamp].append(current )

# No simulation of IT for this neuron type.
# Begin simulation of floating point INaP.
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

# Begin simulation of floating point IDK.
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
        if time >=  clamp_start and time < clamp_start+clamp_duration:
                membrane_voltage = clamps_voltage[clamp]
        else:
            membrane_voltage = hold_voltage
        D, current = potassium_additional_input_get_input_value_as_current(D, membrane_voltage)
        I_DK[clamp].append(current )

# Combine all floating point intrinsic currents.
I_floating = reduce(np.add, [I_h, I_NaP, I_DK])

# Prepare recorded data for comparisson with floating point results.
I_spinnaker = [map(lambda x: x.magnitude.flatten(), clamps[i]) for i in range(clamps_number)]

# try keep same color code for curves.
NUM_COLORS = clamps_number
cm = plt.get_cmap('tab20')

# Plot SpiNNaker fixed-point vs Python floating-point results and their difference.
ax = plt.subplot(1, 2, 1)
ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
plt.plot(np.transpose(I_floating[0]), color='black', linestyle='dotted', label='Floating-point')
plt.plot(np.transpose(I_spinnaker[0])[0], color='black', linestyle='dashed', label='SpiNNaker Fixed-point')
plt.plot(np.transpose(I_floating), linestyle='dotted')
plt.plot(np.transpose(I_spinnaker)[0], linestyle='dashed')
plt.legend(loc='lower right');
plt.xlabel('Time (ms)');
plt.ylabel('I_intrinsically_bursting (nA)');
plt.title('I_intrinsically_bursting (nA)') # TODO: verify it is really nano Ampers
plt.subplot(1, 2, 2)
plt.plot(np.transpose(I_spinnaker)[0] - np.transpose(I_floating), linestyle='solid')
plt.xlabel('Time (ms)');
plt.ylabel('Difference (nA)');
plt.title('Difference (nA)')
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

print('-->> this simulation was ran using test_all_currents_current.py')
