# imports of both spynnaker and external device plugin.
import Tkinter as tk
import spynnaker8 as Frontend
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt
import spynnaker8_external_devices_plugin.pyNN as ExternalDevices
from spynnaker8_external_devices_plugin.pyNN import \
    SpynnakerLiveSpikesConnection


class PyNNScript(object):
    """
    the class which contains the pynn script
    """

    def __init__(self):

        # initial call to set up the front end (pynn requirement)
        Frontend.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)

        use_c_visualiser = True
        use_spike_injector = True

        # neurons per population and the length of runtime in ms for the
        # simulation, as well as the expected weight each spike will contain
        self.n_neurons = 100

        # set up gui
        p = None
        if use_spike_injector:
            from multiprocessing import Process
            from multiprocessing import Event
            ready = Event()
            p = Process(target=GUI, args=[self.n_neurons, ready])
            p.start()
            ready.wait()

        # different runtimes for demostration purposes
        run_time = None
        if not use_c_visualiser and not use_spike_injector:
            run_time = 1000
        elif use_c_visualiser and not use_spike_injector:
            run_time = 1000
        elif use_c_visualiser and use_spike_injector:
            run_time = 1000
        elif not use_c_visualiser and use_spike_injector:
            run_time = 1000

        weight_to_spike = 2.0

        # neural parameters of the IF_curr model used to respond to injected
        # spikes.
        # (cell params for a synfire chain)
        cell_params_lif = {'cm': 0.25,
                           'i_offset': 0.0,
                           'tau_m': 20.0,
                           'tau_refrac': 2.0,
                           'tau_syn_E': 5.0,
                           'tau_syn_I': 5.0,
                           'v_reset': -70.0,
                           'v_rest': -65.0,
                           'v_thresh': -50.0
                           }

        ##################################
        # Parameters for the injector population.  This is the minimal set of
        # parameters required, which is for a set of spikes where the key is
        # not important.  Note that a virtual key *will* be assigned to the
        # population, and that spikes sent which do not match this virtual key
        # will be dropped; however, if spikes are sent using 16-bit keys, they
        # will automatically be made to match the virtual key.  The virtual
        # key assigned can be obtained from the database.
        ##################################
        cell_params_spike_injector = {

            # The port on which the spiNNaker machine should listen for
            # packets. Packets to be injected should be sent to this port on
            # the spiNNaker machine
            'port': 12345
        }

        ##################################
        # Parameters for the injector population.  Note that each injector
        # needs to be given a different port.  The virtual key is assigned
        # here, rather than being allocated later.  As with the above, spikes
        # injected need to match this key, and this will be done automatically
        # with 16-bit keys.
        ##################################
        cell_params_spike_injector_with_key = {

            # The port on which the spiNNaker machine should listen for
            # packets. Packets to be injected should be sent to this port on
            # the spiNNaker machine
            'port': 12346,

            # This is the base key to be used for the injection, which is used
            # to allow the keys to be routed around the spiNNaker machine.
            # This assignment means that 32-bit keys must have the high-order
            # 16-bit set to 0x7; This will automatically be prepended to
            # 16-bit keys.
            'virtual_key': 0x70000
        }

        # create synfire populations (if cur exp)
        pop_forward = Frontend.Population(
            self.n_neurons, Frontend.IF_curr_exp(**cell_params_lif),
            label='pop_forward')
        pop_backward = Frontend.Population(
            self.n_neurons, Frontend.IF_curr_exp(**cell_params_lif),
            label='pop_backward')

        # Create injection populations
        injector_forward = None
        injector_backward = None
        if use_spike_injector:
            injector_forward = Frontend.Population(
                self.n_neurons,
                ExternalDevices.SpikeInjector(
                    **cell_params_spike_injector_with_key),
                label='spike_injector_forward')
            injector_backward = Frontend.Population(
                self.n_neurons,
                ExternalDevices.SpikeInjector(
                    **cell_params_spike_injector),
                label='spike_injector_backward')
        else:
            spike_times = []
            for _ in range(0, self.n_neurons):
                spike_times.append([])
            spike_times[0] = [0]
            spike_times[20] = [(run_time / 100) * 20]
            spike_times[40] = [(run_time / 100) * 40]
            spike_times[60] = [(run_time / 100) * 60]
            spike_times[80] = [(run_time / 100) * 80]
            cell_params_forward = {'spike_times': spike_times}
            spike_times_backwards = []
            for _ in range(0, self.n_neurons):
                spike_times_backwards.append([])
            spike_times_backwards[0] = [(run_time / 100) * 80]
            spike_times_backwards[20] = [(run_time / 100) * 60]
            spike_times_backwards[40] = [(run_time / 100) * 40]
            spike_times_backwards[60] = [(run_time / 100) * 20]
            spike_times_backwards[80] = [0]
            cell_params_backward = {'spike_times': spike_times_backwards}
            injector_forward = Frontend.Population(
                self.n_neurons, Frontend.SpikeSourceArray(
                    **cell_params_forward),
                label='spike_injector_forward')
            injector_backward = Frontend.Population(
                self.n_neurons, Frontend.SpikeSourceArray(
                    **cell_params_backward),
                label='spike_injector_backward')

        # Create a connection from the injector into the populations
        Frontend.Projection(
            injector_forward, pop_forward,
            Frontend.OneToOneConnector(),
            Frontend.StaticSynapse(weight=weight_to_spike))
        Frontend.Projection(
            injector_backward, pop_backward,
            Frontend.OneToOneConnector(),
            Frontend.StaticSynapse(weight=weight_to_spike))

        # Synfire chain connections where each neuron is connected to its next
        # neuron
        # NOTE: there is no recurrent connection so that each chain stops once
        # it reaches the end
        loop_forward = list()
        loop_backward = list()
        for i in range(0, self.n_neurons - 1):
            loop_forward.append((i, (i + 1) %
                                 self.n_neurons, weight_to_spike, 3))
            loop_backward.append(((i + 1) %
                                  self.n_neurons, i, weight_to_spike, 3))
        Frontend.Projection(pop_forward, pop_forward,
                            Frontend.FromListConnector(loop_forward))
        Frontend.Projection(pop_backward, pop_backward,
                            Frontend.FromListConnector(loop_backward))

        # record spikes from the synfire chains so that we can read off valid
        # results in a safe way afterwards, and verify the behavior
        pop_forward.record('spikes')
        pop_backward.record('spikes')

        # Activate the sending of live spikes
        ExternalDevices.activate_live_output_for(
            pop_forward, database_notify_host="localhost",
            database_notify_port_num=19996)
        ExternalDevices.activate_live_output_for(
            pop_backward, database_notify_host="localhost",
            database_notify_port_num=19996)

        if not use_c_visualiser:
            # if not using the c visualiser, then a new spynnaker live spikes
            # connection is created to define that there are python code which
            # receives the outputted spikes.
            live_spikes_connection_receive = SpynnakerLiveSpikesConnection(
                receive_labels=["pop_forward", "pop_backward"],
                local_port=19999, send_labels=None)

            # Set up callbacks to occur when spikes are received
            live_spikes_connection_receive.add_receive_callback(
                "pop_forward", receive_spikes)
            live_spikes_connection_receive.add_receive_callback(
                "pop_backward", receive_spikes)

        # Run the simulation on spiNNaker
        Frontend.run(run_time)

        # Retrieve spikes from the synfire chain population
        spikes_forward = pop_forward.get_data('spikes')
        spikes_backward = pop_backward.get_data('spikes')

        # Clear data structures on spiNNaker to leave the machine in a clean
        # state for future executions
        Frontend.end()

        if use_spike_injector:
            p.join()

        Figure(
            # raster plot of the presynaptic neuron spike times
            Panel(spikes_forward.segments[0].spiketrains,
                  yticks=True, markersize=0.2, xlim=(0, run_time)),
            Panel(spikes_backward.segments[0].spiketrains,
                  yticks=True, markersize=0.2, xlim=(0, run_time)),
            title="Simple synfire chain example with injected spikes",
            annotations="Simulated with {}".format(Frontend.name())
        )
        plt.show()


