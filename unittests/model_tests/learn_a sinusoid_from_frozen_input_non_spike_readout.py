import spynnaker8 as p
import numpy
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

batches = 40
num_repeats = 5  # in a batch
cycle_time = 1023
timestep = 1
p.setup(timestep) # simulation timestep (ms)
runtime = num_repeats * cycle_time * batches


# # Post-synapse population
erbp_neuron_params = {
    "v_thresh": 30,
    "v_reset": 0,
    "v_rest": 0,
    "i_offset": 0, # DC input
    "v": 0,
    "tau_err": 1000
#     "tau_refrac": 50
    }

readout_neuron_params = {
    "v": 0,
    "v_thresh": 30, # controls firing rate of error neurons
    }

tau_err = 20

init_weight = 0.2

p.set_number_of_neurons_per_core(p.extra_models.IFCurrExpERBP, 32)
p.set_number_of_neurons_per_core(p.SpikeSourceArray, 32)


w_rec_out = init_weight
w_rec_out_dist = p.RandomDistribution(
        distribution='normal_clipped', mu=w_rec_out, sigma=w_rec_out,
        low=0.0, high=2*w_rec_out)

w_out_out = init_weight
w_out_out_dist = p.RandomDistribution(
        distribution='normal_clipped', mu=w_out_out, sigma=w_out_out,
        low=0.0, high=2*w_out_out)



