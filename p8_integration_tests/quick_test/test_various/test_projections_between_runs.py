import spynnaker8 as sim
from p8_integration_tests.base_test_case import BaseTestCase
# import neo_convertor


def do_run():
    sim.setup(timestep=1)
    pop_1 = sim.Population(1, sim.IF_curr_exp, {}, label="pop_1")
    inp = sim.Population(
        1, sim.SpikeSourceArray, {'spike_times': [[0]]}, label="input")
    sim.Projection(
        pop_1, pop_1, sim.OneToOneConnector(),
        synapse_type=sim.StaticSynapse(weight=5.0, delay=1),
        receptor_type="excitatory", source=None, space=None)

    pop_1.record("spikes")
    sim.run(20)
    first_spikes = pop_1.spinnaker_get_data("spikes")

    sim.Projection(
        inp, pop_1, sim.FromListConnector([[0, 0, 5, 5]]),
        synapse_type=sim.StaticSynapse(weight=5.0, delay=1),
        receptor_type="excitatory", source=None,
        space=None)

    sim.reset()
    sim.run(20)
    second_spikes = pop_1.spinnaker_get_data("spikes")

    return first_spikes, second_spikes


class TestProjectionBetweenRun(BaseTestCase):
    def do_run(self):
        first_spikes, second_spikes = do_run()
        assert len(first_spikes) == 0
        assert len(second_spikes[0]) == 2

    def test_run(self):
        self.runsafe(self.do_run)
