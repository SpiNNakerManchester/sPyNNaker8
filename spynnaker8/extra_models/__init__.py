
# spynnaker 8 extra models
from spynnaker8.models.model_data_holders\
    import IfCondExpStocDataHolder as IFCondExpStock
from spynnaker8.models.model_data_holders\
    import IfCurrDeltaDataHolder as IFCurDelta
from spynnaker8.models.model_data_holders\
    import IfCurrExpCa2AdaptiveDataHolder as IFCurrExpCa2Adaptive

# plastic timing spynnaker 8
from spynnaker8.models.synapse_dynamics.timing_dependence \
    import TimingDependenceRecurrent as RecurrentRule
from spynnaker8.models.synapse_dynamics.timing_dependence \
    import TimingDependenceSpikeNearestPair as SpikeNearestPair
from spynnaker8.models.synapse_dynamics.timing_dependence \
    import TimingDependenceVogels2011 as Vogels2011Rule
from spynnaker8.models.synapse_dynamics.timing_dependence \
    import TimingDependencePfisterSpikeTriplet as PfisterSpikeTriplet

# plastic weight spynnaker 8
from spynnaker8.models.synapse_dynamics.weight_dependence \
    import WeightDependenceAdditiveTriplet

import os

__all__ = [
    # spynnaker 8 models
    'IFCurDelta', 'IFCurrExpCa2Adaptive', 'IFCondExpStock',

    # spynnaker 8 plastic stuff
    'WeightDependenceAdditiveTriplet',
    'PfisterSpikeTriplet',
    'SpikeNearestPair',
    'RecurrentRule', 'Vogels2011Rule']