def build_input_spike_train(num_repeats, cycle_time):
    pattern = [
            [158.0, 183.0, 184.0, 238.0, 315.0, 348.0, 388.0, 395.0, 403.0, 707.0, 925.0],
            [101.0, 304.0, 337.0, 398.0, 402.0, 740.0, 982.0, 984.0],
            [213.0, 662.0, 810.0, 904.0, 912.0, 1017.0, 1019.0],
            [12.0, 139.0, 236.0, 285.0, 398.0, 407.0, 578.0, 796.0, 888.0, 899.0, 902.0],
            [34.0, 37.0, 43.0, 79.0, 86.0, 116.0, 190.0, 235.0, 328.0, 346.0, 380.0, 464.0, 554.0, 595.0, 740.0, 852.0, 874.0, 929.0, 979.0, 995.0, 1009.0],
            [88.0, 108.0, 121.0, 196.0, 412.0, 445.0, 746.0, 778.0, 845.0, 1005.0],
            [96.0, 166.0, 351.0, 963.0, 980.0],
            [3.0, 114.0, 330.0, 424.0, 540.0, 594.0, 704.0, 710.0, 796.0, 832.0, 858.0, 905.0, 906.0],
            [204.0, 244.0, 442.0, 446.0, 626.0, 816.0, 838.0, 1012.0],
            [89.0, 529.0, 580.0, 626.0, 658.0, 681.0, 729.0, 924.0, 993.0],
            [487.0, 505.0, 705.0, 731.0, 799.0, 813.0, 1013.0],
            [317.0, 328.0, 674.0, 725.0, 730.0, 750.0, 779.0],
            [34.0, 40.0, 226.0, 312.0, 516.0, 743.0, 784.0, 829.0, 864.0, 898.0],
            [89.0, 97.0, 174.0, 218.0, 395.0, 465.0, 543.0, 611.0, 677.0, 762.0, 843.0],
            [49.0, 64.0, 142.0, 157.0, 169.0, 252.0, 379.0, 527.0, 544.0, 548.0, 576.0, 841.0, 935.0, 989.0],
            [11.0, 68.0, 291.0, 368.0, 507.0, 585.0, 604.0, 626.0, 643.0, 662.0, 781.0, 891.0, 902.0, 948.0, 1014.0, 1020.0],
            [4.0, 58.0, 227.0, 382.0, 404.0, 532.0, 586.0, 662.0, 728.0, 895.0, 953.0, 1002.0],
            [195.0, 215.0, 542.0, 600.0, 720.0, 740.0, 786.0, 791.0, 904.0, 935.0, 1015.0],
            [165.0, 200.0, 202.0, 289.0, 312.0, 338.0, 453.0, 459.0, 483.0, 638.0, 653.0, 748.0, 776.0, 856.0, 970.0],
            [13.0, 22.0, 38.0, 112.0, 154.0, 378.0, 439.0, 566.0, 609.0, 675.0, 814.0, 870.0, 924.0, 944.0, 952.0],
            [166.0, 300.0, 324.0, 329.0, 388.0, 444.0, 502.0],
            [10.0, 131.0, 326.0, 351.0, 408.0, 412.0, 446.0, 556.0, 562.0, 625.0, 773.0, 839.0, 900.0, 916.0, 927.0, 944.0, 945.0, 991.0],
            [30.0, 533.0, 561.0, 718.0, 738.0, 819.0, 930.0, 946.0],
            [106.0, 178.0, 199.0, 308.0, 324.0, 382.0, 426.0, 436.0, 497.0, 509.0, 755.0, 868.0, 893.0, 900.0],
            [33.0, 55.0, 95.0, 363.0, 371.0, 402.0, 403.0, 408.0, 627.0, 764.0, 890.0],
            [6.0, 141.0, 411.0, 414.0, 426.0, 521.0, 550.0, 765.0, 767.0, 840.0, 947.0, 1008.0, 1012.0, 1016.0],
            [387.0, 501.0, 776.0, 820.0, 853.0, 934.0, 940.0],
            [31.0, 39.0, 80.0, 133.0, 197.0, 282.0, 322.0, 500.0, 505.0, 557.0, 571.0, 637.0, 713.0, 728.0, 743.0, 767.0],
            [70.0, 84.0, 277.0, 289.0, 369.0, 575.0, 579.0, 665.0, 889.0],
            [95.0, 139.0, 234.0, 338.0, 365.0, 366.0, 472.0, 486.0, 499.0, 662.0, 918.0, 1003.0],
            [32.0, 185.0, 226.0, 311.0, 580.0, 725.0, 830.0, 1018.0],
            [313.0, 418.0, 450.0, 499.0, 790.0, 1021.0],
            [52.0, 66.0, 275.0, 306.0, 309.0, 474.0, 593.0, 668.0, 673.0, 741.0, 874.0, 1019.0],
            [69.0, 192.0, 285.0, 315.0, 379.0, 406.0, 545.0, 574.0, 579.0, 693.0, 815.0, 945.0],
            [12.0, 37.0, 165.0, 418.0, 646.0, 697.0, 799.0, 881.0, 963.0],
            [40.0, 102.0, 231.0, 375.0, 510.0, 631.0, 677.0, 702.0, 768.0, 860.0, 889.0],
            [38.0, 217.0, 260.0, 272.0, 338.0, 371.0, 457.0, 476.0, 576.0, 609.0, 787.0, 813.0, 880.0, 949.0, 951.0],
            [78.0, 243.0, 244.0, 247.0, 355.0, 357.0, 841.0, 915.0, 963.0],
            [310.0, 374.0, 397.0, 654.0, 699.0, 715.0, 863.0, 868.0, 980.0],
            [16.0, 80.0, 173.0, 194.0, 206.0, 212.0, 314.0, 374.0, 418.0, 476.0, 576.0, 591.0, 712.0, 787.0, 894.0],
            [52.0, 91.0, 214.0, 302.0, 311.0, 364.0, 431.0, 468.0, 791.0, 932.0],
            [38.0, 76.0, 118.0, 132.0, 187.0, 214.0, 283.0, 357.0, 503.0, 810.0, 852.0, 941.0, 994.0, 995.0, 997.0],
            [5.0, 142.0, 389.0, 473.0, 562.0, 571.0, 620.0, 679.0, 741.0, 923.0],
            [43.0, 58.0, 177.0, 372.0, 376.0, 415.0, 466.0, 628.0, 664.0, 790.0, 831.0, 948.0, 984.0],
            [55.0, 156.0, 197.0, 373.0, 375.0, 487.0, 545.0, 661.0, 662.0, 821.0],
            [97.0, 182.0, 428.0, 610.0, 812.0, 971.0],
            [80.0, 85.0, 86.0, 206.0, 210.0, 214.0, 473.0, 524.0, 538.0, 599.0, 687.0, 819.0, 938.0],
            [135.0, 213.0, 257.0, 273.0, 361.0, 429.0, 459.0, 643.0, 727.0, 954.0, 995.0],
            [91.0, 408.0, 550.0, 563.0, 908.0],
            [88.0, 134.0, 186.0, 347.0, 418.0, 442.0, 578.0, 592.0, 692.0, 711.0, 905.0, 910.0, 987.0],
            [9.0, 145.0, 259.0, 306.0, 308.0, 348.0, 407.0, 454.0, 534.0, 601.0, 695.0, 759.0, 805.0, 811.0, 823.0, 848.0],
            [233.0, 310.0, 450.0, 645.0, 654.0, 728.0, 747.0, 883.0, 982.0, 983.0],
            [256.0, 320.0, 569.0, 753.0, 849.0, 905.0, 943.0],
            [24.0, 285.0, 346.0, 440.0, 575.0, 627.0, 786.0, 951.0, 973.0],
            [65.0, 184.0, 444.0],
            [10.0, 53.0, 70.0, 197.0, 235.0, 261.0, 330.0, 460.0, 506.0, 675.0, 681.0, 748.0, 800.0, 846.0, 854.0, 898.0, 975.0, 976.0],
            [214.0, 258.0, 654.0, 815.0, 883.0, 1008.0],
            [15.0, 53.0, 142.0, 194.0, 225.0, 275.0, 287.0, 716.0, 909.0, 976.0, 987.0],
            [112.0, 436.0, 458.0, 556.0, 610.0, 662.0, 690.0, 778.0, 793.0, 823.0, 974.0],
            [100.0, 102.0, 239.0, 389.0, 440.0, 627.0, 777.0, 882.0, 908.0, 1000.0],
            [2.0, 30.0, 422.0, 445.0, 660.0, 706.0, 806.0, 895.0, 1015.0],
            [34.0, 182.0, 310.0, 503.0, 507.0, 539.0, 571.0, 580.0, 704.0, 889.0, 965.0],
            [26.0, 93.0, 185.0, 276.0, 294.0, 415.0, 786.0, 874.0, 877.0],
            [119.0, 130.0, 183.0, 271.0, 297.0, 380.0, 384.0, 452.0, 712.0, 836.0, 866.0, 984.0, 987.0, 1016.0],
            [65.0, 133.0, 252.0, 292.0, 315.0, 433.0, 642.0, 714.0, 737.0, 738.0, 769.0, 860.0],
            [36.0, 114.0, 248.0, 376.0, 393.0, 686.0, 755.0, 853.0, 981.0],
            [30.0, 33.0, 130.0, 304.0, 316.0, 364.0, 479.0, 690.0, 714.0, 747.0, 928.0, 1015.0],
            [72.0, 111.0, 275.0, 374.0, 391.0, 446.0, 450.0, 457.0, 656.0, 943.0],
            [29.0, 142.0, 201.0, 247.0, 366.0, 399.0, 488.0, 659.0, 716.0, 720.0, 922.0, 1013.0],
            [70.0, 103.0, 145.0, 197.0, 224.0, 236.0, 508.0, 637.0, 696.0, 746.0, 766.0, 869.0, 966.0],
            [15.0, 40.0, 107.0, 119.0, 169.0, 174.0, 403.0, 456.0, 571.0, 627.0, 666.0, 818.0, 916.0],
            [85.0, 112.0, 141.0, 307.0, 324.0, 333.0, 334.0, 570.0, 845.0, 942.0],
            [241.0, 271.0, 285.0, 717.0, 747.0, 757.0, 838.0, 1003.0],
            [61.0, 83.0, 92.0, 120.0, 174.0, 255.0, 259.0, 349.0, 429.0, 457.0, 465.0, 477.0, 530.0, 665.0, 683.0, 846.0, 861.0, 900.0],
            [82.0, 124.0, 534.0, 675.0, 897.0, 1015.0],
            [189.0, 428.0, 431.0, 579.0, 660.0, 671.0, 701.0, 726.0, 763.0, 870.0, 875.0, 961.0, 965.0, 1006.0],
            [75.0, 135.0, 236.0, 329.0, 356.0, 511.0, 596.0, 597.0, 663.0, 668.0, 671.0, 714.0, 786.0, 797.0],
            [152.0, 383.0, 582.0, 680.0, 848.0, 886.0, 898.0, 899.0],
            [12.0, 39.0, 318.0, 518.0, 583.0, 603.0, 614.0, 624.0, 680.0, 708.0, 738.0, 750.0, 766.0, 769.0, 852.0, 927.0],
            [113.0, 125.0, 296.0, 355.0, 416.0, 482.0, 683.0, 774.0, 960.0, 1022.0],
            [178.0, 210.0, 283.0, 318.0, 320.0, 329.0, 406.0, 419.0, 574.0, 606.0, 700.0, 841.0, 853.0, 866.0, 871.0, 957.0, 1017.0],
            [70.0, 249.0, 284.0, 304.0, 322.0, 371.0, 451.0, 605.0, 650.0, 658.0, 691.0, 778.0, 821.0, 932.0, 936.0, 942.0, 943.0],
            [8.0, 133.0, 257.0, 310.0, 398.0, 477.0, 630.0, 670.0, 722.0, 831.0, 916.0],
            [64.0, 271.0, 302.0, 341.0, 375.0, 400.0, 522.0, 624.0, 660.0],
            [28.0, 87.0, 209.0, 331.0, 414.0, 436.0, 454.0, 584.0, 628.0, 631.0, 667.0, 689.0, 935.0, 1007.0, 1014.0],
            [13.0, 33.0, 271.0, 390.0, 391.0, 471.0, 487.0, 737.0, 821.0, 883.0, 956.0],
            [3.0, 114.0, 240.0, 365.0, 376.0, 387.0, 525.0, 549.0, 716.0, 781.0, 873.0, 1001.0, 1011.0],
            [8.0, 74.0, 182.0, 279.0, 296.0, 401.0, 687.0, 699.0, 705.0, 945.0],
            [182.0, 436.0, 443.0, 447.0, 545.0, 771.0, 878.0, 932.0],
            [3.0, 12.0, 51.0, 90.0, 173.0, 193.0, 396.0, 515.0, 551.0, 601.0, 641.0, 943.0, 978.0],
            [119.0, 219.0, 332.0, 354.0, 421.0, 433.0, 447.0, 460.0, 595.0, 634.0],
            [138.0, 225.0, 333.0, 831.0, 854.0, 879.0, 916.0, 929.0, 951.0, 985.0],
            [14.0, 113.0, 229.0, 255.0, 274.0, 309.0, 460.0, 637.0, 889.0, 912.0, 941.0],
            [21.0, 69.0, 303.0, 356.0, 456.0, 581.0, 613.0, 617.0, 662.0, 700.0, 722.0, 870.0, 913.0, 1001.0],
            [18.0, 122.0, 132.0, 208.0, 366.0, 461.0, 580.0, 707.0, 714.0, 746.0, 799.0, 1010.0],
            [12.0, 59.0, 148.0, 149.0, 189.0, 270.0, 320.0, 481.0, 622.0, 695.0, 992.0],
            [31.0, 414.0, 460.0, 489.0, 499.0, 531.0, 543.0, 587.0, 593.0, 830.0, 844.0],
            [140.0, 324.0, 364.0, 582.0, 733.0, 886.0],
            [13.0, 86.0, 89.0, 130.0, 295.0, 340.0, 354.0, 522.0, 973.0, 986.0],
            [10.0, 75.0, 85.0, 89.0, 93.0, 202.0, 339.0, 469.0, 799.0, 865.0, 899.0, 967.0, 1001.0]
        ]

    spikes = []
    l=[]
    for i in range(len(pattern)):
        l = []
        for j in pattern[i]:
            l.append(j)
        spikes.append(l)

    for r in range(1, num_repeats):
        for p in range(len(pattern)):
            new_iter = [i + r * cycle_time for i in pattern[p]]
            spikes[p].extend(new_iter)

    return spikes


