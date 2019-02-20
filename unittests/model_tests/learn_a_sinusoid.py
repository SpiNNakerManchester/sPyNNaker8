import spynnaker8 as p
import numpy
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

num_repeats = 50
cycle_time = 1023
timestep = 1
p.setup(timestep) # simulation timestep (ms)
runtime = num_repeats * cycle_time

# # Post-synapse population
erbp_neuron_params = {
    "v_thresh": 100,
    "v_reset": 0,
    "v_rest": 0,
    "i_offset": 0.5, # DC input
    "v": 0,
    "tau_err": 20
    }

readout_neuron_params = {
    "v": 0
    }

w_in_rec_exc = 1.5
w_in_rec_exc_dist = p.RandomDistribution(
        distribution='normal_clipped', mu=w_in_rec_exc, sigma=w_in_rec_exc,
        low=0.0, high=2*w_in_rec_exc)


w_in_rec_inh = 0.25*w_in_rec_exc
w_in_rec_inh_dist = p.RandomDistribution(
        distribution='normal_clipped', mu=w_in_rec_inh, sigma=w_in_rec_inh,
        low=0.0, high=2*w_in_rec_inh)


w_rec_rec = 0.75
w_rec_rec_dist = p.RandomDistribution(
        distribution='normal_clipped', mu=w_rec_rec, sigma=w_rec_rec,
        low=0.0, high=2*w_rec_rec)

w_rec_out = 0.75
w_rec_out_dist = p.RandomDistribution(
        distribution='normal_clipped', mu=w_rec_out, sigma=w_rec_out,
        low=0.0, high=2*w_rec_out)

w_out_out = 0.5
w_out_out_dist = p.RandomDistribution(
        distribution='normal_clipped', mu=w_out_out, sigma=w_out_out,
        low=0.0, high=2*w_out_out)

tau_err = 20

