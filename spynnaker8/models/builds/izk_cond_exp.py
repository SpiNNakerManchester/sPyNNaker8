from spynnaker.pyNN.models.neuron.builds.izk_cond_exp_base import \
    IzkCondExpBase
from spynnaker.pyNN.utilities import globals_variables


class IzkCondExp(IzkCondExpBase):

    # noinspection PyPep8Naming
    def __init__(
            self, size, spikes_per_second=None, ring_buffer_sigma=None,
            incoming_spike_buffer_size=None, constraints=None, label=None,
            a=IzkCondExpBase.default_parameters['a'],
            b=IzkCondExpBase.default_parameters['b'],
            c=IzkCondExpBase.default_parameters['c'],
            d=IzkCondExpBase.default_parameters['d'],
            i_offset=IzkCondExpBase.default_parameters['i_offset'],
            u_init=IzkCondExpBase.default_parameters['u_init'],
            v_init=IzkCondExpBase.default_parameters['v_init'],
            tau_syn_E=IzkCondExpBase.default_parameters['tau_syn_E'],
            tau_syn_I=IzkCondExpBase.default_parameters['tau_syn_I'],
            e_rev_E=IzkCondExpBase.default_parameters['e_rev_E'],
            e_rev_I=IzkCondExpBase.default_parameters['e_rev_I']):
        IzkCondExpBase.__init__(
            self, n_neurons=size, spikes_per_second=spikes_per_second,
            ring_buffer_sigma=ring_buffer_sigma, label=label, a=a, b=b, c=c,
            incoming_spike_buffer_size=incoming_spike_buffer_size, d=d,
            constraints=constraints, i_offset=i_offset, u_init=u_init,
            v_init=v_init, tau_syn_E=tau_syn_E, tau_syn_I=tau_syn_I,
            e_rev_I=e_rev_I, e_rev_E=e_rev_E,
            config=globals_variables.get_simulator().config)