###############################################################################
# Build Populations
###############################################################################

# input population


pop_rec = p.Population(100,
                      p.SpikeSourceArray,
                      {'spike_times': build_input_spike_train(
                          num_repeats*batches, cycle_time)},
                      label='pop_in')


# Output population
pop_out = p.Population(3, # HARDCODED 3: One readout; one exc err, one inh err
                       p.extra_models.ReadoutPoissonNeuronNonSpike(
                            **readout_neuron_params
                           ),  # Neuron model
                       label="pop_out" # identifier
                       )

###############################################################################
# Build Projections
###############################################################################

# hidden_pop_timing_dependence=p.TimingDependenceERBP(
#         tau_plus=tau_err, A_plus=0.01, A_minus=0.01)
# hidden_pop_weight_dependence=p.WeightDependenceERBP(
#         w_min=0.0, w_max=1, reg_rate=0.1)

out_pop_timing_dependence=p.TimingDependenceERBP(
        tau_plus=tau_err, A_plus=0.05, A_minus=0.05, is_readout=True)
out_pop_weight_dependence=p.WeightDependenceERBP(
        w_min=0.0, w_max=3, reg_rate=0.0)

#######################################
# input to recurrent excitatory
#######################################

# # Define learning rule object
# learning_rule = p.STDPMechanism(
#     timing_dependence=hidden_pop_timing_dependence,
#     weight_dependence=hidden_pop_weight_dependence,
#     weight=w_in_rec_exc_dist,
#     delay=timestep)
#
# # Create excitatory projection from input to hidden neuron using learning rule
# inp_rec_exc = p.Projection(
#     pop_in,
#     pop_rec,
#     p.AllToAllConnector(),
# #     p.StaticSynapse(weight=w_in_rec_exc_dist, delay=timestep),
#     synapse_type=learning_rule,
#     receptor_type="excitatory")
#
# # input to recurrent inhibitory
# # Define learning rule object
# learning_rule = p.STDPMechanism(
#     timing_dependence=hidden_pop_timing_dependence,
#     weight_dependence=hidden_pop_weight_dependence,
#     weight=w_in_rec_inh_dist,
#     delay=timestep)
#
# # Create inhibitory projection from input to hidden neuron using learning rule
# inp_rec_inh = p.Projection(
#     pop_in,
#     pop_rec,
#     p.AllToAllConnector(),
# #     p.StaticSynapse(weight=w_in_rec_inh_dist, delay=timestep),
#     synapse_type=learning_rule,
#     receptor_type="inhibitory")
#
#
# #######################################
# # recurrent to recurrent
# #######################################
# # Define learning rule object
# learning_rule = p.STDPMechanism(
#     timing_dependence=hidden_pop_timing_dependence,
#     weight_dependence=hidden_pop_weight_dependence,
#     weight=w_rec_rec_dist,
#     delay=timestep)
#
# # Create excitatory recurrent projection
# rec_rec_exc = p.Projection(
#     pop_rec,
#     pop_rec,
#     p.FixedProbabilityConnector(1.0),
#     synapse_type=learning_rule,
#     receptor_type="excitatory")
#
# # input to recurrent inhibitory
# # Define learning rule object
# learning_rule = p.STDPMechanism(
#     timing_dependence=hidden_pop_timing_dependence,
#     weight_dependence=hidden_pop_weight_dependence,
#     weight=w_rec_rec_dist,
#     delay=timestep)
#
# # Create inhibitory recurrent projection from input to hidden neuron using
# # learning rule
# rec_rec_inh = p.Projection(
#     pop_rec,
#     pop_rec,
#     p.FixedProbabilityConnector(1.0),
#     synapse_type=learning_rule,
#     receptor_type="inhibitory")

