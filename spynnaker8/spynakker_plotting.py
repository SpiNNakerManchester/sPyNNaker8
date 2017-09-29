from neo import AnalogSignalArray, SpikeTrain
from neo import Block, Segment
import numpy as np
from quantities import ms
try:
    from pyNN.utility.plotting import repeat
    import matplotlib.pyplot as plt
    matplotlib_missing = False
except Exception as e:
    matplotlib_missing = True

"""
Plotting tools to be unsed together with
https://github.com/NeuralEnsemble/PyNN/blob/master/pyNN/utility/plotting.py
"""


def handle_options(ax, options):
    """
    Handles options that can not be passed to axes.plot

    Removes the ones it has handled

    axes.plot will throw an exception if it gets unwanted options

    :param ax: An Axes in a matplot lib figure
    :type ax: matplotlib.axes
    :param options: All options the plotter can be configured with
    """
    if "xticks" not in options or options.pop("xticks") is False:
        plt.setp(ax.get_xticklabels(), visible=False)
    if "xlabel" in options:
        ax.set_xlabel(options.pop("xlabel"))
    else:
        ax.set_xlabel("Time (ms)")
    if "yticks" not in options or options.pop("yticks") is False:
        plt.setp(ax.get_yticklabels(), visible=False)
    if "ylabel" in options:
        ax.set_ylabel(options.pop("ylabel"))
    else:
        ax.set_ylabel("Neuron index")
    if "ylim" in options:
        ax.set_ylim(options.pop("ylim"))
    if "xlim" in options:
        ax.set_xlim(options.pop("xlim"))


def plot_spikes(ax, spike_times, neurons, label='', **options):
    """
    Plots the spikes based on two lists

    :param ax: An Axes in a matplot lib figure
    :param spike_times: List of Spiketimes
    :param neurons: List of Neuron Ids
    :param label: Label for the graph
    :param options: plotting options
    """
    if len(neurons) > 0:
        max_index = max(neurons)
        min_index = min(neurons)
        ax.plot(spike_times, neurons, 'b.', **options)
        ax.set_ylim(-0.5 + min_index, max_index + 0.5)
    if label:
        plt.text(0.95, 0.95, label,
                 transform=ax.transAxes, ha='right', va='top',
                 bbox=dict(facecolor='white', alpha=1.0))


def plot_spiketrains(ax, spiketrains, label='', **options):
    """

    Plot all spike trains in a Segment in a raster plot.

    :param ax: An Axes in a matplot lib figure
    :param spiketrains: List of spiketimes
    :param label: Label for the graph
    :param options: plotting options
    """
    ax.set_xlim(0, spiketrains[0].t_stop / ms)
    handle_options(ax, options)
    neurons = np.concatenate(map(lambda x:
                                 np.repeat(x.annotations['source_index'],
                                           len(x)),
                                 spiketrains))
    spike_times = np.concatenate(spiketrains, axis=0)
    plot_spikes(ax, spike_times, neurons, label=label, **options)


def plot_spikes_numpy(ax, spikes, label='', **options):
    """
    Plot all spike

    :param ax: An Axes in a matplot lib figure
    :param spikes: spynakker7 format nparray of spikes
    :param label: Label for the graph
    :param options: plotting options
    """
    handle_options(ax, options)
    neurons = spikes[:, 0]
    spike_times = spikes[:, 1]
    plot_spikes(ax, spike_times, neurons, label=label, **options)


def heat_plot(ax, neurons, times, values, label='', **options):
    """
    Plots three lists of neurons, times and values into a heatmap

    :param ax: An Axes in a matplot lib figure
    :param neurons: List of Neuron ids
    :param times: List of times
    :param values: List of values to plot
    :param label: Label for the graph
    :param options: plotting options
    """
    handle_options(ax, options)
    info_array = np.empty((max(neurons)+1, max(times)+1))
    info_array[:] = np.nan
    info_array[neurons, times] = values
    heat_map = ax.imshow(info_array, cmap='hot', interpolation='none',
                         origin='lower', aspect='auto')
    ax.figure.colorbar(heat_map)
    if label:
        plt.text(0.95, 0.95, label,
                 transform=ax.transAxes, ha='right', va='top',
                 bbox=dict(facecolor='white', alpha=1.0))


def heat_plot_numpy(ax, data, label='', **options):
    """
    Plots neurons, times and values into a heatmap

    :param ax: An Axes in a matplot lib figure
    :param data: nparray of values in spknakker7 format
    :param label: Label for the graph
    :param options: plotting options
    """
    neurons = data[:, 0].astype(int)
    times = data[:, 1].astype(int)
    values = data[:, 2]
    heat_plot(ax, neurons, times, values, label='', **options)


def heat_plot_neo(ax, signal_array, label='', **options):
    """
    Plots neurons, times and values into a heatmap

    :param ax: An Axes in a matplot lib figure
    :param signal_array: Neo Signal array Object
    :param label: Label for the graph
    :param options: plotting options
    """
    if label is None:
        label = signal_array.name
    ids = signal_array.channel_index.astype(int)
    times = signal_array.times.magnitude.astype(int)
    all_times = np.tile(times, len(ids))
    neurons = np.repeat(ids, len(times))
    values = np.concatenate(map(lambda x: signal_array[:, x].magnitude, ids))
    heat_plot(ax, neurons, all_times, values, label=label, **options)


