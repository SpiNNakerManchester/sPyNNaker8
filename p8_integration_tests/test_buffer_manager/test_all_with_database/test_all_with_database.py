"""
Synfirechain-like example
"""
import filecmp
import numpy
import os
import shutil
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import SynfireRunner
import spynnaker.plot_utils as plot_utils
import spynnaker.spike_checker as spike_checker

n_neurons = 200  # number of neurons in each population
runtime = 5000
neurons_per_core = n_neurons / 2
# If you change any of these delete the three *_all.csv files
# n_neurons = 1000  # number of neurons in each population
# runtime = 25000
# neurons_per_core = n_neurons / 10
synfire_run = SynfireRunner()
current_file_path = os.path.dirname(os.path.abspath(__file__))


class SynfireIfCurrExp(BaseTestCase):

    def test_run(self):
        synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                           run_times=[runtime])
        spikes = synfire_run.get_output_pop_spikes_numpy()
        spike_checker.synfire_spike_checker(spikes, n_neurons)
        self.assertEquals(1316, len(spikes))
        s_file = os.path.join(current_file_path, "s.csv")
        numpy.savetxt(s_file, spikes, delimiter=',')
        s_all = os.path.join(os.path.dirname(current_file_path), "s_all.csv")
        if (os.path.exists(s_all)):
            self.assertTrue(filecmp.cmp(s_file, s_all))
        else:
            shutil.copy(s_file, s_all)

        v = synfire_run.get_output_pop_voltage_numpy()
        v_file = os.path.join(current_file_path, "v.csv")
        numpy.savetxt(v_file, v, delimiter=',')
        v_all = os.path.join(os.path.dirname(current_file_path), "v_all.csv")
        if (os.path.exists(v_all)):
            self.assertTrue(filecmp.cmp(v_file, v_all))
        else:
            shutil.copy(v_file, v_all)

        gsyn = synfire_run.get_output_pop_gsyn_exc_numpy()
        gsyn_file = os.path.join(current_file_path, "gsyn.csv")
        numpy.savetxt(gsyn_file, gsyn, delimiter=',')
        gsyn_all = os.path.join(
            os.path.dirname(current_file_path), "gsyn_all.csv")
        if (os.path.exists(gsyn_all)):
            self.assertTrue(filecmp.cmp(gsyn_file, gsyn_all))
        else:
            shutil.copy(gsyn_file, gsyn_all)


if __name__ == '__main__':
    synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                       run_times=[runtime])
    gsyn = synfire_run.get_output_pop_gsyn_exc_numpy()
    v = synfire_run.get_output_pop_voltage_numpy()
    spikes = synfire_run.get_output_pop_spikes_numpy()

    plot_utils.plot_spikes(spikes)
    plot_utils.line_plot(v, title="v")
    plot_utils.heat_plot(gsyn, title="gsyn")