#######################################
# recurrent to output
#######################################

# Only connect to neuron '0' of readout population
# rand_out_w.next(),
conn_list_exc = [[x, 0, w_rec_out_dist.next(), 1] for x in range(100)]
conn_list_inh = [[x, 0, w_rec_out_dist.next(), 1] for x in range(100)]

for i in range(0,100,2):
    conn_list_exc[i][2] = 0
    conn_list_inh[i+1][2] = 0


# Define learning rule object
learning_rule = p.STDPMechanism(
    timing_dependence=out_pop_timing_dependence,
    weight_dependence=out_pop_weight_dependence,
    weight=w_rec_out_dist,
    delay=timestep)

# Create excitatory recurrent to out projection
rec_out_exc = p.Projection(
    pop_rec,
    pop_out,
    p.FromListConnector(conn_list_exc),
#     synapse_type=p.StaticSynapse(weight=0.1, delay=1),
    synapse_type=learning_rule,
    receptor_type="excitatory")

# recurrent to out inhibitory
# Define learning rule object
learning_rule = p.STDPMechanism(
    timing_dependence=out_pop_timing_dependence,
    weight_dependence=out_pop_weight_dependence,
    weight=w_rec_out_dist,
    delay=timestep)

# Create inhibitory recurrent projection from recurrent to hidden neuron using
# learning rule
rec_out_inh = p.Projection(
    pop_rec,
    pop_out,
    p.FromListConnector(conn_list_inh),
#     p.StaticSynapse(weight=0.1, delay=1),
    synapse_type=learning_rule,
    receptor_type="inhibitory")