def plot_segment(axes, segment, label='', **options):
    """
    Plots a segment into a plot of spikes or a heatmap

    If there is more than ode type of Data in the segment options must
        include the name of the data to plot

    Note: method signature defined by pynn plotting
        This allows mixing of this plotting tool and pynn's

    :param axes: An Axes in a matplot lib figure
    :param segment: Data for one run to plot
    :param label: Label for the graph
    :param options: plotting options
    """
    if "name" in options:
        name = options.pop("name")
        if name == 'spikes':
            plot_spiketrains(axes, segment.spiketrains, label=label, **options)
        else:
            heat_plot_neo(axes, segment.filter(name=name)[0], label=label,
                          **options)
    elif len(segment.spiketrains) > 0:
        if len(segment.analogsignalarrays) > 1:
            raise Exception("Block.segment[0] has spikes and "
                            "other data please specifiy one "
                            "to plot")
        plot_spiketrains(axes, segment.spiketrains, label=label, **options)
    elif len(segment.analogsignalarrays) == 1:
        heat_plot_neo(axes, segment.analogsignalarrays[0], label=label,
                      **options)
    elif len(segment.analogsignalarrays) > 1:
        raise Exception("Block.segment[0] has {} types of data "
                        "please specify one to plot using name="
                        "" % len(segment.analogsignalarrays))
    else:
        raise Exception("Block does not appear to hold any data")


class SpynakkerPanel(object):
    """
    Represents a single panel in a multi-panel figure.

    Compatable with pyNN.utility.plotting's Frame and
        can be mixed with pyNN.utility.plotting's Panel

    Unlike pyNN.utility.plotting Panel
        Spikes are plotted faster
        other data is plotted as a heatmap

    A panel is a Matplotlib Axes or Subplot instance. A data item may be an
    AnalogSignal, AnalogSignalArray, or a list of SpikeTrains. The Panel will
    automatically choose an appropriate representation. Multiple data items may
    be plotted in the same panel.

    Valid options are any valid Matplotlib formatting options that should be
    applied to the Axes/Subplot, plus in addition:

        `data_labels`:
            a list of strings of the same length as the number of data items.
        `line_properties`:
            a list of dicts containing Matplotlib formatting options, of the
            same length as the number of data items.


    Whole Neo Objects can be passed in as long as they
        contain a single Segment/run
        and only contain one type of data
    Whole Segments can be passed in only if they only contain one type of data

    """

    def __init__(self, *data, **options):
        if matplotlib_missing:
            raise Exception("No matplotlib module found")
        self.data = list(data)
        self.options = options
        self.data_labels = options.pop("data_labels", repeat(None))
        self.line_properties = options.pop("line_properties", repeat({}))

    def plot(self, axes):
        """
        Plot the Panel's data in the provided Axes/Subplot instance.
        """
        for datum, label, properties in zip(self.data, self.data_labels,
                                            self.line_properties):
            properties.update(self.options)
            # Support lists length one
            # for example result of segments[0].filter(name='v')
            if isinstance(datum, list):
                if len(datum) == 0:
                    raise Exception("Can't handle empty list")
                if len(datum) == 1 and not isinstance(datum[0], SpikeTrain):
                    datum = datum[0]
            if isinstance(datum, list):
                if isinstance(datum[0], SpikeTrain):
                    plot_spiketrains(axes, datum, label=label, **properties)
                else:
                    raise Exception("Can't handle lists of type %s"
                                    "" % type(datum))
            # AnalogSignalArray is also a ndarray but data format different!
            elif isinstance(datum, AnalogSignalArray):
                heat_plot_neo(axes, datum, label=label, **properties)
            elif isinstance(datum, np.ndarray):
                if len(datum[0]) == 2:
                    plot_spikes_numpy(axes, datum, label=label, **properties)
                elif len(datum[0]) == 3:
                    heat_plot_numpy(axes, datum, label=label, **properties)
                else:
                    raise Exception("Can't handle ndarray with %s columns"
                                    "" % len(datum[0]))
            elif isinstance(datum, Block):
                if "run" in properties:
                    run = int(properties.pop("run"))
                    if len(datum.segments) <= run:
                        raise Exception("Block only has {} segments"
                                        "" % len(datum.segments))
                    segment = datum.segments[run]
                else:
                    if len(datum.segments) != 1:
                        raise Exception("Block has {} segments please "
                                        "specifiy one to plot using run="
                                        "" % len(datum.segments))
                    segment = datum.segments[0]
                plot_segment(axes, segment, label=label, **properties)
            elif isinstance(datum, Segment):
                plot_segment(axes, datum, label=label, **properties)
            else:
                raise Exception("Can't handle type %s Consider using "
                                "pyNN.utility.plotting" % type(datum))
