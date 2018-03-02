from spynnaker.pyNN.models.neuron.plasticity.stdp.weight_dependence \
    import WeightSTPOnly as CorrectWeightSTPOnly

class WeightSTPOnly(CorrectWeightSTPOnly):
    # noinspection PyPep8Naming
    def __init__(self, w_min=0.0, w_max=1.0):
        CorrectWeightSTPOnly.__init__(
            self, w_min=w_min, w_max=w_max)