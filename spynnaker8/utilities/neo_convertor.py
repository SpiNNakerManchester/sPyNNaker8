from quantities import ms
import numpy as np


def convert_analog_signalarray(signal_array, time_unit=ms):
    """
    Converts part of a NEO object into told spynakker7 format

    :param signal_array: Extended Quantities object
    :param time_unit: Data time unit for time index
    :rtype ndarray
    """
    ids = signal_array.channel_index
    if time_unit == ms:
        times = signal_array.times.magnitude
    else:
        times = signal_array.times.rescale(time_unit).magnitude
    all_times = np.tile(times, len(ids))
    neurons = np.repeat(ids, len(times))
    # I am unsure of what happens if ids is not a contious list of integers
    values = np.concatenate(map(lambda x: signal_array[:, x].magnitude, ids))
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
    if len(data.segments) <= run:
        raise ValueError("Data only contains {} so unable to run {}. "
                         "Note run is the zero based index."
                         "".format(len(data.segments), run))
    if name == "all":
        raise ValueError("Unable to convert all data in one go "
                         "as result would be comparing apples and oranges.")
    if name == "spikes":
        return convert_spikes(data, run)
    return convert_analog_signalarray(data.segments[run].filter(name=name)[0])


def convert_data_list(data, name, runs=None):
    """
    Converts the data into a list of numpy arrays in the format id, time, value

    :param data: Data as returned by a getData() call
    :type data: SpynnakerNeoBlock
    :param name: Name of the data to be extracted.
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


def convert_v_list(data):
    """
    Converts the voltage into a list numpy array one per segment (all runs)
    in the format id, time, value

    :type data: SpynnakerNeoBlock Must have v data
    :return: [nparray]
    """
    return convert_data_list(data, "v", runs=None)


def convert_gsyn_exc_list(data):
    """
    Converts the gsyn_exc into a list numpy array one per segment (all runs)
    in the format id, time, value

    :type data: SpynnakerNeoBlock Must have gsyn_exc data
    :return: [nparray]
    """
    return convert_data_list(data, "gsyn_exc", runs=None)


def convert_gsyn_inh_list(data):
    """
    Converts the gsyn_inh into a list numpy array one per segment (all runs)
    in the format id, time, value

    :type data: SpynnakerNeoBlock Must have gsyn_exc data
    :return: [nparray]
    """
    return convert_data_list(data, "gsyn_inh", runs=None)


def convert_gsyn(gsyn_exc, gsyn_inh):
    """
    Converts two neo objects into the spynakker7 format

    Note: It is acceptable for both neo parameters to be the same object

    :param gsyn_exc: neo with gsyn_exc data
    :param gsyn_inh: neo with gsyn_exc data
    :rtype nparray
    """
    exc = gsyn_exc.segments[0].filter(name='gsyn_exc')[0]
    inh = gsyn_inh.segments[0].filter(name='gsyn_inh')[0]
    ids = exc.channel_index
    ids2 = inh.channel_index
    if (len(ids) != len(ids2)):
        error = "Found {} neuron ids in gsyn_exc but {} in  gsyn_inh" \
                "".format(len(ids), len(ids2))
        raise ValueError(error)
    if (not np.allclose(ids, ids2)):
        raise ValueError("ids in gsyn_exc and gsyn_inh do not match")
    times = exc.times.rescale(ms)
    times2 = inh.times.rescale(ms)
    if (len(times) != len(times2)):
        error = "Found {} times in gsyn_exc but {} in  gsyn_inh" \
                "".format(len(times), len(times))
        raise ValueError(error)
    if (not np.allclose(times, times2)):
        raise ValueError("times in gsyn_exc and gsyn_inh do not match")
    all_times = np.tile(times, len(ids))
    neurons = np.repeat(ids, len(times))
    exc_np = np.concatenate(map(lambda x: exc[:, x], range(len(ids))))
    inh_np = np.concatenate(map(lambda x: inh[:, x], range(len(ids))))
    return np.column_stack((neurons, all_times, exc_np, inh_np))


def convert_spiketrains(spiketrains):
    """
    Converts a list of spiketrains into spynakker7 format

    :param spiketrains: List of SpikeTrains
    :rtype nparray
    """
    neurons = np.concatenate(map(lambda x:
                                 np.repeat(x.annotations['source_index'],
                                           len(x)),
                                 spiketrains))
    spikes = np.concatenate(map(lambda x: x.magnitude, spiketrains))
    return np.column_stack((neurons, spikes))


def convert_spikes(neo, run=0):
    """
    Extracts the spikes for run one from a Neo Object

    :param neo: neo Object incliding Spike Data
    :param run: Zero based index of the run to extract data for
    :type int
    :rtype nparray
    """
    if len(neo.segments) <= run:
        raise ValueError("Data only contains {} so unable to run {}. "
                         "Note run is the zero based index."
                         "".format(len(neo.segments), run))
    return convert_spiketrains(neo.segments[run].spiketrains)


def count_spiketrains(spiketrains):
    """
    Help function to count the number of spikes in a list of spiketrains

    :param spiketrains: List of SpikeTrains
    :return Total number of spikes in all the spiketrains
    """
    return sum(map(len, spiketrains))


def count_spikes(neo):
    """
    Help function to count the number of spikes in a list of spiketrains

    Only counts run 0

    :param neo: Neo Object which has spikes in it
    :return:
    """
    return count_spiketrains(neo.segments[0].spiketrains)