def build_input_spike_train(num_repeats, cycle_time):
    pattern = [
        [149.0, 194.0, 324.0, 516.0, 521.0, 574.0, 593.0, 618.0, 640.0, 707.0, 918.0, 943.0],
		[451.0, 534.0, 695.0, 1001.0],
		[49.0, 266.0, 431.0, 484.0, 573.0, 669.0, 750.0, 906.0, 992.0, 1022.0],
		[11.0, 414.0, 524.0, 549.0, 722.0, 806.0],
		[108.0, 118.0, 122.0, 351.0, 509.0, 516.0, 595.0, 604.0, 647.0, 669.0, 674.0, 818.0],
		[79.0, 95.0, 99.0, 170.0, 171.0, 276.0, 349.0, 368.0, 386.0, 408.0, 439.0, 454.0, 934.0, 1007.0],
		[88.0, 108.0, 121.0, 166.0, 287.0, 375.0, 379.0, 566.0, 752.0, 834.0, 913.0],
		[146.0, 385.0, 526.0, 536.0, 565.0, 587.0, 659.0, 722.0, 810.0],
		[11.0, 19.0, 111.0, 284.0, 287.0, 344.0, 374.0, 409.0, 476.0, 525.0, 593.0, 613.0, 659.0, 799.0, 835.0, 871.0, 993.0],
		[73.0, 111.0, 151.0, 295.0, 373.0, 381.0, 499.0, 542.0, 548.0, 571.0, 805.0, 815.0, 863.0, 898.0],
		[11.0, 149.0, 276.0, 402.0, 448.0, 636.0, 801.0, 900.0, 932.0, 1020.0],
		[70.0, 79.0, 111.0, 260.0, 296.0, 669.0, 760.0],
		[30.0, 146.0, 223.0, 359.0, 513.0, 601.0, 649.0, 757.0, 827.0, 832.0],
		[32.0, 66.0, 317.0, 319.0, 335.0, 498.0, 638.0, 756.0, 764.0, 837.0, 936.0],
		[102.0, 163.0, 397.0, 412.0, 416.0, 510.0, 596.0, 639.0, 710.0, 739.0, 745.0, 850.0, 871.0, 984.0, 1008.0],
		[56.0, 312.0, 355.0, 401.0, 480.0, 564.0, 665.0, 736.0],
		[226.0, 263.0, 361.0, 519.0, 579.0, 589.0, 598.0, 615.0, 619.0, 697.0, 854.0, 887.0, 1004.0],
		[30.0, 163.0, 229.0, 268.0, 269.0, 299.0, 355.0, 393.0, 537.0, 540.0, 569.0, 583.0, 602.0, 608.0, 733.0, 790.0],
		[263.0, 302.0, 372.0, 682.0, 727.0, 782.0, 815.0, 853.0, 889.0],
		[65.0, 481.0, 562.0, 637.0, 762.0, 968.0, 978.0],
		[85.0, 215.0, 273.0, 366.0, 414.0, 417.0, 522.0, 712.0, 754.0, 806.0, 814.0, 953.0, 997.0],
		[19.0, 60.0, 98.0, 165.0, 223.0, 246.0, 273.0, 292.0, 304.0, 326.0, 364.0, 374.0, 514.0, 641.0, 720.0, 875.0],
		[174.0, 199.0, 366.0, 592.0, 636.0, 729.0, 789.0, 800.0, 1012.0],
		[72.0, 129.0, 191.0, 402.0, 497.0, 533.0, 546.0, 582.0, 599.0, 704.0, 780.0, 834.0, 943.0],
		[36.0, 97.0, 182.0, 202.0, 269.0, 283.0, 526.0, 592.0, 634.0, 767.0],
		[41.0, 48.0, 49.0, 360.0, 418.0, 536.0, 583.0, 776.0, 824.0, 880.0],
		[114.0, 378.0, 395.0, 611.0, 757.0, 854.0],
		[17.0, 171.0, 427.0, 543.0, 600.0, 621.0, 622.0, 663.0, 696.0, 735.0, 807.0, 842.0, 971.0],
		[10.0, 39.0, 311.0, 338.0, 781.0, 805.0, 933.0, 1000.0],
		[67.0, 117.0, 121.0, 233.0, 347.0, 523.0, 678.0, 947.0, 976.0],
		[116.0, 243.0, 325.0, 421.0, 434.0, 438.0, 520.0, 645.0, 680.0, 713.0, 753.0, 786.0, 855.0, 995.0],
		[70.0, 86.0, 102.0, 146.0, 355.0, 371.0, 377.0, 392.0, 555.0, 567.0, 749.0, 934.0, 954.0],
		[216.0, 326.0, 331.0, 494.0, 544.0, 547.0, 571.0, 650.0, 654.0, 669.0, 757.0, 790.0, 905.0, 929.0, 1023.0],
		[305.0, 326.0, 642.0, 658.0, 778.0, 808.0, 841.0, 895.0, 917.0],
		[103.0, 319.0, 346.0, 435.0, 525.0, 605.0, 612.0, 648.0, 818.0, 836.0, 856.0],
		[47.0, 158.0, 267.0, 315.0, 326.0, 518.0, 655.0, 710.0, 745.0, 836.0, 856.0, 901.0, 991.0],
		[170.0, 180.0, 263.0, 298.0, 607.0, 855.0],
		[55.0, 445.0, 476.0, 670.0, 774.0, 848.0, 854.0],
		[28.0, 278.0, 310.0, 324.0, 356.0, 873.0, 979.0, 1001.0],
		[99.0, 135.0, 231.0, 306.0, 316.0, 327.0, 341.0, 557.0, 761.0, 762.0, 788.0, 824.0],
		[55.0, 187.0, 206.0, 322.0, 328.0, 347.0, 350.0, 457.0, 725.0, 821.0, 915.0],
		[2.0, 22.0, 35.0, 160.0, 210.0, 336.0, 430.0, 466.0, 561.0, 586.0, 588.0, 792.0, 998.0, 1012.0],
		[124.0, 229.0, 285.0, 359.0, 379.0, 427.0, 443.0, 515.0, 687.0, 813.0, 821.0, 968.0, 995.0],
		[337.0, 386.0, 536.0, 546.0, 1001.0],
		[52.0, 77.0, 190.0, 219.0, 316.0, 327.0, 384.0, 531.0, 562.0, 1005.0],
		[95.0, 184.0, 239.0, 300.0, 610.0, 812.0, 1023.0],
		[72.0, 102.0, 184.0, 404.0, 407.0, 416.0, 555.0, 768.0, 792.0, 849.0],
		[184.0, 206.0, 217.0, 235.0, 288.0, 363.0, 382.0, 523.0, 539.0, 589.0, 643.0, 782.0, 993.0, 1008.0],
		[31.0, 61.0, 162.0, 198.0, 304.0, 350.0, 420.0, 562.0, 574.0, 603.0, 620.0, 688.0, 717.0, 787.0, 934.0],
		[20.0, 101.0, 124.0, 136.0, 370.0, 439.0, 576.0, 712.0, 779.0, 930.0],
		[11.0, 23.0, 120.0, 402.0, 585.0, 888.0, 963.0, 980.0],
		[79.0, 107.0, 164.0, 221.0, 252.0, 485.0, 488.0, 662.0, 692.0, 765.0, 818.0, 937.0, 1019.0],
		[16.0, 97.0, 110.0, 243.0, 343.0, 402.0, 512.0, 659.0, 737.0, 810.0, 818.0, 939.0, 961.0, 985.0],
		[37.0, 198.0, 228.0, 385.0, 389.0, 535.0, 619.0, 693.0, 729.0, 814.0, 885.0, 940.0],
		[72.0, 202.0, 213.0, 238.0, 368.0, 447.0, 567.0, 646.0, 648.0, 667.0, 700.0, 920.0],
		[31.0, 38.0, 43.0, 107.0, 142.0, 435.0, 439.0, 580.0, 748.0, 1005.0],
		[86.0, 275.0, 282.0, 376.0, 492.0, 619.0, 690.0, 821.0, 982.0],
		[51.0, 135.0, 148.0, 149.0, 231.0, 246.0, 417.0, 618.0, 619.0, 623.0, 648.0, 918.0],
		[244.0, 302.0, 308.0, 396.0, 447.0, 523.0, 610.0, 689.0, 730.0, 817.0, 958.0],
		[131.0, 396.0, 453.0, 570.0, 573.0, 695.0, 736.0, 815.0, 851.0, 1011.0],
		[26.0, 169.0, 243.0, 352.0, 461.0, 763.0, 809.0, 810.0, 956.0, 971.0, 1018.0],
		[208.0, 220.0, 243.0, 300.0, 412.0, 455.0, 489.0, 803.0, 956.0],
		[115.0, 269.0, 299.0, 420.0, 650.0, 664.0, 665.0, 811.0, 902.0, 910.0],
		[346.0, 496.0, 693.0, 783.0, 801.0, 860.0, 973.0],
		[128.0, 142.0, 294.0, 318.0, 466.0, 477.0, 493.0, 509.0, 554.0, 617.0, 630.0, 663.0, 671.0, 681.0, 754.0, 842.0],
		[43.0, 56.0, 85.0, 107.0, 118.0, 149.0, 282.0, 334.0, 379.0, 535.0, 677.0, 977.0],
		[41.0, 331.0, 378.0, 440.0, 494.0, 706.0, 770.0, 883.0, 903.0, 980.0, 1003.0],
		[67.0, 150.0, 233.0, 237.0, 388.0, 448.0, 468.0, 528.0, 903.0],
		[378.0, 443.0, 446.0, 571.0, 646.0, 851.0, 892.0, 972.0],
		[50.0, 213.0, 261.0, 281.0, 390.0, 406.0, 422.0, 493.0, 640.0, 707.0, 750.0, 945.0, 1013.0],
		[54.0, 180.0, 367.0, 386.0, 479.0, 727.0, 892.0],
		[37.0, 176.0, 396.0, 402.0, 527.0, 560.0, 634.0, 685.0],
		[94.0, 500.0, 613.0, 682.0, 711.0, 752.0, 758.0, 1016.0],
		[2.0, 51.0, 170.0, 255.0, 319.0, 341.0, 369.0, 443.0, 542.0, 682.0, 717.0],
		[31.0, 333.0, 357.0, 405.0, 489.0, 634.0, 751.0, 916.0, 972.0],
		[402.0, 466.0, 478.0, 779.0, 826.0],
		[35.0, 71.0, 87.0, 157.0, 186.0, 304.0, 337.0, 466.0, 601.0, 627.0, 805.0, 855.0],
		[189.0, 233.0, 425.0, 601.0, 602.0, 857.0],
		[137.0, 358.0, 372.0, 642.0, 647.0, 755.0, 887.0, 986.0],
		[216.0, 263.0, 388.0, 419.0, 607.0, 651.0, 919.0, 934.0, 953.0, 1002.0],
		[20.0, 186.0, 386.0, 561.0, 598.0, 723.0, 953.0],
		[73.0, 108.0, 167.0, 221.0, 359.0, 409.0, 417.0, 790.0, 852.0, 864.0, 934.0],
		[29.0, 201.0, 216.0, 296.0, 339.0, 710.0, 880.0, 891.0, 931.0, 956.0],
		[161.0, 162.0, 208.0, 240.0, 340.0, 386.0, 474.0, 747.0, 899.0],
		[106.0, 238.0, 307.0, 525.0, 695.0, 859.0, 860.0],
		[404.0, 435.0, 497.0, 573.0, 725.0],
		[162.0, 325.0, 448.0, 613.0, 779.0, 924.0, 925.0],
		[191.0, 248.0, 488.0, 498.0, 836.0, 869.0, 899.0],
		[57.0, 137.0, 162.0, 527.0, 531.0, 563.0, 809.0, 838.0, 902.0, 977.0],
		[34.0, 60.0, 240.0, 452.0, 492.0, 498.0, 562.0, 800.0, 888.0, 928.0],
		[8.0, 205.0, 346.0, 364.0, 476.0, 524.0, 607.0, 665.0, 762.0, 845.0, 926.0],
		[107.0, 169.0, 394.0, 549.0, 561.0, 583.0, 707.0, 708.0],
		[182.0, 190.0, 230.0, 274.0, 360.0, 466.0, 538.0, 622.0, 839.0, 851.0],
		[47.0, 62.0, 65.0, 222.0, 413.0, 545.0, 558.0, 615.0, 951.0],
		[22.0, 272.0, 322.0, 372.0, 486.0, 707.0, 850.0, 958.0],
		[49.0, 198.0, 439.0, 588.0, 605.0, 708.0, 752.0, 765.0, 887.0, 953.0],
		[204.0, 253.0, 265.0, 295.0, 348.0, 491.0, 574.0, 749.0, 864.0, 958.0],
		[104.0, 159.0, 186.0, 198.0, 273.0, 332.0, 372.0, 399.0, 429.0, 472.0, 582.0, 595.0, 621.0, 772.0, 821.0, 904.0],
		[47.0, 106.0, 184.0, 267.0, 415.0, 597.0, 630.0, 653.0, 877.0, 917.0],
		[1.0, 36.0, 164.0, 187.0, 286.0, 314.0, 418.0, 433.0, 512.0, 546.0, 615.0, 881.0, 917.0, 959.0, 984.0]
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


pop_in = p.Population(100,
                      p.SpikeSourceArray,
                      {'spike_times': build_input_spike_train(num_repeats, cycle_time)},
                      label='pop_in')

pop_rec = p.Population(100,  # number of neurons
                       p.extra_models.IFCurrExpERBP(**erbp_neuron_params),
                       label="pop_rec")

# Output population
pop_out = p.Population(3, # HARDCODE TO 3: One readout; one exc err, one inh err
                       p.extra_models.ReadoutPoissonNeuron(
                            **readout_neuron_params
                           ),  # Neuron model
                       label="pop_out" # identifier
                       )

###############################################################################
# Build Projections
###############################################################################

#######################################
# input to recurrent excitatory
#######################################

# Define learning rule object
learning_rule = p.STDPMechanism(
    timing_dependence=p.TimingDependenceERBP(
        tau_plus=tau_err, A_plus=1, A_minus=1),
    weight_dependence=p.WeightDependenceERBP(
        w_min=0.0, w_max=2),
    weight=w_in_rec_exc_dist,
    delay=timestep)

# Create excitatory projection from input to hidden neuron using learning rule
inp_rec_exc = p.Projection(
    pop_in,
    pop_rec,
    p.AllToAllConnector(),
    p.StaticSynapse(weight=w_in_rec_exc_dist, delay=timestep),
#     synapse_type=learning_rule,
    receptor_type="excitatory")

# input to recurrent inhibitory
# Define learning rule object
learning_rule = p.STDPMechanism(
    timing_dependence=p.TimingDependenceERBP(
        tau_plus=tau_err, A_plus=1, A_minus=1),
    weight_dependence=p.WeightDependenceERBP(
        w_min=0.0, w_max=2),
    weight=w_in_rec_inh_dist,
    delay=timestep)

# Create inhibitory projection from input to hidden neuron using learning rule
inp_rec_inh = p.Projection(
    pop_in,
    pop_rec,
    p.AllToAllConnector(),
    p.StaticSynapse(weight=w_in_rec_inh_dist, delay=timestep),
#     synapse_type=learning_rule,
    receptor_type="inhibitory")


#######################################
# recurrent to recurrent
#######################################
# Define learning rule object
learning_rule = p.STDPMechanism(
    timing_dependence=p.TimingDependenceERBP(
        tau_plus=tau_err, A_plus=1, A_minus=1),
    weight_dependence=p.WeightDependenceERBP(
        w_min=0.0, w_max=2),
    weight=w_rec_rec_dist,
    delay=timestep)

# Create excitatory recurrent projection
rec_rec_exc = p.Projection(
    pop_rec,
    pop_rec,
    p.AllToAllConnector(),
    synapse_type=learning_rule,
    receptor_type="excitatory")

# input to recurrent inhibitory
# Define learning rule object
learning_rule = p.STDPMechanism(
    timing_dependence=p.TimingDependenceERBP(
        tau_plus=tau_err, A_plus=1, A_minus=1),
    weight_dependence=p.WeightDependenceERBP(
        w_min=0.0, w_max=2),
    weight=w_rec_rec_dist,
    delay=timestep)

# Create inhibitory recurrent projection from input to hidden neuron using learning rule
rec_rec_inh = p.Projection(
    pop_rec,
    pop_rec,
    p.AllToAllConnector(),
    synapse_type=learning_rule,
    receptor_type="inhibitory")

#######################################
# recurrent to output
#######################################

# Only connect to neuron '0' of readout population
# rand_out_w.next(),
conn_list_exc = [[x, 0, w_rec_out_dist.next(), 1] for x in range(100)]
conn_list_inh = [[x, 0, w_rec_out_dist.next(), 1] for x in range(100)]


# Define learning rule object
learning_rule = p.STDPMechanism(
    timing_dependence=p.TimingDependenceERBP(
        tau_plus=tau_err, A_plus=1, A_minus=1),
    weight_dependence=p.WeightDependenceERBP(
        w_min=0.0, w_max=2),
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
    timing_dependence=p.TimingDependenceERBP(
        tau_plus=tau_err, A_plus=1, A_minus=1),
    weight_dependence=p.WeightDependenceERBP(
        w_min=0.0, w_max=2),
    weight=w_rec_out_dist,
    delay=timestep)

# Create inhibitory recurrent projection from recurrent to hidden neuron using learning rule
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

# Connect excitatory fb neuron 1 to all recurrent neurons
# rand_out_w.next()
exc_fb_rec_conn_list = [[1, x, 0.1*w_rec_out_dist.next(), 1] for x in range(100)]
# Connect inhibitory fb neuron 2 to all recurrent neurons
# rand_out_w.next()
inh_fb_rec_conn_list = [[2, x, 0.1*w_rec_out_dist.next(), 1] for x in range(100)]

fb_out_rec_exc = p.Projection(
    pop_out, pop_rec, p.FromListConnector(exc_fb_rec_conn_list),
    p.StaticSynapse(weight=0.1, delay=1), receptor_type="exc_err")

fb_out_rec_inh = p.Projection(
    pop_out, pop_rec, p.FromListConnector(inh_fb_rec_conn_list),
    p.StaticSynapse(weight=0.1, delay=1), receptor_type="inh_err")


# Now to output layer to gate plasticity on output weights
# rand_out_w.next()
# rand_out_w.next()
exc_fb_out_conn_list  = [1, 0, w_out_out_dist.next(), 1]
inh_fb_out_conn_list  = [2, 0, w_out_out_dist.next(), 1]

fb_out_out_exc = p.Projection(
    pop_out, pop_out, p.FromListConnector([exc_fb_out_conn_list]),
    p.StaticSynapse(weight=0.0, delay=1), receptor_type="exc_err")

fb_out_out_inh = p.Projection(
    pop_out, pop_out, p.FromListConnector([inh_fb_out_conn_list]),
    p.StaticSynapse(weight=0.0, delay=1), receptor_type="inh_err")

###############################################################################
# Run Simulation
###############################################################################

pop_in.record('spikes')
pop_rec.record("spikes")
pop_out.record("all")

p.run(runtime)

in_spikes = pop_in.get_data('spikes')
pop_rec_data = pop_rec.get_data('spikes')
pop_out_data = pop_out.get_data()


# Plot
F = Figure(
    # plot data for postsynaptic neuron
    Panel(in_spikes.segments[0].spiketrains,
          yticks=True, markersize=2, xlim=(0, runtime)),
    Panel(pop_rec_data.segments[0].spiketrains,
          yticks=True, markersize=2, xlim=(0, runtime)
          ),
    Panel(pop_out_data.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[pop_out.label], yticks=True, xlim=(0, runtime)
          ),
    Panel(pop_out_data.segments[0].filter(name='gsyn_exc')[0],
          ylabel="gsyn excitatory (mV)",
          data_labels=[pop_out.label], yticks=True, xlim=(0, runtime)
          ),
    Panel(pop_out_data.segments[0].spiketrains,
          yticks=True, markersize=2, xlim=(0, runtime)),
    )

plt.show()
p.end()


print "job done"

