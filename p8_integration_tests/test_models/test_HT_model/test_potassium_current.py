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

# Clamp parameters.
clamps_voltage = numpy.arange(30,-101,-10)
clamp_start = runtime / 10
clamp_duration = runtime - 2* clamp_start
clamps_number = len(clamps_voltage)

# Spike source to send spike via plastic synapse
# Commented for now because not relevant for voltage clamp results.
#AMPA_src = p.Population(1, p.SpikeSourceArray,
#                        {'spike_times': [runtime/10,5 * runtime/10]}, label="src1")

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

# Begin simulation of floating point IDK.
hold_voltage = -65.0
def potassium_additional_input_get_input_value_as_current(D, membrane_voltage):
    g_DK = 1.25
    e_to_t_on_tau = 0.367879
    NaInflux = 0.025 / (1. + np.exp(-(membrane_voltage- -10) * 0.2))
    D_infinity = 1250 * NaInflux + 0.001
    D = D_infinity + (D - D_infinity) * e_to_t_on_tau
    m_inf = 1. / (1. + (0.0078125 /(D**3)))
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

# # begin simulation of floating point IDK
# hold_voltage = -65.0
# 
# def potassium_additional_input_get_input_value_as_current(D, membrane_voltage):
#     g_DK = 1.25
#     e_to_t_on_tau = 0.367879 
#     NaInflux = 0.025 / (1. + np.exp(-(membrane_voltage- -10) * 0.2))
#     D_infinity = 1250 * NaInflux + 0.001
#     D = D_infinity + (D - D_infinity) * e_to_t_on_tau
#     m_inf = 1. / (1. + (0.0078125 /(D**3)+0.00000001)) 
#     I_DK = - g_DK * m_inf * (membrane_voltage - -90)  #+ 5.6402035021220295e-06
#     return D, I_DK
# 
# I_DK =[[] for clamp in range(clamps_number)]
# 
# for clamp in range(clamps_number):
#     NaInflux = 0.025 / (1 + np.exp(-(hold_voltage - -10) * 0.2))
#     D = 1250 * NaInflux + 0.001
#     for time in np.arange(0, runtime, dt):
#         if time >=  clamp_start and time < clamp_start+clamp_duration:
#             membrane_voltage = clamps_voltage[clamp]
#         else: 
#             membrane_voltage = hold_voltage
#         D, current = potassium_additional_input_get_input_value_as_current(D, membrane_voltage)
#         I_DK[clamp].append(current)

# Prepare recorded data for comparisson with floating point results.
I_spinnaker = [map(lambda x: x.magnitude.flatten(), clamps[i]) for i in range(clamps_number)]
diff = np.transpose(I_spinnaker)[0] - np.transpose(I_DK)
error = 100 * np.absolute(diff) / np.transpose(I_DK) # percentual error w.r.t. I_floating
maxdiff= np.amax(diff)
error_at_max_diff = error.flatten()[np.argmax(diff)]

# try keep same color code for curves.
NUM_COLORS = clamps_number
cm = plt.get_cmap('tab20')

# Plot SpiNNaker fixed-point vs Python floating-point results and their difference.
ax = plt.subplot(1, 2, 1)
ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
plt.plot(np.transpose(I_DK[0]), color='black', linestyle='dotted', label='Floating-point')
plt.plot(np.transpose(I_spinnaker[0])[0], color='black', linestyle='dashed', label='SpiNNaker Fixed-point')
plt.plot(np.transpose(I_DK), linestyle='dotted')
plt.plot(np.transpose(I_spinnaker)[0], linestyle='dashed')
plt.legend(loc='lower left');
plt.xlabel('Time (ms)');
plt.ylabel('I_DK (nA)');  # TODO: verify it is really nano Ampers
plt.title('I_potassium');
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
for val in np.transpose(I_DK)[runtime/2]:
    print(val)
print('steady values at half runtime for Fixed-point:')
for val in np.transpose(I_spinnaker)[0][runtime/2]:
    print(val)

p.end()

print('-->> this simulation was ran using %s'%__file__)

