#!/usr/bin/python
"""
Synfirechain-like example
"""
import numpy
import os.path

import spynnaker.spike_checker as spike_checker
import spynnaker.plot_utils as plot_utils
from spynnaker8.utilities import neo_convertor
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import TestRun

n_neurons = 20  # number of neurons in each population
delay = 1
runtime = 100
neurons_per_core = None
placement_constraint = (0, 0)
expected_spikes = 33
current_file_path = os.path.dirname(os.path.abspath(__file__))
spike_file = os.path.join(current_file_path, "20_1_spikes.csv")
v_file = os.path.join(current_file_path, "20_1_v.csv")
gysn_file = os.path.join(current_file_path, "20_1_gsyn.csv")


class Synfire20n20pcDelaysDelayExtensionsAllRecording(BaseTestCase):
    def test_all_no_constarint(self):
        synfire_run = TestRun()
        synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                           delay=delay, run_times=[runtime], record=True,
                           record_7=True, record_v=True, record_v_7=True,
                           record_gsyn_exc=True, record_gsyn_exc_7=True,
                           record_gsyn_inh=False)
        gsyn_exc_7 = synfire_run.get_output_pop_gsyn_exc_7()
        v_7 = synfire_run.get_output_pop_voltage_7()
        spikes_7 = synfire_run.get_output_pop_spikes_7()

        gsyn_exc_neo = synfire_run.get_output_pop_gsyn_exc()
        v_neo = synfire_run.get_output_pop_voltage()
        spikes_neo = synfire_run.get_output_pop_spikes()

        gsyn_exc = neo_convertor.convert_data(gsyn_exc_neo, "gsyn_exc")
        v = neo_convertor.convert_data(v_neo, "v")
        spikes = neo_convertor.convert_spikes(spikes_neo)

        self.assertEquals(n_neurons * runtime, len(gsyn_exc))
        read_gsyn = numpy.loadtxt(gysn_file, delimiter=',')
        self.assertTrue(numpy.allclose(read_gsyn[:, 0:3], gsyn_exc_7))
        self.assertTrue(numpy.allclose(read_gsyn[:, 0:3], gsyn_exc))

        self.assertEquals(n_neurons * runtime, len(v))
        read_v = numpy.loadtxt(v_file, delimiter=',')
        self.assertTrue(numpy.allclose(read_v, v_7))
        self.assertTrue(numpy.allclose(read_v, v))

        self.assertEquals(expected_spikes, len(spikes))
        spike_checker.synfire_spike_checker(spikes, n_neurons)
        read_spikes = numpy.loadtxt(spike_file, delimiter=',')
        self.assertTrue(numpy.allclose(read_spikes, spikes_7))
        self.assertTrue(numpy.allclose(read_spikes, spikes))

    def test_all_constarint(self):
        synfire_run = TestRun()
        synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                           delay=delay, run_times=[runtime],
                           placement_constraint=placement_constraint,
                           record=True, record_7=True, record_v=True,
                           record_v_7=True, record_gsyn_exc=True,
                           record_gsyn_exc_7=True, record_gsyn_inh=False)
        gsyn_exc_7 = synfire_run.get_output_pop_gsyn_exc_7()
        v_7 = synfire_run.get_output_pop_voltage_7()
        spikes_7 = synfire_run.get_output_pop_spikes_7()

        gsyn_exc_neo = synfire_run.get_output_pop_gsyn_exc()
        v_neo = synfire_run.get_output_pop_voltage()
        spikes_neo = synfire_run.get_output_pop_spikes()

        gsyn_exc = neo_convertor.convert_data(gsyn_exc_neo, "gsyn_exc")
        v = neo_convertor.convert_data(v_neo, "v")
        spikes = neo_convertor.convert_spikes(spikes_neo)

        self.assertEquals(n_neurons * runtime, len(gsyn_exc))
        read_gsyn = numpy.loadtxt(gysn_file, delimiter=',')
        self.assertTrue(numpy.allclose(read_gsyn[:, 0:3], gsyn_exc_7))
        self.assertTrue(numpy.allclose(read_gsyn[:, 0:3], gsyn_exc))

        self.assertEquals(n_neurons * runtime, len(v))
        read_v = numpy.loadtxt(v_file, delimiter=',')
        self.assertTrue(numpy.allclose(read_v, v_7))
        self.assertTrue(numpy.allclose(read_v, v))

        self.assertEquals(expected_spikes, len(spikes))
        spike_checker.synfire_spike_checker(spikes, n_neurons)
        read_spikes = numpy.loadtxt(spike_file, delimiter=',')
        self.assertTrue(numpy.allclose(read_spikes, spikes_7))
        self.assertTrue(numpy.allclose(read_spikes, spikes))

    def test_spikes_no_constarint(self):
        synfire_run = TestRun()
        synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                           delay=delay, run_times=[runtime], record=True,
                           record_v=False, record_gsyn_exc_7=False,
                           record_gsyn_inh=False)
        spikes_neo = synfire_run.get_output_pop_spikes()
        spikes = neo_convertor.convert_spikes(spikes_neo)

        self.assertEquals(expected_spikes, len(spikes))
        spike_checker.synfire_spike_checker(spikes, n_neurons)
        read_spikes = numpy.loadtxt(spike_file, delimiter=',')
        self.assertTrue(numpy.allclose(read_spikes, spikes))

    def test_v_no_constarint(self):
        synfire_run = TestRun()
        synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                           delay=delay, run_times=[runtime], record=False,
                           record_v=True, record_gsyn_exc_7=False,
                           record_gsyn_inh=False)
        v_neo = synfire_run.get_output_pop_voltage()
        v = neo_convertor.convert_data(v_neo, "v")

        self.assertEquals(n_neurons * runtime, len(v))
        read_v = numpy.loadtxt(v_file, delimiter=',')
        self.assertTrue(numpy.allclose(read_v, v))

    def test_gsyn_no_constarint(self):
        synfire_run = TestRun()
        synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                           delay=delay, run_times=[runtime], record=False,
                           record_v=False, record_gsyn_exc_7=True,
                           record_gsyn_inh=False)
        gsyn_exc_neo = synfire_run.get_output_pop_gsyn_exc()
        gsyn_exc = neo_convertor.convert_data(gsyn_exc_neo, "gsyn_exc")

        self.assertEquals(n_neurons * runtime, len(gsyn_exc))
        read_gsyn = numpy.loadtxt(gysn_file, delimiter=',')
        self.assertTrue(numpy.allclose(read_gsyn[:, 0:3], gsyn_exc))


if __name__ == '__main__':
    synfire_run = TestRun()
    synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                       run_times=[runtime], record=True, record_v=True,
                       record_gsyn_exc_7=True, record_gsyn_inh=True)
    gsyn_exc_neo = synfire_run.get_output_pop_gsyn_exc()
    v_neo = synfire_run.get_output_pop_voltage()
    spikes_neo = synfire_run.get_output_pop_spikes()

    gsyn_exc = neo_convertor.convert_data(gsyn_exc_neo, "gsyn_exc")
    v = neo_convertor.convert_data(v_neo, "v")
    spikes = neo_convertor.convert_spikes(spikes_neo)

    print len(spikes)
    plot_utils.plot_spikes(spikes)
    numpy.savetxt(spike_file, spikes, delimiter=',')

    plot_utils.heat_plot(v)
    numpy.savetxt(v_file, v, delimiter=',')

    plot_utils.heat_plot(gsyn_exc)
    numpy.savetxt(gysn_file, gsyn_exc, delimiter=',')
