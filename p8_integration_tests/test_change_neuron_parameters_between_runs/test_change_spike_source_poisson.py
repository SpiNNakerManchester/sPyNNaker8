import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase


def do_run():
    p.setup(1.0)

    inp = p.Population(
        100, p.SpikeSourcePoisson(rate=2), label="input",
        additional_parameters={"seed": 417})
    inp.record("spikes")

    p.run(100)

    p.reset()

    inp.set(rate=30)

    p.run(100)

    p.end()


class TestChangeParameter(BaseTestCase):

    def test_no_split(self):
        do_run()


if __name__ == '__main__':
    do_run()
