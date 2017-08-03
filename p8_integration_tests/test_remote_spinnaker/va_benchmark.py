# coding: utf-8
"""
An implementation of benchmarks 1 and 2 from

    Brette et al. (2007) Journal of Computational Neuroscience 23: 349-398

The IF network is based on the CUBA and COBA models of Vogels & Abbott
(J. Neurosci, 2005).  The model consists of a network of excitatory and
inhibitory neurons, connected via current-based "exponential"
synapses (instantaneous rise, exponential decay).

Andrew Davison, UNIC, CNRS
August 2006
"""
import socket
import spynnaker8 as p
from pyNN.random import NumpyRNG, RandomDistribution
from pyNN.utility import Timer
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

simulator_name = 'spiNNaker'
benchmark = 'CUBA'

# exec("from pyNN.%s import *" % simulator_name)

timer = Timer()

# === Define parameters ===
threads = 1
rngseed = 98766987
parallel_safe = True

n = 1500          # number of cells
r_ei = 4.0        # number of excitatory cells:number of inhibitory cells
pconn = 0.02      # connection probability
stim_dur = 50.    # (ms) duration of random stimulation
rate = 100.       # (Hz) frequency of the random stimulation

dt = 1.0          # (ms) simulation timestep
tstop = 1000      # (ms) simulaton duration
delay = 2

# Cell parameters
area = 20000.     # (µm²)
tau_m = 20.       # (ms)
cm = 1.           # (µF/cm²)
g_leak = 5e-5     # (S/cm²)

E_leak = None
if benchmark == "COBA":
    E_leak = -60.  # (mV)
elif benchmark == "CUBA":
    E_leak = -49.  # (mV)
v_thresh = -50.   # (mV)
v_reset = -60.    # (mV)
t_refrac = 5.     # (ms) (clamped at v_reset)
v_mean = -60.     # (mV) mean membrane potential, for calculating CUBA weights
tau_exc = 5.      # (ms)
tau_inh = 10.     # (ms)

# Synapse parameters
Gexc = None
Ginh = None
if benchmark == "COBA":
    Gexc = 4.     # (nS)
    Ginh = 51.    # (nS)
elif benchmark == "CUBA":
    Gexc = 0.27   # (nS) # Those weights should be similar to the COBA weights
    Ginh = 4.5    # (nS) # but with depolarising drift
Erev_exc = 0.     # (mV)
Erev_inh = -80.   # (mV)

# === Calculate derived parameters ===
area = area * 1e-8                     # convert to cm²
cm = cm * area * 1000                  # convert to nF
Rm = 1e-6 / (g_leak * area)            # membrane resistance in MΩ
assert tau_m == cm * Rm                # just to check

n_exc = int(round((n * r_ei / (1 + r_ei))))  # number of excitatory cells
n_inh = n - n_exc                            # number of inhibitory cells

print n_exc, n_inh

w_exc = None
w_inh = None
celltype = None
if benchmark == "COBA":
    celltype = p.IF_cond_exp
    w_exc = Gexc * 1e-3              # We convert conductances to uS
    w_inh = Ginh * 1e-3
    print w_exc, w_inh
elif benchmark == "CUBA":
    celltype = p.IF_curr_exp
    w_exc = 1e-3 * Gexc * (Erev_exc - v_mean)  # (nA) weight of exc synapses
    w_inh = 1e-3 * Ginh * (Erev_inh - v_mean)  # (nA)
    assert w_exc > 0
    assert w_inh < 0

# === Build the network ===

extra = {'threads': threads,
         'filename': "va_%s.xml" % benchmark,
         'label': 'VA'}
if simulator_name == "neuroml":
    extra["file"] = "VAbenchmarks.xml"

node_id = p.setup(
    timestep=dt, min_delay=delay, max_delay=delay,
    db_name='va_benchmark.sqlite', **extra)

if simulator_name == 'spiNNaker':
    p.set_number_of_neurons_per_core(p.IF_curr_exp, 100)      # this will set
    #  100 neurons per core
    p.set_number_of_neurons_per_core(p.IF_cond_exp, 50)      # this will set
    # 50 neurons per core
np = 1

host_name = socket.gethostname()
print "Host #%d is on %s" % (np, host_name)

