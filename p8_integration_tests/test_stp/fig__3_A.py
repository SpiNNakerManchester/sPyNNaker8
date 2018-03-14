import numpy as np
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt


def processing_data(data, frequencies):
    gsyn_traces = map(float, data)
    # subtract the initial_run
    gsyn_traces = gsyn_traces[100:]

    rt_scaling = 10
    start_time = 0
    avg_traces = []
    for freq in spiking_frequencies:
        avg_traces.append(np.mean(gsyn_traces[start_time:start_time+200*rt_scaling]))
        start_time = start_time + 200*rt_scaling
    return avg_traces



output_path = 'C:\\Users\\Lultra\\git\\'
filename1 = 'dep_01.txt'
filename2 = 'dep_05.txt'
filename3 = 'dep_095.txt'

with open(output_path + filename1) as f1:
    data_dep1 = f1.readlines()
with open(output_path + filename2) as f2:
    data_dep2 = f2.readlines()
with open(output_path + filename3) as f3:
    data_dep3 = f3.readlines()


spiking_frequencies = np.linspace(0, 100, 41)
stp_traces_dep1 = processing_data(data_dep1, spiking_frequencies)
stp_traces_dep2 = processing_data(data_dep2, spiking_frequencies)
stp_traces_dep3 = processing_data(data_dep3, spiking_frequencies)



# plotting

plt.figure(1)
plt.title('different depression rates')
plt.plot(spiking_frequencies, stp_traces_dep1, label='$f_D = 0.1$')
plt.plot(spiking_frequencies, stp_traces_dep2, label='$f_D = 0.5$')
plt.plot(spiking_frequencies, stp_traces_dep3, label='$f_D = 0.95$')
plt.xlabel('presynaptic frequency (Hz)')
plt.ylabel('stationary postsynaptic current (mA)')
plt.xlim([0,100])
plt.legend(loc='center right')
plt.savefig(output_path + '3_A-reproduction.png', format = 'png', dpi = 1200)
plt.show()


