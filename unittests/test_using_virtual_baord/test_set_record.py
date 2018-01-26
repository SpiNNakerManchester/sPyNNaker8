import spynnaker8 as sim
from spynnaker.pyNN.models.common import NeuronRecorder
from p8_integration_tests.base_test_case import BaseTestCase


class TestSetRecord(BaseTestCase):

    def test_set_spikes(self):
        sim.setup(timestep=1)
        if_curr = sim.Population(1, sim.IF_curr_exp())
        self.assertItemsEqual([], if_curr._get_all_recording_variables())
        ssa = sim.Population(
            1, sim.SpikeSourceArray(spike_times=[0]))
        ssp = sim.Population(2, sim.SpikeSourcePoisson(rate=100.0, seed=1))
        if_curr.record("spikes")
        self.assertItemsEqual(
            ["spikes"], if_curr._get_all_recording_variables())
        ssa.record("spikes")
        ssp.record("spikes")
        sim.end()

    def test_set_v(self):
        sim.setup(timestep=1)
        if_curr = sim.Population(1, sim.IF_curr_exp())
        ssa = sim.Population(
            1, sim.SpikeSourceArray(spike_times=[0]))
        ssp = sim.Population(2, sim.SpikeSourcePoisson(rate=100.0, seed=1))
        if_curr.record("v")

        try:
            ssa.record("v")
        except Exception as e:
            self.assertEqual(
                "This population does not support the recording of v!",
                e.message)
        try:
            ssp.record("v")
        except Exception as e:
            self.assertEqual(
                "This population does not support the recording of v!",
                e.message)

        sim.end()

    def test_set_all(self):
        sim.setup(timestep=1)
        if_curr = sim.Population(1, sim.IF_curr_exp())
        ssa = sim.Population(
            1, sim.SpikeSourceArray(spike_times=[0]))
        ssp = sim.Population(2, sim.SpikeSourcePoisson(rate=100.0, seed=1))
        if_curr.record("all")
        self.assertItemsEqual(["spikes", "v", "gsyn_inh", "gsyn_exc"],
                              if_curr._get_all_recording_variables())
        ssa.record("all")
        self.assertItemsEqual(["spikes"],
                              ssa._get_all_recording_variables())
        ssp.record("all")
        self.assertItemsEqual(["spikes"],
                              ssp._get_all_recording_variables())
        sim.end()

    def test_set_spikes_interval(self):
        sim.setup(timestep=1)
        if_curr = sim.Population(1, sim.IF_curr_exp())
        recorder = if_curr._vertex._neuron_recorder
        self.assertItemsEqual([], if_curr._get_all_recording_variables())
        ssa = sim.Population(
            1, sim.SpikeSourceArray(spike_times=[0]))
        ssp = sim.Population(2, sim.SpikeSourcePoisson(rate=100.0, seed=1))
        if_curr.record("spikes", sampling_interval=2)
        ssa.record("spikes", sampling_interval=2)
        ssp.record("spikes", sampling_interval=2)
        self.assertItemsEqual(
            ["spikes"], if_curr._get_all_recording_variables())
        assert recorder.get_neuron_sampling_interval("spikes") == 2

    def test_set_spikes_interval2(self):
        sim.setup(timestep=0.5)
        if_curr = sim.Population(1, sim.IF_curr_exp())
        recorder = if_curr._vertex._neuron_recorder
        self.assertItemsEqual([], if_curr._get_all_recording_variables())
        if_curr.record("spikes", sampling_interval=2.5)
        self.assertItemsEqual(
            ["spikes"], if_curr._get_all_recording_variables())
        assert recorder.get_neuron_sampling_interval("spikes") == 2.5

    def test_set_spikes_indexes(self):
        sim.setup(timestep=1)
        if_curr = sim.Population(5, sim.IF_curr_exp())
        recorder = if_curr._vertex._neuron_recorder
        ssa = sim.Population(
            5, sim.SpikeSourceArray(spike_times=[0]))
        ssp = sim.Population(5, sim.SpikeSourcePoisson(rate=100.0, seed=1))
        if_curr.record("spikes", indexes=[1, 2, 4])
        ssa.record("spikes", indexes=[1, 2, 4])
        ssp.record("spikes", indexes=[1, 2, 4])
        self.assertItemsEqual(
            ["spikes"], if_curr._get_all_recording_variables())
        assert recorder._indexes["spikes"] == [1, 2, 4]

    def test_set_spikes_indexes2(self):
        sim.setup(timestep=1)
        if_curr = sim.Population(5, sim.IF_curr_exp())
        recorder = if_curr._vertex._neuron_recorder
        if_curr.record("spikes", indexes=[1, 2, 4])
        if_curr.record("spikes", indexes=[1, 3])
        self.assertItemsEqual(
            ["spikes"], if_curr._get_all_recording_variables())
        assert recorder._indexes["spikes"] == [1, 2, 3, 4]

    def test_turn_off_spikes_indexes(self):
        sim.setup(timestep=1)
        if_curr = sim.Population(5, sim.IF_curr_exp())
        if_curr.record("spikes")
        if_curr.record(None)
        self.assertItemsEqual([], if_curr._get_all_recording_variables())

    def test_set_spikes_indexes3(self):
        sim.setup(timestep=1)
        if_curr = sim.Population(5, sim.IF_curr_exp())
        recorder = if_curr._vertex._neuron_recorder
        if_curr.record("spikes")
        self.assertItemsEqual(
            ["spikes"], if_curr._get_all_recording_variables())
        self.assertItemsEqual([2, 4, 5], recorder._indexes["spikes"])

    # These test are currently directly on NeuronRecorder as no pynn way
    # to do this

    def test_turn_off_some_indexes(self):
        recorder = NeuronRecorder(["spikes", "v", "gsyn_exc", "gsyn_inh"], 5)
        recorder.set_recording("spikes", True)
        self.assertItemsEqual(
            ["spikes"], recorder.recording_variables)
        recorder.set_recording("spikes", False, indexes=[2, 4])
        self.assertItemsEqual([0, 1, 3], recorder._indexes["spikes"])
