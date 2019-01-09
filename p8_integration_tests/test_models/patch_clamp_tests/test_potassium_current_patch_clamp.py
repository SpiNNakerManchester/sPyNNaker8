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
    'I_DK': 0.0,
    'g_DK': 0.5,
    'E_DK': -90.0,
    'm_inf_DK': 0.0,
    'e_to_t_on_tau_m_DK': 1250}

plt_colours = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']


# #############################################################################
# Setup and run patch clamp test in Python
# #############################################################################

def potassium_additional_input_get_input_value_as_current(D, membrane_voltage):
    e_to_t_on_tau = np.exp(
        -timestep / neuron_params['e_to_t_on_tau_m_DK'])  # 0.367879
    NaInflux = 0.025 / (1. + np.exp(-(membrane_voltage - -10) * 0.2))
    D_infinity = neuron_params['e_to_t_on_tau_m_DK'] * NaInflux + 0.001
    D = D_infinity + (D - D_infinity) * e_to_t_on_tau
    m_inf = 1. / (1. + (0.0078125 / (D**3)))
    I_DK = -neuron_params['g_DK'] * m_inf * (membrane_voltage -
                                             neuron_params['E_DK'])
    return D, I_DK


I_DK_Python = []
hold_voltage = -65.0

for k in range(len(clamp_voltages[0])):
    NaInflux = 0.025 / (1 + np.exp(-(hold_voltage - -10) * 0.2))
    D = 1250 * NaInflux + 0.001

    for j in clamp_voltages:
        I_DK_Python.append([])
        for i in range(int(round(runtime / timestep))):
            D, I_DK_dt = potassium_additional_input_get_input_value_as_current(
                D, j[k])
            I_DK_Python[k].append(I_DK_dt)

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
I_DK_SpiNNaker = exc_data.segments[0].filter(name='gsyn_exc')[0].magnitude


# #############################################################################
# Create Plot
# #############################################################################
for i in range(I_DK_SpiNNaker.shape[1]):
    plt.plot(I_DK_Python[i], label='Python: ' + str(clamp_voltages[1][i]),
             linestyle='-.', color=plt_colours[i])
    plt.plot(I_DK_SpiNNaker[:, i], label='SpiNNaker: ' +
             str(clamp_voltages[1][i]), linestyle='--', color=plt_colours[i])

plt.legend()
plt.title('I_DK Current Patch Clamp Analysis')
plt.xlabel('Time (ms)')
plt.ylabel('Current (nA)')
plt.show()

p.end()
print "job done"
