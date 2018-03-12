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
        # normalization: multiplying probabilities with firing rates
        norm_stp_traces.append(np.mean(stps_traces)*freq)
        start_time = start_time + 200*rt_scaling
    return freq_stp_traces, norm_stp_traces



output_path = 'C:\\Users\\Lultra\\git\\'
filename1 = 'out_fac.txt'
filename2 = 'out_dep.txt'

with open(output_path + filename1) as f1:
    data_fac = f1.readlines()
with open(output_path + filename2) as f2:
    data_dep = f2.readlines()

spiking_frequencies = np.linspace(0, 100, 21)
freq_stp_traces_fac, norm_stp_traces_fac = processing_data(data_fac, spiking_frequencies)
freq_stp_traces_dep, norm_stp_traces_dep = processing_data(data_dep, spiking_frequencies)



# plotting

fig1, ax1 = plt.subplots()
plt.title('facilitation')
p1 = ax1.plot(spiking_frequencies, freq_stp_traces_fac, 'b--', label='$<P_{rel}>$')
ax1.set_xlabel('r (Hz)')
ax1.set_ylabel(r'$<P_{rel}>$')
ax1.set_xlim([0,100])
ax1.set_ylim([0,1.])
ax2 = ax1.twinx()
p2 = ax2.plot(spiking_frequencies, norm_stp_traces_fac, 'b', label=r'$<P_{rel}>r$ (Hz)')
ax2.set_ylabel(r'$<P_{rel}>r$ (Hz)')
plots = p1+p2
labs = [plot.get_label() for plot in plots]
ax1.legend(plots, labs, loc='upper left')
plt.savefig(output_path + '5_18_A-reproduction.png', format = 'png', dpi = 1200)
plt.show()

fig2, ax3 = plt.subplots()
plt.title('depression')
p3 = ax3.plot(spiking_frequencies, freq_stp_traces_dep, 'b--', label='$<P_{rel}>$')
ax3.set_xlabel('r (Hz)')
ax3.set_ylabel(r'$<P_{rel}>$')
ax3.set_xlim([0,100])
ax3.set_ylim([0,1.])
ax4 = ax3.twinx()
p4 = ax4.plot(spiking_frequencies, norm_stp_traces_dep, 'b', label=r'$<P_{rel}>r$ (Hz)')
ax4.set_ylabel(r'$<P_{rel}>r$ (Hz)')
plots = p3+p4
labs = [plot.get_label() for plot in plots]
ax3.legend(plots, labs, loc='center right')
plt.savefig(output_path + '5_18_B-reproduction.png', format = 'png', dpi = 1200)
plt.show()


