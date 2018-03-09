import numpy
import os
import sys

import spynnaker8 as sim
from p8_integration_tests.base_test_case import BaseTestCase
from spynnaker8.models.populations.population_view import PopulationView


current_file_path = os.path.dirname(os.path.abspath(__file__))


def run_script(
        simtime, n_neurons, run_split=1,
        record_spikes=False, spike_rate=None, spike_rec_indexes=None,
        spike_get_indexes=None,
        record_v=False, v_rate=None, v_indexes=None,
        record_exc=False, exc_rate=None, exc_indexes=None,
        record_inh=False, inh_rate=None, inh_indexes=None,
        file_prefix=""):

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
        if spike_rec_indexes is None:
            pop_1.record(['spikes'], sampling_interval=spike_rate)
        else:
            view = PopulationView(pop_1, spike_rec_indexes)
            view.record(['spikes'], sampling_interval=spike_rate)
    if record_v:
        pop_1.record(['v'], sampling_interval=v_rate, indexes=v_indexes)
    if record_exc:
        pop_1.record(['gsyn_exc'], sampling_interval=exc_rate,
                     indexes=exc_indexes)
    if record_inh:
        pop_1.record(['gsyn_inh'], sampling_interval=inh_rate,
                     indexes=inh_indexes)
    for i in range(run_split):
        sim.run(simtime/run_split)

    if record_spikes:
        if spike_get_indexes is None:
            neo = pop_1.get_data("spikes")
        else:
            view = PopulationView(pop_1, spike_get_indexes)
            neo = view.get_data("spikes")
        spikes = neo.segments[0].spiketrains
        spike_file = os.path.join(current_file_path, file_prefix+"spikes.csv")
        write_spikes(spikes, spike_file)
    else:
        spikes = None

    if record_v:
        neo = pop_1.get_data('v')
        v = neo.segments[0].filter(name='v')[0]
        v_file = os.path.join(current_file_path, file_prefix+"v.csv")
        numpy.savetxt(v_file, v, delimiter=',')
    else:
        v = None
    if record_exc:
        neo = pop_1.get_data('gsyn_exc')
        exc = neo.segments[0].filter(name='gsyn_exc')[0]
        exc_file = os.path.join(current_file_path, file_prefix+"exc.csv")
        numpy.savetxt(exc_file, exc, delimiter=',')
    else:
        exc = None
    if record_inh:
        neo = pop_1.get_data('gsyn_inh')
        inh = neo.segments[0].filter(name='gsyn_inh')[0]
        inh_file = os.path.join(current_file_path, file_prefix+"inh.csv")
        numpy.savetxt(inh_file, inh, delimiter=',')
    else:
        inh = None

    sim.end()

    return spikes, v,  exc, inh


def compare_spikearrays(this, full, tollerance=False):
    if numpy.array_equal(this, full):
        return sys.maxint
    if this[0] != full[0]:
        raise Exception("Index missmatch")
    if len(this) != len(full):
        print "{} spikes length differ. {} != {}" \
              "".format(this[0], len(this), len(full))
    i1 = 0
    i2 = 0
    lowest = None
    while i1 < len(this) and i2 < len(full):
        if this[i1] == full[i2]:
            i1 += 1
            i2 += 1
        elif this[i1] < full[i2]:
            print "extra spike {} has spike at {}".format(this[0], this[i1])
            i1 += 1
            if lowest is None:
                lowest = this[i1]
        elif this[i1] > full[i2]:
            print "spike missing {} no spike at {}".format(this[0], full[i2])
            i2 += 1
            if lowest is None:
                lowest = full[i2]
    while i1 < len(this):
        print "trailing extra spike {} has spike at {}" \
              "".format(this[0], this[i1])
        if lowest is None:
            lowest = this[i1]
        i1 += 1
    while i2 < len(full):
        print "trailing spike missing {} no spike at {}" \
              "".format(this[0], full[i2])
        if lowest is None:
            lowest = full[i2]
        i2 += 1
    if lowest is None:
        lowest = sys.maxint
    return lowest
    # raise Exception("Spikes not equal")


def compare_spikes(file_path, full_path, simtime, n_neurons, spike_rate=1,
                   spike_indexes=None, tollerance=sys.maxint):
    this_spikes = read_spikes(file_path, simtime, n_neurons)
    full_spikes = read_spikes(full_path, simtime, n_neurons, rate=spike_rate,
                              indexes=spike_indexes)
    if len(this_spikes) != len(full_spikes):
        raise Exception("Spikes different length this {} full {}"
                        "".format(len(this_spikes), len(full_spikes)))
    lowest = sys.maxint
    for this, full in zip(this_spikes, full_spikes):
        low = compare_spikearrays(this, full)
        lowest = min(lowest, low)
    if lowest < tollerance:
        raise Exception("Spikes different from {}".format(lowest))
    print "Spikes equal"
    return lowest


