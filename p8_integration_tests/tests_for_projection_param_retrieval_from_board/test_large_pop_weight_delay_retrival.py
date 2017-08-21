from p8_integration_tests.base_test_case import BaseTestCase
import spynnaker8 as p

sources = 1000  # number of neurons in each population
targets = 2000
weight_to_spike = 2.0
delay = 1


def do_run():
    p.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)

    cell_params_lif = {'cm': 0.25,  # nF
                       'i_offset': 0.0, 'tau_m': 20.0, 'tau_refrac': 2.0,
                       'tau_syn_E': 5.0, 'tau_syn_I': 5.0, 'v_reset': -70.0,
                       'v_rest': -65.0, 'v_thresh': -50.0}

    populations = list()
    projections = list()

    populations.append(
        p.Population(sources, p.IF_curr_exp, cell_params_lif, label='pop_1'))

    populations.append(
        p.Population(targets, p.IF_curr_exp, cell_params_lif, label='pop_2'))

    connectors = p.AllToAllConnector()
    synapse_type = p.StaticSynapse(weight=weight_to_spike, delay=delay)
    projections.append(p.Projection(populations[0], populations[1],
                                    connectors, synapse_type=synapse_type))

    # before
    pre_delays_array = projections[0].get(attribute_names=["delay"],
                                          format="nparray")
    pre_delays_list = projections[0].get(attribute_names=["delay"],
                                         format="list")
    pre_weights_array = projections[0].get(attribute_names=["weight"],
                                           format="array")
    pre_weights_list = projections[0].get(attribute_names=["weight"],
                                          format="list")

    p.run(100)

    # after
    post_delays_array = projections[0].get(attribute_names=["delay"],
                                           format="nparray")
    post_delays_list = projections[0].get(attribute_names=["delay"],
                                          format="list")
    post_weights_array = projections[0].get(attribute_names=["weight"],
                                            format="array")
    post_weights_list = projections[0].get(attribute_names=["weight"],
                                           format="list")

    p.end()

    return (pre_delays_array, pre_delays_list, pre_weights_array,
            pre_weights_list, post_delays_array, post_delays_list,
            post_weights_array, post_weights_list)


