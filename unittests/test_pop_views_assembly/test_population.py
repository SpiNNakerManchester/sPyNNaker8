from p8_integration_tests.base_test_case import BaseTestCase
import spynnaker8 as sim


class Test_Population(BaseTestCase):

        def test_properties(self):
            n_neurons = 5
            label = "pop_1"
            sim.setup(timestep=1.0)
            pop_1 = sim.Population(n_neurons, sim.IF_curr_exp(), label=label)
            self.assertEquals(n_neurons, pop_1.size)
            self.assertEquals(label, pop_1.label)
            self.assertEquals(sim.IF_curr_exp.build_model(), type(pop_1.celltype))
            v_init = -60
            pop_1.initialize(v=v_init)
            initial_values = pop_1.initial_values
            self.assertDictContainsSubset(dict({"v": v_init}), initial_values)
            v_init = [60 + index for index in xrange(n_neurons)]
            pop_1.initialize(v=v_init)
            initial_values = pop_1.initial_values
            self.assertDictContainsSubset(dict({"v": v_init}), initial_values)

            try:
                print pop_1.all_cells
            except NotImplementedError:
                pass

            try:
                print pop_1.local_cells
            except NotImplementedError:
                pass

            self.assertEquals(n_neurons, pop_1.local_size)

            try:
                print pop_1.position_generator
            except NotImplementedError:
                pass

            print pop_1.structure
