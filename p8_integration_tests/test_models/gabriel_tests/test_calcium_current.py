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
clamps_voltage = numpy.arange(30,-101,-10)
clamp_start = runtime / 10
clamp_duration = runtime / 4
clamps_number = len(clamps_voltage)

# Spike source to send spike via plastic synapse.
# Commented for now because not relevant for voltage clamp results.
#AMPA_src = p.Population(1, p.SpikeSourceArray,
#                        {'spike_times': [0.5*runtime/10, 2.5 * runtime/10]}, label="src1")

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


# Begin simulation of floating point Ih
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
        if time >=  clamp_start and time < clamp_start+clamp_duration: 
                membrane_voltage = clamps_voltage[clamp]
        else: 
            membrane_voltage = hold_voltage
        m, h, current = calcium_additional_input_get_input_value_as_current(m, h, membrane_voltage)
        I_T[clamp].append(current )

# Prepare recorded data for comparisson with floating point results.
I_spinnaker = [map(lambda x: x.magnitude.flatten(), clamps[i]) for i in range(clamps_number)]
diff = np.transpose(I_spinnaker)[0] - np.transpose(I_T)
error = 100 * np.absolute(diff) / np.transpose(I_T) # percentual error w.r.t. I_floating
maxdiff= np.amax(diff)
error_at_max_diff = error.flatten()[np.argmax(diff)]

# try keep same color code for curves.
NUM_COLORS = clamps_number
cm = plt.get_cmap('tab20')

# Plot SpiNNaker fixed-point vs Python floating-point results and their difference.
ax = plt.subplot(1, 2, 1)
ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
plt.plot(np.transpose(I_T[0]), color='black', linestyle='dotted', label='Floating-point')
plt.plot(np.transpose(I_spinnaker[0])[0], color='black', linestyle='dashed', label='SpiNNaker Fixed-point')
plt.plot(np.transpose(I_T), linestyle='dotted')
plt.plot(np.transpose(I_spinnaker)[0], linestyle='dashed')
plt.legend(loc='lower left');
plt.xlabel('Time (ms)');
plt.ylabel('I_T (nA)'); 
plt.title('I_calcium'); # TODO: verify it is really nano Ampers
ax2 = plt.subplot(2, 2, 2)
ax2.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
plt.plot(error, linestyle='solid')
plt.xlabel('Time (ms)');
plt.ylabel('percent error (%)');
plt.title('Percent Error (error at max diff = %0.2f %% )'%error_at_max_diff)
ax2 = plt.subplot(2, 2, 4)
ax2.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
plt.plot(-diff, linestyle='solid')
plt.xlabel('Time (ms)');
plt.ylabel('difference (nA)');
plt.title('max diff = %0.4f nA'%np.amax(diff))
plt.tight_layout()
plt.show()

print('steady values at half runtime for Floating-point:')
for val in np.transpose(I_T)[runtime/2]:
    print(val)
print('steady values at half runtime for Fixed-point:')
for val in np.transpose(I_spinnaker)[0][runtime/2]:
    print(val)

#Figure(
#    # plot data for postsynaptic neuron
#    Panel(*clamps, ylabel='Pacemaker Intrinsic Current (?)', xlabel='time (ms)', data_labels = [clamp_pops[i].label for i in range(clamps_number)], yticks=True, xlim=(0,runtime)),
#    annotations="Post-synaptic neuron firing frequency: {} Hz".format(1)
#    
#)
#plt.show()

#end simulator
p.end()

print('-->> this simulation was ran using %s'%__file__)

