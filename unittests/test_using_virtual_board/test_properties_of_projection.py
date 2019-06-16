import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase


class TestProps(BaseTestCase):

    def test_props(self):
        p.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)

        cell_params_lif = {'cm': 0.25,  # nF
                           'i_offset': 0.0, 'tau_m': 20.0, 'tau_refrac': 2.0,
                           'tau_syn_E': 5.0, 'tau_syn_I': 5.0,
                           'v_reset': -70.0,
                           'v_rest': -65.0, 'v_thresh': -50.0}

        source = p.Population(1, p.IF_curr_exp, cell_params_lif, label='pop_1')

        dest = p.Population(1, p.IF_curr_exp, cell_params_lif, label='pop_2')

        connector = p.AllToAllConnector()
        synapse_type = p.StaticSynapse(weight=0, delay=1)

        test_label = "BLAH!"

        proj = p.Projection(
            presynaptic_population=source,
            postsynaptic_population=dest,
            connector=connector, synapse_type=synapse_type, label="BLAH!")

        proj_label = proj.label
        proj_source = proj.pre
        proj_dest = proj.post
        self.assertEqual(source, proj_source)
        self.assertEqual(dest, proj_dest)
        self.assertEqual(test_label, proj_label)
