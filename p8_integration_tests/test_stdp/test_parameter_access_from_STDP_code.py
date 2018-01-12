# This test will print logs to iobuf via the C code, therefore please uncomment
# lines in synapse_dynamics_stdp_mad_impl.c and verify output to iobuf
# output should be verified there.

import spynnaker8 as p
p.setup(1)
cell_params = {"v_thresh": [-50.1, -50.2, -50.3,
                            -50.4, -50.5, -50.6, -50.7, -50.8, -50.9, -51.0],
               "i_offset": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]}
pop_ex = p.Population(10, p.IF_curr_exp(**cell_params), label="test")

pop_src1 = p.Population(10,
                        p.SpikeSourceArray,
                        {'spike_times': [[1, 15],
                                         [2, 15],
                                         [3, 15],
                                         [4, 15],
                                         [5, 15],
                                         [6, 15],
                                         [7, 15],
                                         [8, 15],
                                         [9, 15],
                                         [10, 15]
                                         ]},
                        label="src1")

# Plastic Connections between pre_pop and post_pop
stdp_model = p.STDPMechanism(
    timing_dependence=p.SpikePairRule(
        tau_plus=20., tau_minus=20.0, A_plus=0.02, A_minus=0.02),
    weight_dependence=p.AdditiveWeightDependence(w_min=0, w_max=0.01))

plastic_projection = p.Projection(
    pop_src1, pop_ex, p.OneToOneConnector(),
    synapse_type=stdp_model, receptor_type='excitatory')


p.run(20)

p.end()
print "\n job done"
