#!/usr/bin/python
from __future__ import print_function
"""
Synfirechain-like example
"""
import numpy
import os.path

import spynnaker.spike_checker as spike_checker
from spynnaker8.spynnaker_plotting import SpynnakerPanel
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import SynfireRunner
from pyNN.utility.plotting import Figure
import matplotlib.pyplot as plt

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
gysn_exc_file = os.path.join(current_file_path, "20_1_gsyn_exc.csv")


class Synfire20n20pcDelaysDelayExtensionsAllRecording(BaseTestCase):
    def test_all_no_constarint(self):
        synfire_run = SynfireRunner()
        synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                           delay=delay, run_times=[runtime], record=True,
                           record_7=True, record_v=True, record_v_7=True,
                           record_gsyn_exc=True, record_gsyn_exc_7=True,
                           record_gsyn_inh=False)
        gsyn_exc_7 = synfire_run.get_output_pop_gsyn_exc_7()
        v_7 = synfire_run.get_output_pop_voltage_7()
        spikes_7 = synfire_run.get_output_pop_spikes_7()

        gsyn_exc = synfire_run.get_output_pop_gsyn_exc_numpy()
        v = synfire_run.get_output_pop_voltage_numpy()
        spikes = synfire_run.get_output_pop_spikes_numpy()

        self.assertEquals(n_neurons * runtime, len(gsyn_exc))
        read_gsyn = numpy.loadtxt(gysn_file, delimiter=',')
        if not numpy.allclose(read_gsyn, gsyn_exc_7):
            for g1, g2 in zip(read_gsyn, gsyn_exc_7):
                if not numpy.allclose(g1, g2, rtol=1e-04):
                    print(g1, g2, g1[2]-g2[2], (g1[2]-g2[2])/g1[2])

        self.assertTrue(numpy.allclose(read_gsyn, gsyn_exc_7, rtol=1e-04),
                        "gsyn synakker method mismatch")
        self.assertTrue(numpy.allclose(read_gsyn, gsyn_exc, rtol=1e-04),
                        "gsyn neo method mismatch")

        self.assertEquals(n_neurons * runtime, len(v))
        read_v = numpy.loadtxt(v_file, delimiter=',')
        self.assertTrue(numpy.allclose(read_v, v_7, rtol=1e-03),
                        "v synakker method mismatch")
        self.assertTrue(numpy.allclose(read_v, v, rtol=1e-03),
                        "v neo method mismatch")

        self.assertEquals(expected_spikes, len(spikes))
        spike_checker.synfire_spike_checker(spikes, n_neurons)
        read_spikes = numpy.loadtxt(spike_file, delimiter=',')
        self.assertTrue(numpy.allclose(read_spikes, spikes_7),
                        "spikes synakker method mismatch")
        self.assertTrue(numpy.allclose(read_spikes, spikes),
                        "spikes neo method mismatch")

    def test_all_constarint(self):
        synfire_run = SynfireRunner()
        synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                           delay=delay, run_times=[runtime],
                           placement_constraint=placement_constraint,
                           record=True, record_7=True, record_v=True,
                           record_v_7=True, record_gsyn_exc=True,
                           record_gsyn_exc_7=True, record_gsyn_inh=False)

        gsyn_exc = synfire_run.get_output_pop_gsyn_exc_numpy()
        v = synfire_run.get_output_pop_voltage_numpy()
        spikes = synfire_run.get_output_pop_spikes_numpy()

        self.assertEquals(n_neurons * runtime, len(gsyn_exc))
        read_gsyn = numpy.loadtxt(gysn_file, delimiter=',')
        self.assertTrue(numpy.allclose(read_gsyn, gsyn_exc, rtol=1e-04),
                        "gsyn neo method mismatch")

        self.assertEquals(n_neurons * runtime, len(v))
        read_v = numpy.loadtxt(v_file, delimiter=',')
        self.assertTrue(numpy.allclose(read_v, v, rtol=1e-03),
                        "v neo method mismatch")

        self.assertEquals(expected_spikes, len(spikes))
        spike_checker.synfire_spike_checker(spikes, n_neurons)
        read_spikes = numpy.loadtxt(spike_file, delimiter=',')
        self.assertTrue(numpy.allclose(read_spikes, spikes),
                        "spikes neo method mismatch")


if __name__ == '__main__':
    synfire_run = SynfireRunner()
    synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                       delay=delay, run_times=[runtime],
                       placement_constraint=placement_constraint, record=True,
                       record_7=True, record_v=True, record_v_7=True,
                       record_gsyn_exc=True, record_gsyn_exc_7=True,
                       record_gsyn_inh=False)

    gsyn_exc = synfire_run.get_output_pop_gsyn_exc_numpy()
    gsyn_exc_neo = synfire_run.get_output_pop_gsyn_exc_neo()
    v = synfire_run.get_output_pop_voltage_numpy()
    v_neo = synfire_run.get_output_pop_voltage_neo()
    spikes = synfire_run.get_output_pop_spikes_numpy()
    spikes_neo = synfire_run.get_output_pop_spikes_neo()

    numpy.savetxt(spike_file, spikes, delimiter=',')
    numpy.savetxt(v_file, v, delimiter=',')
    numpy.savetxt(gysn_file, gsyn_exc, delimiter=',')

    Figure(SpynnakerPanel(spikes_neo, yticks=True, xticks=True, markersize=4,
                          xlim=(0, runtime)),
           SpynnakerPanel(v_neo, yticks=True, xticks=True),
           SpynnakerPanel(gsyn_exc_neo, yticks=True),
           title="Synfire with delay of {}".format(delay),
           annotations="generated by {}".format(__file__))
    plt.show()
