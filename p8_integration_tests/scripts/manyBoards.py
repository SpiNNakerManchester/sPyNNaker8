from __future__ import division
import spynnaker8 as sim
from p8_integration_tests.scripts.checker import check_data

CHIPS_PER_BOARD_EXCLUDING_SAFETY = 43.19


class ManyBoards(object):

    def add_pop(self, x, y, n_neurons, input):
        pop = sim.Population(
            n_neurons, sim.IF_curr_exp(), label="pop_{}_{}".format(x, y))
        pop.add_placement_constraint(x=x, y=y)
        sim.Projection(input, pop, sim.AllToAllConnector(),
                       synapse_type=sim.StaticSynapse(weight=5, delay=1))
        pop.record("all")
        return pop

    def setup(self, n_boards, n_neurons, simtime):
        n_chips_required = n_boards * CHIPS_PER_BOARD_EXCLUDING_SAFETY
        sim.setup(timestep=1.0, n_chips_required=n_chips_required)
        machine = sim.get_machine()
        input_spikes = list(range(0, simtime - 100, 10))
        self._expected_spikes = len(input_spikes)
        input = sim.Population(1, sim.SpikeSourceArray(spike_times=input_spikes),
                               label="input")
        self._pops = []
        for i, chip in enumerate(machine.ethernet_connected_chips):
            if i >= n_boards:
                break
            offset = machine.BOARD_48_CHIPS[i % 48]
            self._pops.append(self.add_pop(
                chip.x + offset[0], chip.y + offset[1], n_neurons, input))

    def do_run(self, n_boards, n_neurons, simtime):
        self._simtime = simtime
        self.setup(n_boards=n_boards, n_neurons=n_neurons, simtime=simtime)
        sim.run(simtime)
        return sim

    def check_all_data(self):
        for pop in self._pops:
            check_data(pop, self._expected_spikes, self._simtime)


if __name__ == '__main__':
    """
    main entrance method
    """
    me = ManyBoards()
    sim = me.do_run(n_boards=5, n_neurons=255, simtime=300)
    me.check_all_data()
    sim.end()
