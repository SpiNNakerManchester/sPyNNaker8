import numpy as np
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt


output_path = 'C:\\Users\\Lultra\\git\\'
filename1 = 'out_fac.txt'
filename2 = 'out_dep.txt'

with open(output_path + filename) as f:
    data = f.readlines()

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


rt_scaling = 10

# normalization: multiplying probabilities with firing rates
for i in range(len(current_stp_traces)):
    if times[i] <= 200*rt_scaling:
        current_stp_traces[i] = current_stp_traces[i] * 25.
    elif times[i] >= 200*rt_scaling and times[i] <= 500*rt_scaling:
        current_stp_traces[i] = current_stp_traces[i] * 100.
    elif times[i] >= 500*rt_scaling and times[i] <= 1000*rt_scaling:
        current_stp_traces[i] = current_stp_traces[i] * 10.
    else:
        current_stp_traces[i] = current_stp_traces[i] * 40.


# plotting

plt.figure(1)

plt.plot(times, current_stp_traces)
plt.xlabel('time (ms)')
plt.ylabel(r'$<P_{rel}>r$ (Hz)')
plt.axvline(x=200*rt_scaling, linestyle='dashed', color='grey')
plt.axvline(x=500*rt_scaling, linestyle='dashed', color='grey')
plt.axvline(x=1000*rt_scaling, linestyle='dashed', color='grey')
plt.text(80*rt_scaling, 8, '25 Hz')
plt.text(330*rt_scaling, 8, '100 Hz')
plt.text(730*rt_scaling, 8, '10 Hz')
plt.text(1080*rt_scaling, 8, '40 Hz')

plt.savefig(output_path + '5_19-reproduction.png', format = 'png', dpi = 1200)
plt.show()