# Create a receiver of live spikes
def receive_spikes(label, time, neuron_ids):
    for neuron_id in neuron_ids:
        print "Received spike at time", time, "from", label, "-", neuron_id


class GUI(object):
    """ Simple gui to demostrate live inejction of the spike io script.
    """

    def __init__(self, n_neurons, ready):
        self._n_neurons = n_neurons

        # Set up the live connection for sending and receiving spikes
        self._live_spikes_connection = SpynnakerLiveSpikesConnection(
            receive_labels=None, local_port=19996,
            send_labels=["spike_injector_forward",
                         "spike_injector_backward"])

        # Set up callbacks to occur at the start of simulation
        self._live_spikes_connection.add_start_callback(
            "spike_injector_forward", self.start)

        self._root = tk.Tk()
        self._root.title("Injecting Spikes GUI")
        label = tk.Label(self._root, fg="dark green")
        label.pack()
        neuron_id_value = tk.IntVar()
        self._neuron_id = tk.Spinbox(
            self._root, from_=0, to=self._n_neurons - 1,
            textvariable=neuron_id_value)
        self._neuron_id.pack()
        pop_label_value = tk.StringVar()
        self._pop_label = tk.Spinbox(
            self._root, textvariable=pop_label_value,
            values=("spike_injector_forward", "spike_injector_backward"))
        self._pop_label.pack()
        self._button = tk.Button(
            self._root, text='Inject', width=25, command=self.inject_spike,
            state="disabled")
        self._button.pack()

        ready.set()

        self._root.mainloop()

    def start(self, pop_label, connection):
        self._button["state"] = "normal"

    def inject_spike(self):
        neuron_id = int(self._neuron_id.get())
        label = str(self._pop_label.get())
        print "injecting with neuron_id {} to pop {}".format(neuron_id, label)
        self._live_spikes_connection.send_spike(label, neuron_id)


# set up the initial script
if __name__ == '__main__':
    from multiprocessing import freeze_support
    freeze_support()
    script = PyNNScript()
