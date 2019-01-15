import spynnaker8 as p
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt
import numpy as np

timestep = 0.1
p.setup(timestep)  # set simulation timestep (ms)
runtime = 500
new_i_offset = 10 # can be: 0, 10, 20, or 30


case_dict = {0:1, 10:2, 20: 3, 30: 4}


# read V data
f = open("Current_injection-V.txt", "r")
#f = open("Current_injection-V_4.txt", "r")

l = f.readlines()[0].split("\r")
l.remove(l[0])
f.close

NEST_v_data = np.zeros((len(l)-1,5))

for i in range(len(l)-1):
    d = l[i].split()
    for j in range(len(d)):
        NEST_v_data[i,j] = float(d[j])


# read I_DK
f = open("Current_injection-IKNa.txt", "r")
#f = open("Current_injection-IKNa_4.txt", "r")

l = f.readlines()[0].split("\r")
l.remove(l[0])
f.close

NEST_I_DK_data = np.zeros((len(l)-1,5))

for i in range(len(l)-1):
    d = l[i].split()
    for j in range(len(d)):
        NEST_I_DK_data[i,j] = float(d[j])


#read I_NaP
f = open("Current_injection-INaP.txt", "r")
#f = open("Current_injection-INaP_4.txt", "r")

l = f.readlines()[0].split("\r")
l.remove(l[0])
f.close

NEST_I_NaP_data = np.zeros((len(l)-1,5))

for i in range(len(l)-1):
    d = l[i].split()
    for j in range(len(d)):
        NEST_I_NaP_data[i,j] = float(d[j])


# Post-synapse population
neuron_params = {
        # 'v': -65,
        'g_Na': 0.2,
        'E_Na': 30.0,
        'g_K': 1.0, # Ex Cort values
        'E_K': -90.0,
        'tau_m': 16,
        't_spike': 2,
        'i_offset': 0,
        'g_H': 0,
        'g_T': 0,
        'g_NaP': 0.5,
        'g_DK': 0.5
        }


pop_exc_1 = p.Population(1,
                       p.extra_models.HillTononiNeuron(**neuron_params),
                       label="HT Neuron")
pop_exc_2 = p.Population(1,
                       p.extra_models.HillTononiNeuron(**neuron_params),
                       label="HT Neuron")
pop_exc_3 = p.Population(1,
                       p.extra_models.HillTononiNeuron(**neuron_params),
                       label="HT Neuron")
pop_exc_4 = p.Population(1,
                       p.extra_models.HillTononiNeuron(**neuron_params),
                       label="HT Neuron")


# pop_src1.record('all')
total_runtime = 0
pop_exc_1.record("all")
pop_exc_2.record("all")
pop_exc_3.record("all")
pop_exc_4.record("all")

p.run(runtime)
total_runtime += runtime
pop_exc_1.set(i_offset=0)
pop_exc_2.set(i_offset=10)
pop_exc_3.set(i_offset=20)
pop_exc_4.set(i_offset=30)

p.run(runtime)
total_runtime += runtime
pop_exc_1.set(i_offset=0)
pop_exc_2.set(i_offset=0)
pop_exc_3.set(i_offset=0)
pop_exc_4.set(i_offset=0)

p.run(runtime)
total_runtime += runtime

exc_data = {}
exc_data[1] = pop_exc_1.get_data()
exc_data[2] = pop_exc_2.get_data()
exc_data[3] = pop_exc_3.get_data()
exc_data[4] = pop_exc_4.get_data()

titles = {1: "0 nA", 2: "10 nA", 3: "20 nA", 4: "30 nA"}

plt.figure()
plt.suptitle("Membrane Potential (mV)")
index=1
for case in case_dict.keys():
    # Plot Voltage
    plt.subplot(4,1,index)
    plt.title(titles[index])
    plt.plot(NEST_v_data[:,0], NEST_v_data[:,case_dict[case]], label="NEST")
    plt.plot(NEST_v_data[:,0],
             exc_data[index].segments[0].filter(name='v')[0].magnitude[
                 0:len(NEST_v_data[:,case_dict[new_i_offset]])], label="SpiNNaker")
    plt.legend()
    plt.tight_layout()
    plt.show(block=False)
    index+=1

# Plot I_DK
plt.figure()
plt.suptitle("Intrinsic Current I_DK")
index=1
for case in case_dict.keys():
    plt.subplot(4,1,index)
    plt.title(titles[index], loc='right')
    plt.plot(NEST_I_DK_data[:,0], -NEST_I_DK_data[:,case_dict[case]], label="NEST")
    plt.plot(NEST_I_DK_data[:,0],
             exc_data[index].segments[0].filter(name='gsyn_inh')[0].magnitude[
                 0:len(NEST_I_DK_data[:,case_dict[new_i_offset]])], label="SpiNNaker")
    plt.legend()
    plt.tight_layout()
    plt.show(block=False)
    index+=1

# Plot I_NaP
plt.figure()
plt.suptitle("Intrinsic Current I_NaP")
index=1
for case in case_dict.keys():
    plt.subplot(4,1,index)
    plt.title(titles[index])
    plt.plot(NEST_I_NaP_data[:,0], -NEST_I_NaP_data[:,case_dict[case]], label="NEST")
    plt.plot(NEST_I_NaP_data[:,0],
             exc_data[index].segments[0].filter(name='gsyn_exc')[0].magnitude[
                 0:len(NEST_I_NaP_data[:,case_dict[new_i_offset]])], label="SpiNNaker")
    plt.legend()
    plt.tight_layout()
    plt.show(block=False)
    index+=1

plt.show()
p.end()