class LargePopWeightDelayRetrival(BaseTestCase):
    def test_compare_before_and_after(self):
        (pre_delays_array, pre_delays_list, pre_weights_array,
            pre_weights_list, post_delays_array, post_delays_list,
            post_weights_array, post_weights_list) = do_run()
        self.assertEqual(3, len(pre_delays_array))
        self.assertEqual((sources, targets), pre_delays_array[0].shape)
        self.assertEqual(0, pre_delays_array[0][0][0])
        self.assertEqual(sources-1, pre_delays_array[0][-1][-1])
        self.assertEqual((sources, targets), pre_delays_array[1].shape)
        self.assertEqual(0, pre_delays_array[1][0][0])
        self.assertEqual(targets-1, pre_delays_array[1][-1][-1])
        self.assertEqual((sources, targets), pre_delays_array[2].shape)
        self.assertEqual(delay, pre_delays_array[2][0][0])
        self.assertEqual(delay, pre_delays_array[2][-1][-1])

        self.assertEqual(sources * targets, len(pre_delays_list))
        self.assertEqual(3, len(pre_delays_list[0]))
        self.assertEqual(0, pre_delays_list[0][0])
        self.assertEqual(0, pre_delays_list[0][1])
        self.assertEqual(delay, pre_delays_list[0][2])
        self.assertEqual(sources - 1, pre_delays_list[-1][0])
        self.assertEqual(targets - 1, pre_delays_list[-1][1])
        self.assertEqual(delay, pre_delays_list[-1][2])

        self.assertEqual(3, len(pre_weights_array))
        self.assertEqual((sources, targets), pre_weights_array[0].shape)
        self.assertEqual(0, pre_weights_array[0][0][0])
        self.assertEqual(sources - 1, pre_weights_array[0][-1][-1])
        self.assertEqual((sources, targets), pre_weights_array[1].shape)
        self.assertEqual(0, pre_weights_array[1][0][0])
        self.assertEqual(targets - 1, pre_weights_array[1][-1][-1])
        self.assertEqual((sources, targets), pre_weights_array[2].shape)
        self.assertEqual(weight_to_spike, pre_weights_array[2][0][0])
        self.assertEqual(weight_to_spike, pre_weights_array[2][-1][-1])

        self.assertEqual(sources * targets, len(pre_weights_list))
        self.assertEqual(3, len(pre_weights_list[0]))
        self.assertEqual(0, pre_weights_list[0][0])
        self.assertEqual(0, pre_weights_list[0][1])
        self.assertEqual(weight_to_spike, pre_weights_list[0][2])
        self.assertEqual(sources-1, pre_weights_list[-1][0])
        self.assertEqual(targets-1, pre_weights_list[-1][1])
        self.assertEqual(weight_to_spike, pre_weights_list[-1][2])

        self.assertEqual(3, len(post_delays_array))
        self.assertEqual((sources, targets), post_delays_array[0].shape)
        self.assertEqual(0, post_delays_array[0][0][0])
        self.assertEqual(sources - 1, post_delays_array[0][-1][-1])
        self.assertEqual((sources, targets), post_delays_array[1].shape)
        self.assertEqual(0, post_delays_array[1][0][0])
        self.assertEqual(targets - 1, post_delays_array[1][-1][-1])
        self.assertEqual((sources, targets), post_delays_array[2].shape)
        self.assertEqual(delay, post_delays_array[2][0][0])
        self.assertEqual(delay, post_delays_array[2][-1][-1])

        self.assertEqual(sources * targets, len(post_delays_list))
        self.assertEqual(3, len(post_delays_list[0]))
        self.assertEqual(0, post_delays_list[0][0])
        self.assertEqual(0, post_delays_list[0][1])
        self.assertEqual(delay, post_delays_list[0][2])
        self.assertEqual(sources - 1, post_delays_list[-1][0])
        self.assertEqual(targets - 1, post_delays_list[-1][1])
        self.assertEqual(delay, post_delays_list[-1][2])

        self.assertEqual(3, len(post_weights_array))
        self.assertEqual((sources, targets), post_weights_array[0].shape)
        self.assertEqual(0, post_weights_array[0][0][0])
        self.assertEqual(sources - 1, post_weights_array[0][-1][-1])
        self.assertEqual((sources, targets), post_weights_array[1].shape)
        self.assertEqual(0, post_weights_array[1][0][0])
        self.assertEqual(targets - 1, post_weights_array[1][-1][-1])
        self.assertEqual((sources, targets), post_weights_array[2].shape)
        self.assertEqual(weight_to_spike, post_weights_array[2][0][0])
        self.assertEqual(weight_to_spike, post_weights_array[2][-1][-1])

        self.assertEqual(sources * targets, len(post_weights_list))
        self.assertEqual(3, len(post_weights_list[0]))
        self.assertEqual(0, post_weights_list[0][0])
        self.assertEqual(0, post_weights_list[0][1])
        self.assertEqual(weight_to_spike, post_weights_list[0][2])
        self.assertEqual(sources - 1, post_weights_list[-1][0])
        self.assertEqual(targets - 1, post_weights_list[-1][1])
        self.assertEqual(weight_to_spike, post_weights_list[-1][2])


if __name__ == '__main__':
    (pre_delays_array, pre_delays_list, pre_weights_array,
        pre_weights_list, post_delays_array, post_delays_list,
        post_weights_array, post_weights_list) = do_run()
    print "array"
    print pre_delays_array[0].shape
    print pre_delays_array[0].shape == (900, 900)
    print pre_delays_array[0]
    print pre_delays_array[1].shape
    print pre_delays_array[1]
    print pre_delays_array[2].shape
    print pre_delays_array[2]
    print "list"
    print pre_delays_list.shape
    print "array"
    print pre_weights_array[0].shape
    print pre_weights_array[1].shape
    print pre_weights_array[2].shape
    print "list"
    print pre_weights_list.shape
    print "array"
    print post_delays_array[0].shape
    print post_delays_array[1].shape
    print post_delays_array[2].shape
    print "list"
    print post_delays_list.shape
    print "array"
    print post_weights_array[0].shape
    print post_weights_array[1].shape
    print post_weights_array[2].shape
    print "list"
    print post_weights_list.shape