print "%s Initialising the simulator with %d thread(s)..." % (
    node_id, extra['threads'])

cell_params = {'tau_m': tau_m,
               'tau_syn_E': tau_exc,
               'tau_syn_I': tau_inh,
               'v_rest': E_leak,
               'v_reset': v_reset,
               'v_thresh': v_thresh,
               'cm': cm,
               'tau_refrac': t_refrac,
               'i_offset': 0
               }

print cell_params

if (benchmark == "COBA"):
    cell_params['e_rev_E'] = Erev_exc
    cell_params['e_rev_I'] = Erev_inh

timer.start()

print "%s Creating cell populations..." % node_id
exc_cells = p.Population(
    n_exc, celltype(**cell_params), label="Excitatory_Cells")
inh_cells = p.Population(
    n_inh, celltype(**cell_params), label="Inhibitory_Cells")
exc_conn = None
ext_stim = None
if benchmark == "COBA":
    ext_stim = p.Population(
        20, p.SpikeSourcePoisson(rate=rate, duration=stim_dur),
        label="expoisson")
    rconn = 0.01
    ext_conn = p.FixedProbabilityConnector(rconn)
    ext_stim.record("spikes")

print "%s Initialising membrane potential to random values..." % node_id
rng = NumpyRNG(seed=rngseed, parallel_safe=parallel_safe)
uniformDistr = RandomDistribution('uniform', [v_reset, v_thresh], rng=rng)
exc_cells.set(v=uniformDistr)
inh_cells.set(v=uniformDistr)

print "%s Connecting populations..." % node_id
exc_conn = p.FixedProbabilityConnector(pconn, rng=rng)
inh_conn = p.FixedProbabilityConnector(pconn, rng=rng)

connections = {
    'e2e': p.Projection(
        exc_cells, exc_cells, exc_conn, receptor_type='excitatory',
        synapse_type=p.StaticSynapse(weight=w_exc, delay=delay)),
    'e2i': p.Projection(
        exc_cells, inh_cells, exc_conn, receptor_type='excitatory',
        synapse_type=p.StaticSynapse(weight=w_exc, delay=delay)),
    'i2e': p.Projection(
        inh_cells, exc_cells, inh_conn, receptor_type='inhibitory',
        synapse_type=p.StaticSynapse(weight=w_inh, delay=delay)),
    'i2i': p.Projection(
        inh_cells, inh_cells, inh_conn, receptor_type='inhibitory',
        synapse_type=p.StaticSynapse(weight=w_inh, delay=delay))}

if benchmark == "COBA":
    connections['ext2e'] = p.Projection(
        ext_stim, exc_cells, ext_conn, receptor_type='excitatory',
        synapse_type=p.StaticSynapse(weight=0.1))
    connections['ext2i'] = p.Projection(
        ext_stim, inh_cells, ext_conn, receptor_type='excitatory',
        synapse_type=p.StaticSynapse(weight=0.1))

# === Setup recording ===
print "%s Setting up recording..." % node_id
exc_cells.record("spikes")

buildCPUTime = timer.diff()

# === Run simulation ===
print "%d Running simulation..." % node_id

print "timings: number of neurons:", n
print "timings: number of synapses:", n * n * pconn

p.run(tstop)

simCPUTime = timer.diff()

# === Print results to file ===

exc_spikes = exc_cells.get_data("spikes")

Figure(
    # raster plot of the presynaptic neuron spike times
    Panel(exc_spikes.segments[0].spiketrains,
          yticks=True, markersize=0.2, xlim=(0, tstop)),
    title="va_benchmark",
    annotations="Simulated with {}".format(p.name())
)
plt.show()

writeCPUTime = timer.diff()

if node_id == 0:
    print "\n--- Vogels-Abbott Network Simulation ---"
    print "Nodes                  : %d" % np
    print "Simulation type        : %s" % benchmark
    print "Number of Neurons      : %d" % n
    print "Number of Synapses     : %s" % connections
    print "Excitatory conductance : %g nS" % Gexc
    print "Inhibitory conductance : %g nS" % Ginh
    print "Build time             : %g s" % buildCPUTime
    print "Simulation time        : %g s" % simCPUTime
    print "Writing time           : %g s" % writeCPUTime


# === Finished with simulator ===

p.end()
