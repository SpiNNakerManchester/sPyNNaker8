from spynnaker.pyNN.models.neuron.plasticity.stdp.common \
    import plasticity_helpers
import math

# if we want a kernel peak at t=100ms
# sin_power=20
t_peak = 50
# time_constant = 1/(math.atan(sin_power)/t_peak)

plasticity_helpers.write_pfpc_lut(spec=None,
                                  peak_time=t_peak,
                                  lut_size=256,
                                  shift=0,
                                  time_probe=t_peak)



