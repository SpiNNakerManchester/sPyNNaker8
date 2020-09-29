import spynnaker8 as p
from time import sleep
import traceback


sim_finished = False
n_spikes = list()
n_spikes.append(0)


def recv(label, time, neuron_ids):
    """ Receive spikes and add the number received to the current segment count
    """
    global n_spikes
    print("Time: {}; Received spikes from {}:{}".format(
        time, label, neuron_ids))
    n_spikes[len(n_spikes) - 1] += len(neuron_ids)


def send_sync(label, conn):
    """ Send "continue" signal after a delay and update the current segment
    """
    global sim_finished
    global n_spikes
    while not sim_finished:
        sleep(0.1)
        if not sim_finished:
            print("Sending sync")
            try:
                n_spikes.append(0)
                p.external_devices.continue_simulation()
            except Exception:
                traceback.print_exc()


def stop(label, conn):
    """ Mark the simulation finished to stop sending the sync signal
    """
    global sim_finished
    sim_finished = True


def test_live_sync():
    """ Test the synchronisation from host behaviour by receiving live spikes
        and checking that the right spikes only arrive after synchronisation
    """
    global sim_finished
    global n_spikes
    conn = p.external_devices.SpynnakerLiveSpikesConnection(
        receive_labels=["ssa"], local_port=None)
    conn.add_receive_callback("ssa", recv)
    conn.add_start_resume_callback("ssa", send_sync)
    conn.add_pause_stop_callback("ssa", stop)

    p.setup(1.0)
    pop = p.Population(
        100, p.SpikeSourceArray([[i] for i in range(100)]), label="ssa")
    p.external_devices.activate_live_output_for(
        pop, database_notify_port_num=conn.local_port)

    p.external_devices.run_sync(100, 20)
    sim_finished = True
    p.end()

    # 20 spikes should be in each range
    for i in range(5):
        assert(n_spikes[i] == 20)
