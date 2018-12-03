"""
retina example that just feeds data from a retina to live output via an
intermediate population
"""
import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase


def do_run():
    # Setup
    p.setup(timestep=1.0)

    p.Population(
        None,
        p.external_devices.ArbitraryFPGADevice(
            2000, fpga_link_id=12, fpga_id=1,
            board_address="127.0.0.1",
            label="bacon")
        )

    p.Population(
        None,
        p.external_devices.ArbitraryFPGADevice(
            2000, fpga_link_id=11, fpga_id=1,
            board_address="127.0.0.2",
            label="bacon")
        )

    p.run(1000)
    p.end()


class Sata2DifferentBoardsValidBoardAddress(BaseTestCase):

    def test_sata_2_different_boards_valid_board_address(self):
        do_run()


if __name__ == '__main__':
    do_run()
