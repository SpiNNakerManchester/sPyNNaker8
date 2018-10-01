
# spynnaker 8 extra models
from spynnaker8.models.model_data_holders\
    import IfCondExpStocDataHolder as IFCondExpStock
from spynnaker8.models.model_data_holders\
    import IfCurrDeltaDataHolder as IFCurDelta
from spynnaker8.models.model_data_holders\
    import IfCurrExpCa2AdaptiveDataHolder as IFCurrExpCa2Adaptive
from spynnaker8.models.model_data_holders\
    import IFCurrDualExpDataHolder as IF_curr_dual_exp
from spynnaker8.models.model_data_holders.izk_cond_exp_data_holder import \
    IzkCondExpDataHolder as Izhikevich_cond
from spynnaker8.models.model_data_holders\
    import IFCurrCombExp2E2IDataHolder as IFCurrCombExp2E2I
from spynnaker8.models.model_data_holders\
    import IFCondExp2E2IDataHolder as IFCondExp2E2I

# plastic timing spynnaker 8
from spynnaker8.models.synapse_dynamics.timing_dependence \
    import TimingDependenceRecurrent as RecurrentRule
from spynnaker8.models.synapse_dynamics.timing_dependence \
    import TimingDependenceSpikeNearestPair as SpikeNearestPairRule
from spynnaker8.models.synapse_dynamics.timing_dependence \
    import TimingDependenceVogels2011 as Vogels2011Rule
from spynnaker8.models.synapse_dynamics.timing_dependence \
    import TimingDependencePfisterSpikeTriplet as PfisterSpikeTriplet
from spynnaker8.models.synapse_dynamics.timing_dependence \
    import TimingDependenceCyclic as TimingDependenceCyclic

# plastic weight spynnaker 8
from spynnaker8.models.synapse_dynamics.weight_dependence \
    import WeightDependenceAdditiveTriplet
from spynnaker8.models.synapse_dynamics.weight_dependence \
    import WeightDependenceCyclic

__all__ = [
    # spynnaker 8 models
    'IFCurDelta', 'IFCurrExpCa2Adaptive', 'IFCondExpStock',
    'Izhikevich_cond', 'IF_curr_dual_exp', "IFCurrCombExp2E2I",
    'IFCondExp2E2I',

    # spynnaker 8 plastic stuff
    'WeightDependenceAdditiveTriplet',
    'PfisterSpikeTriplet',
    'SpikeNearestPairRule',
    'RecurrentRule', 'Vogels2011Rule', 'TimingDependenceCyclic', 'WeightDependenceCyclic']
