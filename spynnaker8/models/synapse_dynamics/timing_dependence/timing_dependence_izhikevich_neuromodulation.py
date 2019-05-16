from spynnaker.pyNN.models.neuron.plasticity.stdp.timing_dependence.\
    timing_dependence_izhikevich_neuromodulation import \
    TimingDependenceIzhikevichNeuromodulation \
    as CommonTimingDependenaceIzhikevichNeuromodulation


class TimingDependenceIzhikevichNeuromodulation(
        CommonTimingDependenaceIzhikevichNeuromodulation):

    def __init__(self, tau_plus=20.0, tau_minus=20.0, tau_c=1000, tau_d=200):
        CommonTimingDependenaceIzhikevichNeuromodulation.__init__(
            self, tau_plus=tau_plus, tau_minus=tau_minus,
            tau_c=tau_c, tau_d=tau_d)
