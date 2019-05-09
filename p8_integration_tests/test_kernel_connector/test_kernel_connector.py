import pylab
import numpy as np
import spynnaker8 as sim
from p8_integration_tests.base_test_case import BaseTestCase


def do_run(psh, psw, ksh, ksw, plot):
    sim.setup(timestep=1.0)

    # Note: this is working for square images and square odd-sided kernels

    # determine population size and runtime from the kernel sizes
#     psh = 4
#     psw = 4
    n_pop = psw*psh
    runtime = (n_pop*5)+1000

    spiking = [[n*5, (n_pop*5)-1-(n*5)] for n in range(n_pop)]
    print('ssa using ', spiking)

    input_pop = sim.Population(n_pop, sim.SpikeSourceArray(spiking), label="input")
    pop = sim.Population(n_pop // 4, sim.IF_curr_exp(), label="pop")

    weights = 5.0
    delays = 17.0

#     ksh = 3
#     ksw = 3
    pre_start = [0, 0]
    post_start = [0, 0]
    pre_step = [1, 1]
    post_step = [1, 1]

    shape_pre = [psh, psw]
    shape_post = [psh // 2, psw // 2]
    shape_kernel = [ksh, ksw]

    weight_list = [[7.0 if (a+b)%2==0 else 5.0 for a in range(ksw)] for b in range(ksh)]
    delay_list = [[20.0 if (a+b)%2==1 else 10.0 for a in range(ksw)] for b in range(ksh)]

    weight_kernel = np.asarray(weight_list)
    delay_kernel = np.asarray(delay_list)

    kernel_connector = sim.KernelConnector(shape_pre, shape_post, shape_kernel,
                                           weight_kernel=weight_kernel,
                                           delay_kernel=delay_kernel,
                                           pre_sample_steps=pre_step,
                                           post_sample_steps=post_step,
                                           pre_start_coords=pre_start,
                                           post_start_coords=post_start)
    print('kernel connector is: ', kernel_connector)
    c2 = sim.Projection(input_pop, pop, kernel_connector,
                        sim.StaticSynapse(weight=weights, delay=delays))

    pop.record(['v', 'spikes'])

    sim.run(runtime)

    weightsdelays = sorted(c2.get(['weight', 'delay'], 'list'),
                           key = lambda x: x[1])
    print(weightsdelays)
    print('there are', len(weightsdelays), 'connections')

    # Get data
    spikes = pop.spinnaker_get_data('spikes')
    v = pop.spinnaker_get_data('v')

    if plot:
        # Now plot some spikes
        pylab.figure()
        pylab.plot([i[1] for i in spikes],
                   [i[0] for i in spikes], "r.")
        pylab.xlabel('Time/ms')
        pylab.ylabel('spikes')
        pylab.title('spikes: kernel connector test')

        pylab.show()
#
#         pylab.figure()
#         pylab.plot([i[1] for i in spikes3],
#                    [i[0] for i in spikes3], "g.")
#         pylab.plot([i[1] for i in spikes4],
#                    [i[0] for i in spikes4], "r.")
#         pylab.plot([i[1] for i in spikes2],
#                    [i[0] for i in spikes2], "b.")
#         pylab.xlabel('Time/ms')
#         pylab.ylabel('spikes')
#         pylab.title('spikes: populations 2, 3, 4')
#
#         pylab.show()

    sim.end()

    return v, spikes, weightsdelays


class KernelConnectorTest(BaseTestCase):
    def test_run(self):
        psh = 4
        psw = 4
        ksh = 4
        ksw = 4
        v, spikes, weightsdelays = do_run(psh, psw, ksh, ksw, plot=False)
        # any checks go here
        self.assertEquals(25, len(weightsdelays))
        self.assertEquals(59, len(spikes))
        self.assertEquals(4320, len(v))


if __name__ == '__main__':
    psh = 4
    psw = 4
    ksh = 4
    ksw = 4
    v, spikes, weightsdelays = do_run(psh, psw, ksh, ksw, plot=True)
    print(len(v), len(spikes), len(weightsdelays))
