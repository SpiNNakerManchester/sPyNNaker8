from neo import AnalogSignalArray, AnalogSignal, SpikeTrain
from quantities import ms
import numpy as np


def convert_analog_signal(data):
    raise NotImplementedError("AnalogSignal")


def convert_analog_signalarray(signal_array, time_unit=ms):
    ids = signal_array.channel_index
    times = signal_array.times.rescale(time_unit)
    all_times = np.tile(times, len(ids))
    neurons = np.repeat(ids, len(times))
    # I am unsure of what happens if ids is not a contious list of integers
    values = np.concatenate(map(lambda x: signal_array[:, x], ids))
    return np.column_stack((neurons, all_times, values))


def convert_data(data, name, run=0):
    """
    Converts the data into a numpy array in the format id, time, value

    :param data: Data as returned by a getData() call
    :type data: SpynnakerNeoBlock
    :param name: Nane of the data to be extracted.
        Same values as used in getData()
    :type str
    :param run: Zero based index of the run to extract data for
    :type int
    :return: nparray
    """
    print name
    print type(data)
    if len(data.segments) <= run:
        raise ValueError("Data only contains {} so unable to run {}. "
                         "Note run is the zero based index."
                         "".format(len(data.segments), run))
    if name == "all":
        raise ValueError("Unable to convert all data in one go "
                         "as result would be comparing apples and oranges.")
    temp = data.segments[run].filter(name=name)
    print type(temp)
    print type(temp[0])
    print len(temp)
    return convert_analog_signalarray(data.segments[run].filter(name=name)[0])


def convert_data_list(data, name, runs=None):
    """
    Converts the data into a numpy array in the format id, time, value

    :param data: Data as returned by a getData() call
    :type data: SpynnakerNeoBlock
    :param name: Nane of the data to be extracted.
        Same values as used in getData()
    :type str
    :param runs: List of Zero based index of the run to extract data for.
        Or None to extract all runs
    :return: [nparray]
    """
    results = []
    if runs is None:
        runs = range(len(data.segments))
    for run in runs:
        results.append(convert_data(data, name, run=run))
    return results


def convert_gsyn(gsyn_exc, gsyn_inh):
    exc = gsyn_exc.segments[0].filter(name='gsyn_exc')[0]
    inh = gsyn_inh.segments[0].filter(name='gsyn_inh')[0]
    ids = exc.channel_index
    ids2 = inh.channel_index
    if (len(ids) != len(ids2)):
        error = "Found {} neuron ids in gsyn_exc but {} in  gsyn_inh" \
                "".format(len(ids), len(ids2))
        raise ValueError(error)
    if (not np.allclose(ids, ids2)):
        print ids
        print "different to"
        print ids2
        raise ValueError("ids in gsyn_exc and gsyn_inh do not match")
    times = exc.times.rescale(ms)
    times2 = inh.times.rescale(ms)
    if (len(times) != len(times2)):
        error = "Found {} times in gsyn_exc but {} in  gsyn_inh" \
                "".format(len(times), len(times))
        raise ValueError(error)
    if (not np.allclose(times, times2)):
        print times
        print "different to"
        print times2
        raise ValueError("times in gsyn_exc and gsyn_inh do not match")
    all_times = np.tile(times, len(ids))
    neurons = np.repeat(ids, len(times))
    exc_np = np.concatenate(map(lambda x: exc[:, x], range(len(ids))))
    inh_np = np.concatenate(map(lambda x: inh[:, x], range(len(ids))))
    return np.column_stack((neurons, all_times, exc_np, inh_np))


def convert_spiketrains(spiketrains):
    print "spiketrain"
    print type(spiketrains)
    print type(spiketrains[0])
    neurons = np.concatenate(map(lambda x:
                                 np.full_like(x, x.annotations['source_index']),
                                 spiketrains))
    spikes = np.concatenate(spiketrains, axis=0)
    return np.column_stack((neurons, spikes))


def convert_spikes(spikes):
    return convert_spiketrains(spikes.segments[0].spiketrains)

