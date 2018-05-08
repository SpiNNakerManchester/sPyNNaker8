from .weight_dependence_additive import WeightDependenceAdditive
from .weight_dependence_multiplicative import WeightDependenceMultiplicative
from .weight_dependence_cyclic import WeightDependenceCyclic
from .weight_dependence_additive_triplet import WeightDependenceAdditiveTriplet

__all__ = ["WeightDependenceAdditive", "WeightDependenceMultiplicative",
           "WeightDependenceAdditiveTriplet", "WeightDependenceCyclic"]
