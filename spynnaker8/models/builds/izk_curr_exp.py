from pyNN.standardmodels.cells import Izhikevich as PyNNIzhikevich

from spynnaker.pyNN.models.neuron.builds.izk_curr_exp_base import \
    IzkCurrExpBase
from spynnaker.pyNN.utilities import globals_variables


class IzkCurrExp(IzkCurrExpBase):

    # noinspection PyPep8Naming
    def __init__(
            self, size, spikes_per_second=None, ring_buffer_sigma=None,
            incoming_spike_buffer_size=None, constraints=None, label=None,
            a=PyNNIzhikevich.default_parameters['a'],
            b=PyNNIzhikevich.default_parameters['b'],
            c=PyNNIzhikevich.default_parameters['c'],
            d=PyNNIzhikevich.default_parameters['d'],
            i_offset=PyNNIzhikevich.default_parameters['i_offset'],
            u_init=IzkCurrExpBase.default_parameters['u_init'],
            v_init=IzkCurrExpBase.default_parameters['v_init'],
            tau_syn_E=IzkCurrExpBase.default_parameters['tau_syn_E'],
            tau_syn_I=IzkCurrExpBase.default_parameters['tau_syn_I']):
        IzkCurrExpBase.__init__(
            self, n_neurons=size, spikes_per_second=spikes_per_second,
            ring_buffer_sigma=ring_buffer_sigma, label=label, a=a, b=b, c=c,
            incoming_spike_buffer_size=incoming_spike_buffer_size, d=d,
            constraints=constraints, i_offset=i_offset, u_init=u_init,
            v_init=v_init, tau_syn_E=tau_syn_E, tau_syn_I=tau_syn_I,
            config=globals_variables.get_simulator().config)
