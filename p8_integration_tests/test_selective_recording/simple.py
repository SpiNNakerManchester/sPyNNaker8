import numpy
import os

import spynnaker8 as sim
from p8_integration_tests.base_test_case import BaseTestCase

current_file_path = os.path.dirname(os.path.abspath(__file__))
spike_file = os.path.join(current_file_path, "spikes.csv")
v_file = os.path.join(current_file_path, "v.csv")
exc_file = os.path.join(current_file_path, "exc.csv")
inh_file = os.path.join(current_file_path, "inh.csv")
master_spike_file = os.path.join(current_file_path, "master_spikes.csv")
master_v_file = os.path.join(current_file_path, "master_v.csv")
master_exc_file = os.path.join(current_file_path, "master_exc.csv")
master_inh_file = os.path.join(current_file_path, "master_inh.csv")

SIMTIME = 20000


def run_script(
        record_spikes=False, spike_rate=None, spike_indexes=None,
        record_v=False, v_rate=None, v_indexes=None,
        record_exc=False, exc_rate=None, exc_indexes=None,
        record_inh=False, inh_rate=None, inh_indexes=None):
    n_neurons = 500
    simtime = SIMTIME

    sim.setup(timestep=1)

    pop_1 = sim.Population(n_neurons, sim.IF_curr_exp(), label="pop_1")
    input1 = sim.Population(1, sim.SpikeSourceArray(spike_times=[0]),
                            label="input")
    sim.Projection(input1, pop_1, sim.AllToAllConnector(),
                   synapse_type=sim.StaticSynapse(weight=5, delay=1))
    input2 = sim.Population(n_neurons, sim.SpikeSourcePoisson(
        rate=100.0, seed=1),  label="Stim_Exc")
    sim.Projection(input2, pop_1, sim.OneToOneConnector(),
                   synapse_type=sim.StaticSynapse(weight=5, delay=1))
    if record_spikes:
        pop_1.record(
            ['spikes'], sampling_interval=spike_rate, indexes=spike_indexes)
    if record_v:
        pop_1.record(['v'], sampling_interval=v_rate, indexes=v_indexes)
    if record_exc:
        pop_1.record(['gsyn_exc'], sampling_interval=exc_rate, indexes=exc_indexes)
    if record_inh:
        pop_1.record(['gsyn_inh'], sampling_interval=inh_rate, indexes=inh_indexes)
    sim.run(simtime)

    neo = pop_1.get_data()
    if record_spikes:
        spikes = neo.segments[0].spiketrains
        write_spikes(spikes)
        print spikes[0]
        spikes = read_spikes(spike_file)
        spikes2 = read_spikes(master_spike_file, rate=spike_rate)
        if len(spikes) != len(spikes2):
            print len(spikes)
            print len(spikes2)
            raise Exception("Spikes different length")
        for s1, s2 in zip(spikes, spikes2):
            if not numpy.array_equal(s1, s2):
                print s1
                print s2
                print len(s1)
                print len(s2)
                raise Exception("Spikes not equal")
        print "Spikes equal"
    else:
        spikes = None
    if record_v:
        v = neo.segments[0].filter(name='v')[0]
        numpy.savetxt(v_file, v, delimiter=',')
        compare(v_file, master_v_file, v_rate)
    else:
        v = None
    if record_exc:
        exc = neo.segments[0].filter(name='gsyn_exc')[0]
        numpy.savetxt(exc_file, exc, delimiter=',')
        compare(exc_file, master_exc_file, exc_rate)
    else:
        exc = None
    if record_inh:
        inh = neo.segments[0].filter(name='gsyn_inh')[0]
        numpy.savetxt(inh_file, inh, delimiter=',')
        compare(inh_file, master_inh_file, inh_rate)
    else:
        inh = None

    sim.end()

    return spikes, v,  exc, inh


def write_spikes(spikes):
    with open(spike_file, "w") as f:
        for i, spiketrain in enumerate(spikes):
            f.write("{}".format(i))
            for time in spiketrain.times:
                f.write(",{}".format(time.magnitude))
            f.write("\n")


def ordered_rounded_set(in_list, factor):
    out_list = []
    added = set()
    for s in in_list[1:]:
        raw = float(s)
        if (raw % factor) > 0:
            val = round(raw + factor - (raw % factor), 5)
        else:
            val = raw
        if val < SIMTIME and not val in added:
            out_list.append(val)
            added.add(val)
    out_list.insert(0, in_list[0])
    return out_list


def read_spikes(name, rate=1):
    spikes = []
    with open(name) as f:
        for line in f:
            parts = line.split(",")
            spikes.append(ordered_rounded_set(parts, rate))
    return spikes


def compare(f1, f2, rate):
    print f1
    d1 = numpy.loadtxt(f1, delimiter=',')
    print d1.shape
    print f2
    d2 = numpy.loadtxt(f2, delimiter=',')
    print d2.shape
    d2_rate = d2[::rate]
    print d2_rate.shape
    if not numpy.array_equal(d1, d2_rate):
        if d1.shape != d2_rate.shape:
            raise Exception("Shape not equal")
        for i in xrange(d1.shape[0]):
            if not numpy.array_equal(d1[i], d2_rate[i]):
                print d1[i]
                print d2_rate[i]
                raise Exception("not equal")


if __name__ == '__main__':
    spikes, v, exc, inh = run_script(
        record_spikes=True, spike_rate=3, spike_indexes=None,
        record_v=True, v_rate=4, v_indexes=None,
        record_exc=True, exc_rate=1, exc_indexes=None,
        record_inh=True, inh_rate=2, inh_indexes=None)

