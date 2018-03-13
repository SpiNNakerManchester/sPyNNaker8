import numpy as np
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt


def processing_data(data, frequencies):
    data = [line for line in data if not line.startswith('[INFO]') and not line == '\n']
    #for line in data:
        #print(line)
    times = []
    current_stp_traces = []
    for line in data:
        value = line.split(': ', 1)[-1]
        if line.startswith(' time'):
            times.append(value)
        elif line.startswith(' current'):
            current_stp_traces.append(value)
        else:
            print "Line without meaningful value"
    # converting strings to numbers
    times = map(int, times)
    current_stp_traces = map(float, current_stp_traces)
    # subtract the initial_run value from every time
    times = map(lambda x: x - 100, times)
    # compute average release probabilities for every simulated frequency
    rt_scaling = 10
    start_time = 0
    freq_stp_traces = []
    norm_stp_traces = []
    for freq in spiking_frequencies:
        stps_traces = []
        for i in range(len(times)):
            if times[i] >= start_time and times[i] <= start_time+200*rt_scaling:
                stps_traces.append(current_stp_traces[i])
        freq_stp_traces.append(np.mean(stps_traces))
        start_time = start_time + 200*rt_scaling
    return freq_stp_traces



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

spiking_frequencies = np.linspace(0, 100, 21)
freq_stp_traces_dep1 = processing_data(data_dep1, spiking_frequencies)
freq_stp_traces_dep2 = processing_data(data_dep2, spiking_frequencies)
freq_stp_traces_dep3 = processing_data(data_dep3, spiking_frequencies)



# plotting

plt.figure(1)
plt.title('different depression rates')
plt.plot(spiking_frequencies, freq_stp_traces_dep1, label='$f_D = 0.1$')
plt.plot(spiking_frequencies, freq_stp_traces_dep2, label='$f_D = 0.5$')
plt.plot(spiking_frequencies, freq_stp_traces_dep3, label='$f_D = 0.95$')
plt.xlabel('presynaptic frequency (Hz)')
plt.ylabel(r'$<P_{rel}>$')
plt.xlim([0,100])
plt.legend(loc='center right')
plt.savefig(output_path + 'different_depression_rates.png', format = 'png', dpi = 1200)
plt.show()


