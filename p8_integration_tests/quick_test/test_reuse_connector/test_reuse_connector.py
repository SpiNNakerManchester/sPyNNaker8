import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase


def do_run():

    p.setup(timestep=1.0)
    inp = p.Population(1, p.SpikeSourceArray(spike_times=[0]))
    out = p.Population(1, p.IF_curr_exp())

    connector = p.OneToOneConnector()

    proj_1 = p.Projection(inp, out, connector,
                          p.StaticSynapse(weight=2.0, delay=2.0))
    proj_2 = p.Projection(inp, out, connector,
                          p.StaticSynapse(weight=1.0, delay=1.0))

    p.run(1)

    proj_1_list = proj_1.get(("weight", "delay"), "list")
    proj_2_list = proj_2.get(("weight", "delay"), "list")
    print(proj_1_list)
    print(proj_2_list)
    p.end()

    return proj_1_list, proj_2_list


class ReuseConnectorTest(BaseTestCase):
    def test_run(self):
        proj_1_list, proj_2_list = do_run()
        # any checks go here
        test_1_list = []
        test_1_list.append((0, 0, 2.0, 2.0))
        test_2_list = []
        test_2_list.append((0, 0, 1.0, 1.0))
        self.assertEqual(len(proj_1_list), 1)
        self.assertEqual(len(proj_2_list), 1)
        for i in range(4):
            self.assertEquals(test_1_list[0][i], proj_1_list[0][i])
            self.assertEquals(test_2_list[0][i], proj_2_list[0][i])


if __name__ == '__main__':
    proj_1_list, proj_2_list = do_run()
