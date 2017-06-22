import unittest
import spynnaker8 as sim

class TestListStandardModules(unittest.TestCase):

    def test_check_list(self):
        results = sim.list_standard_models()
        self.assertIn('IF_cond_exp', results)
        self.assertIn('Izhikevich', results)
        self.assertIn('SpikeSourceArray', results)
        self.assertIn('SpikeSourcePoisson', results)
        self.assertNotIn('DataHolder', results)
