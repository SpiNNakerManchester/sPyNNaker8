
# spynnaker 8 extra models
from spynnaker.pyNN.models.neuron.builds import (
    IFCondExpStoc, IFCurrDelta as
    IFCurDelta, IFCurrExpCa2Adaptive, IFCurrDualExpBase as
    IF_curr_dual_exp, IzkCondExpBase as
    Izhikevich_cond, IFCurrExpSEMDBase as
    IF_curr_exp_sEMD)
from spynnaker.pyNN.models.neuron.builds.if_cond_exp_cerebellum import \
    IFCondExpCerebellum

# plastic timing spynnaker 8
from spynnaker8.models.synapse_dynamics.timing_dependence import (
    TimingDependenceRecurrent as
    RecurrentRule,
    TimingDependenceSpikeNearestPair as
    SpikeNearestPairRule,
    TimingDependenceVogels2011 as
    Vogels2011Rule,
    TimingDependencePfisterSpikeTriplet as
    PfisterSpikeTriplet)
# Cerebellum Plasticity
from spynnaker8.models.synapse_dynamics.timing_dependence\
    .timing_dependence_pfpc import TimingDependencePFPC as \
    TimingDependencePFPC
from spynnaker8.models.synapse_dynamics.weight_dependence import (
    WeightDependenceAdditiveTriplet)
from spynnaker8.models.synapse_dynamics.timing_dependence\
    .timing_dependence_mfvn import TimingDependenceMFVN as \
    TimingDependenceMFVN
from spynnaker8.models.synapse_dynamics.weight_dependence\
    .weight_dependence_mfvn import \
    WeightDependenceMFVN as WeightDependenceMFVN

# plastic weight spynnaker 8
from spynnaker8.models.synapse_dynamics.weight_dependence \
    import WeightDependenceAdditiveTriplet

__all__ = [
    # sPyNNaker 8 models
    'IFCurDelta', 'IFCurrExpCa2Adaptive', 'IFCondExpStoc',
    'Izhikevich_cond', 'IF_curr_dual_exp', 'IF_curr_exp_sEMD',
    "IFCondExpCerebellum",

    # sPyNNaker 8 plastic stuff
    'WeightDependenceAdditiveTriplet',
    'PfisterSpikeTriplet',
    'SpikeNearestPairRule',
    'RecurrentRule', 'Vogels2011Rule',
    "TimingDependencePFPC", "WeightDependencePFPC",
    'TimingDependenceMFVN', 'WeightDependenceMFVN'
    ]
