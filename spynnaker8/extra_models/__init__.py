
# spynnaker 8 extra models
from spynnaker.pyNN.models.neuron.builds.if_cond_exp_stoc import IFCondExpStoc
from spynnaker.pyNN.models.neuron.builds.if_curr_delta import IFCurrDelta
from spynnaker.pyNN.models.neuron.builds.if_curr_exp_ca2_adaptive \
    import IFCurrExpCa2Adaptive
from spynnaker.pyNN.models.neuron.builds.if_curr_dual_exp_base \
    import IFCurrDualExpBase as IF_curr_dual_exp
from spynnaker.pyNN.models.neuron.builds.izk_cond_exp_base import \
    IzkCondExpBase as Izhikevich_cond
from spynnaker.pyNN.models.neuron.builds.if_curr_exp_semd_base import \
    IFCurrExpSEMDBase as IF_curr_exp_sEMD

# plastic timing spynnaker 8
from spynnaker8.models.synapse_dynamics.timing_dependence \
    import TimingDependenceRecurrent as RecurrentRule
from spynnaker8.models.synapse_dynamics.timing_dependence \
    import TimingDependenceSpikeNearestPair as SpikeNearestPairRule
from spynnaker8.models.synapse_dynamics.timing_dependence \
    import TimingDependenceVogels2011 as Vogels2011Rule
from spynnaker8.models.synapse_dynamics.timing_dependence \
    import TimingDependencePfisterSpikeTriplet as PfisterSpikeTriplet

# plastic weight spynnaker 8
from spynnaker8.models.synapse_dynamics.weight_dependence \
    import WeightDependenceAdditiveTriplet

__all__ = [
    # spynnaker 8 models
    'IFCurDelta', 'IFCurrExpCa2Adaptive', 'IFCondExpStoc',
    'Izhikevich_cond', 'IF_curr_dual_exp', 'IF_curr_exp_sEMD',

    # spynnaker 8 plastic stuff
    'WeightDependenceAdditiveTriplet',
    'PfisterSpikeTriplet',
    'SpikeNearestPairRule',
    'RecurrentRule', 'Vogels2011Rule']