#######################################
# Feedback connections
#######################################

# # Connect excitatory fb neuron (1) to all recurrent neurons
# # rand_out_w.next()
# exc_fb_rec_conn_list = [[1, x, 0.01*w_rec_out_dist.next(), 1] for x in range(100)]
# # Connect inhibitory fb neuron (2) to all recurrent neurons
# # rand_out_w.next()
# inh_fb_rec_conn_list = [[2, x, 0.01*w_rec_out_dist.next(), 1] for x in range(100)]
#
# fb_out_rec_exc = p.Projection(
#     pop_out, pop_rec, p.FromListConnector(exc_fb_rec_conn_list),
#     p.StaticSynapse(weight=10, delay=1), receptor_type="exc_err")
#
# fb_out_rec_inh = p.Projection(
#     pop_out, pop_rec, p.FromListConnector(inh_fb_rec_conn_list),
#     p.StaticSynapse(weight=10, delay=1), receptor_type="inh_err")


# Now to output layer to gate plasticity on output weights
# rand_out_w.next()
# rand_out_w.next()
# exc_fb_out_conn_list  = [1, 0, w_out_out_dist.next(), 1]
# inh_fb_out_conn_list  = [2, 0, w_out_out_dist.next(), 1]
#
# fb_out_out_exc = p.Projection(
#     pop_out, pop_out, p.FromListConnector([exc_fb_out_conn_list]),
#     p.StaticSynapse(weight=0.5, delay=1), receptor_type="exc_err")
#
# fb_out_out_inh = p.Projection(
#     pop_out, pop_out, p.FromListConnector([inh_fb_out_conn_list]),
#     p.StaticSynapse(weight=0.5, delay=1), receptor_type="inh_err")