def compare_results(
        simtime, n_neurons,
        record_spikes=False, spike_rate=None, spike_indexes=None,
        record_v=False, v_rate=None, v_indexes=None,
        record_exc=False, exc_rate=None, exc_indexes=None,
        record_inh=False, inh_rate=None, inh_indexes=None, full_prefix="",
        tollerance=sys.maxint):
    if record_spikes:
        file_path = os.path.join(current_file_path, "spikes.csv")
        full_path = os.path.join(current_file_path, full_prefix+"spikes.csv")
        compare_spikes(file_path, full_path, simtime, n_neurons,
                       spike_rate, spike_indexes, tollerance)
    if record_v:
        file_path = os.path.join(current_file_path, "v.csv")
        full_path = os.path.join(current_file_path, full_prefix+"v.csv")
        compare(file_path, full_path, v_rate, v_indexes)
    if record_exc:
        file_path = os.path.join(current_file_path, "exc.csv")
        full_path = os.path.join(current_file_path, full_prefix+"exc.csv")
        compare(file_path, full_path, exc_rate, exc_indexes)
    if record_inh:
        file_path = os.path.join(current_file_path, "inh.csv")
        full_path = os.path.join(current_file_path, full_prefix+"inh.csv")
        compare(file_path, full_path, inh_rate, inh_indexes)


def run_and_compare_script(
        simtime, n_neurons, run_split=1,
        record_spikes=False, spike_rate=None, spike_rec_indexes=None,
        spike_get_indexes=None,
        record_v=False, v_rate=None, v_indexes=None,
        record_exc=False, exc_rate=None, exc_indexes=None,
        record_inh=False, inh_rate=None, inh_indexes=None,
        tollerance=sys.maxint):
    full_prefix = "{}_{}_".format(simtime, n_neurons)
    if (not os.path.exists(
            os.path.join(current_file_path, full_prefix + "spikes.csv")) or
            not os.path.exists(
                os.path.join(current_file_path, full_prefix + "v.csv")) or
            not os.path.exists(
                os.path.join(current_file_path, full_prefix + "v.csv")) or
            not os.path.exists(
                os.path.join(current_file_path, full_prefix + "v.csv"))):
        print ("Comparision files do not exist so creating them")
        run_script(
            simtime, n_neurons,
            record_spikes=True,
            record_v=True,
            record_exc=True,
            record_inh=True,
            file_prefix=full_prefix)

    run_script(
        simtime, n_neurons, run_split,
        record_spikes=record_spikes, spike_rate=spike_rate,
        spike_rec_indexes=spike_rec_indexes,
        spike_get_indexes=spike_get_indexes,
        record_v=record_v, v_rate=v_rate, v_indexes=v_indexes,
        record_exc=record_exc, exc_rate=exc_rate, exc_indexes=exc_indexes,
        record_inh=record_inh, inh_rate=inh_rate, inh_indexes=inh_indexes)
    if spike_rec_indexes is None:
        if spike_get_indexes is None:
            spike_indexes = None
        else:
            spike_indexes = spike_get_indexes
    else:
        if spike_get_indexes is None:
            spike_indexes = spike_rec_indexes
        else:
            spike_indexes = [index for index in spike_rec_indexes
                             if index in spike_get_indexes]

    compare_results(
        simtime, n_neurons,
        record_spikes=record_spikes, spike_rate=spike_rate,
        spike_indexes=spike_indexes,
        record_v=record_v, v_rate=v_rate, v_indexes=v_indexes,
        record_exc=record_exc, exc_rate=exc_rate, exc_indexes=exc_indexes,
        record_inh=record_inh, inh_rate=inh_rate, inh_indexes=inh_indexes,
        full_prefix=full_prefix, tollerance=tollerance)


def write_spikes(spikes, spike_file):
    with open(spike_file, "w") as f:
        for spiketrain in spikes:
            f.write("{}".format(spiketrain.annotations["source_index"]))
            for time in spiketrain.times:
                f.write(",{}".format(time.magnitude))
            f.write("\n")


def ordered_rounded_set(in_list, factor, simtime):
    out_list = []
    added = set()
    for s in in_list[1:]:
        raw = float(s)
        if (raw % factor) > 0:
            val = round(raw + factor - (raw % factor), 5)
        else:
            val = raw
        if val < simtime and val not in added:
            out_list.append(val)
            added.add(val)
    out_list.insert(0, in_list[0])
    return out_list


def read_spikes(name, simtime, n_neurons, rate=1, indexes=None):
    spikes = []
    with open(name) as f:
        for line in f:
            parts = line.split(",")
            if len(parts) > 1:
                if indexes is None:
                    if int(parts[0]) < n_neurons:
                        spikes.append(
                            ordered_rounded_set(parts, rate, simtime))
                else:
                    if int(parts[0]) in indexes:
                        spikes.append(
                            ordered_rounded_set(parts, rate, simtime))
    return spikes


