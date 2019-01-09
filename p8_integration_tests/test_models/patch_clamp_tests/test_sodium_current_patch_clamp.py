import spynnaker8 as p
import numpy as np
import matplotlib.pyplot as plt

# #############################################################################
# Global Parameters
# #############################################################################
timestep = 0.1
runtime = 500
clamp_voltages = [[-65, -65, -65, -65, -65, -65, -65],
                  [-50, -40, -30, -20, -10,   0,  10],
                  [-65, -65, -65, -65, -65, -65, -65]]

plt.figure()

neuron_params = {
    'v': clamp_voltages[0],
    'g_H': 0,
    'g_T': 0,
    'g_NaP': 0.5,
    'g_DK': 0,
    'E_NaP': 30}

plt_colours = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']


def sodium_additional_input_get_input_value_as_current(membrane_voltage):
    g_NaP = neuron_params['g_NaP']  # 0.007
    m_inf = 1 / (1 + np.exp(-(membrane_voltage + 55.7) * 0.12987))
    I_NaP = g_NaP * m_inf * m_inf * m_inf * (membrane_voltage -
                                             neuron_params['E_NaP'])
    return -I_NaP


# #############################################################################
# Setup and run patch clamp test in Python
# #############################################################################
I_Nap_Python = []
for k in range(len(clamp_voltages[0])):
    for j in clamp_voltages:
        I_Nap_Python.append([])
        for i in range(int(round(runtime / timestep))):
            I_Nap_Python[k].append(
                sodium_additional_input_get_input_value_as_current(j[k]))

# #############################################################################
# Setup and run patch clamp test on SpiNNaker
# #############################################################################

p.setup(timestep)  # set simulation timestep (ms)

patch_clamped_neuron = p.Population(len(clamp_voltages[0]),
                                    p.extra_models.PatchClamped(
                                        **neuron_params),
                                    label="Patch Clamped HT Neuron")

patch_clamped_neuron.record("all")

clamp_index = 0  # initialised to first clamp voltage during construction
for i in clamp_voltages:
    p.run(runtime)
    clamp_index += 1
    if clamp_index < len(clamp_voltages):
        patch_clamped_neuron.set(v=clamp_voltages[clamp_index])

# Extract SpiNNaker data and add to plot
exc_data = patch_clamped_neuron.get_data()
I_Nap_SpiNNaker = exc_data.segments[0].filter(name='gsyn_inh')[0].magnitude


# #############################################################################
# Create Plot
# #############################################################################
for i in range(I_Nap_SpiNNaker.shape[1]):
    plt.plot(I_Nap_Python[i], label='Python: ' + str(clamp_voltages[1][i]),
             linestyle='-.', color=plt_colours[i])
    plt.plot(I_Nap_SpiNNaker[:, i], label='SpiNNaker: ' +
             str(clamp_voltages[1][i]), linestyle='--', color=plt_colours[i])

plt.legend()
plt.title('I_NaP Current Patch Clamp Analysis')
plt.xlabel('Time (ms)')
plt.ylabel('Current (nA)')
plt.show()

p.end()
print "job done"