###############################################################################
# Run Simulation
###############################################################################

# pop_in.record('spikes')
pop_rec.record("spikes")
pop_out.record("all")


# p.run(runtime)
plot_start = 0
window =  num_repeats * cycle_time
plot_end = plot_start + window


for i in range(batches):

    print "run: {}".format(i)
    p.run(runtime/batches)

#     in_spikes = pop_in.get_data('spikes')
    pop_rec_data = pop_rec.get_data('spikes')
    pop_out_data = pop_out.get_data()

    # Plot
    F = Figure(
#         # plot data for postsynaptic neuron
#         Panel(in_spikes.segments[0].spiketrains,
#               yticks=True, markersize=2, xlim=(plot_start, plot_end)),
        Panel(pop_rec_data.segments[0].spiketrains,
              yticks=True, markersize=2, xlim=(plot_start, plot_end)
              ),
        Panel(pop_out_data.segments[0].filter(name='v')[0],
              ylabel="Membrane potential (mV)",
              data_labels=[pop_out.label], yticks=True, xlim=(plot_start, plot_end)
              ),
        Panel(pop_out_data.segments[0].filter(name='gsyn_exc')[0],
              ylabel="gsyn excitatory (mV)",
              data_labels=[pop_out.label], yticks=True, xlim=(plot_start, plot_end)
              ),
        Panel(pop_out_data.segments[0].filter(name='gsyn_inh')[0],
              ylabel="gsyn inhibitory (mV)",
              data_labels=[pop_out.label], yticks=True, xlim=(plot_start, plot_end)
              ),
        Panel(pop_out_data.segments[0].spiketrains,
              yticks=True, markersize=2, xlim=(plot_start, plot_end)),
        annotations="Batch: {}".format(i)
        )

    plt.pause(1)
#     plt.draw()

    plot_start = plot_end
    plot_end += window


p.end()


print "job done"

plt.show()