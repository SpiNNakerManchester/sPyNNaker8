import spynnaker8 as sim
from spinnman.processes.get_machine_process import GetMachineProcess


def hacked_receive_chip_info(self, scp_read_chip_info_response):
    chip_info = scp_read_chip_info_response.chip_info
    self._chip_info[chip_info.x, chip_info.y] = chip_info
    # Hack to test ignores
    if (chip_info.x == 8 and chip_info.y == 4):
        self._ignore_cores.add((2, 2, -10, chip_info.ethernet_ip_address))
        self._ignore_cores.add((2, 2, -9, chip_info.ethernet_ip_address))


GetMachineProcess._receive_chip_info = hacked_receive_chip_info


sim.setup(timestep=1.0, n_boards_required=6)
machine = sim.get_machine()
sim.end()