def compare(current, full, rate, indexes):
    """
    Compares two data files to see if they contain similar data.

    Ignoring data not recorded due to sampling rate or indexes.

    The current data is also read from file so that any float changes \
        due to read write are the same.

    :param current:
    :param full:
    :param rate:
    :param indexes:
    """
    print current
    d1 = numpy.loadtxt(current, delimiter=',')
    print d1.shape
    if len(d1.shape) == 1:
        d1 = numpy.transpose(numpy.array([d1]))
    print full
    d2 = numpy.loadtxt(full, delimiter=',')
    if indexes is None:
        d2_rate = d2[::rate]
    else:
        d2_rate = d2[::rate, indexes]
    print d2_rate.shape
    if not numpy.array_equal(d1, d2_rate):
        if d1.shape != d2_rate.shape:
            raise Exception(
                "Shape not equal {} {}".format(d1.shape, d2_rate.shape))
        for i in xrange(d1.shape[0]):
            if not numpy.array_equal(d1[i], d2_rate[i]):
                print "row {}".format(i)
                print d1[i]
                print d2_rate[i]
                raise Exception("not equal")


class TestSampling(BaseTestCase):

    def test_big_with_rate(self):
        simtime = 20000
        n_neurons = 500
        run_and_compare_script(
            simtime, n_neurons,
            record_spikes=True, spike_rate=2,
            record_v=True, v_rate=3,
            record_exc=True, exc_rate=4,
            record_inh=True, inh_rate=5,
            tollerance=simtime-2)

    def test_big_with_rec_index(self):
        simtime = 20000
        n_neurons = 500
        run_and_compare_script(
            simtime, n_neurons,
            record_spikes=True, spike_rate=1,
            spike_rec_indexes=range(0, n_neurons, 2),
            record_v=True, v_rate=1, v_indexes=range(0, n_neurons, 2),
            record_exc=True, exc_rate=1, exc_indexes=range(0, n_neurons, 3),
            record_inh=True, inh_rate=1, inh_indexes=range(0, n_neurons, 4))

    def test_big_with_get_index(self):
        simtime = 500
        n_neurons = 500
        run_and_compare_script(
            simtime, n_neurons,
            record_spikes=True, spike_rate=1,
            spike_get_indexes=range(0, n_neurons, 2),
            record_v=True, v_rate=1, v_indexes=range(0, n_neurons, 2),
            record_exc=True, exc_rate=1, exc_indexes=range(0, n_neurons, 3),
            record_inh=True, inh_rate=1, inh_indexes=range(0, n_neurons, 4))

    def test_big_with_both(self):
        simtime = 20000
        n_neurons = 500
        run_and_compare_script(
            simtime, n_neurons,
            record_spikes=True, spike_rate=5,
            spike_rec_indexes=range(0, n_neurons, 2),
            record_v=True, v_rate=4, v_indexes=range(0, n_neurons, 2),
            record_exc=True, exc_rate=3, exc_indexes=range(0, n_neurons, 3),
            record_inh=True, inh_rate=2, inh_indexes=range(0, n_neurons, 4))

    def test_medium_split(self):
        simtime = 5000
        n_neurons = 500
        run_and_compare_script(
            simtime, n_neurons, run_split=5,
            record_spikes=True, spike_rate=5,
            spike_rec_indexes=range(0, n_neurons, 2),
            record_v=True, v_rate=4, v_indexes=range(0, n_neurons, 2),
            record_exc=True, exc_rate=3, exc_indexes=range(0, n_neurons, 3),
            record_inh=True, inh_rate=2, inh_indexes=range(0, n_neurons, 4))

    def test_one(self):
        simtime = 500
        n_neurons = 300
        run_and_compare_script(
            simtime, n_neurons,
            record_spikes=True, spike_rate=5,
            spike_rec_indexes=[0],
            record_v=True, v_indexes=[0],
            record_exc=True, exc_indexes=[0],
            record_inh=True, inh_indexes=[0])


if __name__ == '__main__':
    simtime = 20000
    n_neurons = 500

    run_and_compare_script(
        simtime, n_neurons,
        record_spikes=True, spike_rate=2, spike_indexes=None,
        record_v=True, v_rate=3, v_indexes=None,
        record_exc=True, exc_rate=4, exc_indexes=None,
        record_inh=True, inh_rate=5, inh_indexes=None)
    """
    file_path = os.path.join(current_file_path, "20000_500_spikes.csv")
    full_path = os.path.join(current_file_path, "master_20000_500_spikes.csv")
    compare_spikes(file_path, full_path)
    """
