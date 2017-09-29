"""
retina example that just feeds data from a retina to live output via an
intermediate population
"""
import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase


def do_run():
    # Setup
    p.setup(timestep=1.0)

    # FPGA Retina - Down Polarity
    p.Population(2000, p.external_devices.ArbitraryFPGADevice,
                 {'fpga_link_id': 12, 'fpga_id': 1, 'label': "bacon"},
                 label='External sata thing')

    p.run(1000)
    p.end()


class Sata1PopTest(BaseTestCase):

    def test_sata_1pop(self):
        do_run()


if __name__ == "__main__":
    do_run()
