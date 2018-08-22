"""
Inhib Tuning

File: inhib_tuning.py

"""
#!/usr/bin/python
import spynnaker8 as p
#import pyNN.spiNNaker as p
#import spynnaker_extra_pynn_models as q
import numpy, pylab, pickle
import math
import os, sys
from pyNN.utility.plotting import Figure, Panel
from pyNN.random import NumpyRNG, RandomDistribution
import constrainedPatternGenerator as pg
import spikeTrains as st

numpy.random.seed(seed=201)
rng = NumpyRNG(seed=400)

timeStep = 0.2

p.setup(timestep=timeStep, min_delay = timeStep, max_delay = timeStep * 14)
p.set_number_of_neurons_per_core(p.IF_curr_exp, 100)
p.set_number_of_neurons_per_core(p.extra_models.IFCurrCombExp2E2I, 96)
p.set_number_of_neurons_per_core(p.SpikeSourceArray, 100)
p.set_number_of_neurons_per_core(p.SpikeSourcePoisson, 100)

populations = list()
projections = list()
nExcitNeurons = 8000
nStimulusNeurons = 8000
stimulusFiringRate = 14.0
nStimulusFiring = 1600
patternCycleTime = 30

e2eProbConn = 0.07
e2iProbConn = 0.04
i2iProbConn = float(sys.argv[1])

#e2eWeight = 5.0/50.0   # 0.021 spike rate
#e2eWeight = 5.0/30.0   # 0.028 spike rate
#e2eWeight = 5.0/25.0   # 2.4826 spike rate
#e2eWeight = 5.0/20.0    # 19.57 spike rate
# With recurrent inhib: (i2iProbConn = 0.05)
#e2eWeight = 5.0/20.0    # 4.07 spike rate
#i2iWeight = 0.1
#e2eWeight = 5.0/20.0    # 9.34 spike rate
#i2iWeight = 0.025
# With recurrent inhib: (i2iProbConn = 0.13)
#e2eWeight = 0.25  # 5.0/20.0=0.25  # 9.16 spike rate
#i2iWeight = 0.01
e2eWeight = 0.10  # 5.0/20.0=0.25  # 1.26 spike rate
e2iWeight = 0.10  # 5.0/20.0=0.25  # 1.26 spike rate
i2iWeight = 0.06

e2eDelay = RandomDistribution('normal_clipped', (0.6, 0.8, timeStep, 3*2.8), rng=rng)
e2iDelay = RandomDistribution('normal_clipped', (0.6, 0.8, timeStep, 3*2.8), rng=rng)
i2iDelay = RandomDistribution('normal_clipped', (1.6, 0.6, timeStep, 3*2.8), rng=rng)  # was 0.6 not 1.6

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# Construct pattern set

numPatterns = 1
numRepeats = 100
numBins = 10
myJitter = 0.0
interPatternGap = 0.0
runTime = 3000

inPatterns = list()
for i in range(numPatterns):
   patt = pg.pattern(nStimulusNeurons, nStimulusFiring, patternCycleTime, 10, numBins, rng=rng, spikeTrain=False, jitterSD = myJitter, spuriousSpikeProb = 0.0)
   inPatterns.append(patt)

timeCount = 0
patternPresentationOrder = list()
patternPresentationOrder.append(-1)
teachingOrder = list()
teachingOrder.append(-1)
# Teaching phase:
for patt in range(numPatterns):
    for rpt in range(numRepeats):
        patternPresentationOrder.append(patt)
        teachingOrder.append(patt)
        timeCount +=1

# Construct a stream first to see how long the simulaton will last:
myStimulus=pg.spikeStream()
patternTiming = myStimulus.buildStream(numSources=nStimulusNeurons, patterns=inPatterns, interPatternGap=interPatternGap, rng = rng, runTime=runTime, offset=0.0, order=patternPresentationOrder, noise=7.0)

runTime = myStimulus.endTime

cell_params_lif   = {'cm'        : 0.25, # nF was 0.25
                     'i_offset'  : 0.0,
                     'tau_m'     : 10.0,
                     'tau_refrac': 2.0,
                     'tau_syn_E' : 0.8,
                     'tau_syn_I' : 0.8,
                     'v_reset'   : -5.0,
                     'v_rest'    : 0.0,
                     'v_thresh'  : 15.0
                     }

#populations.append(p.Population(nStimulusNeurons, p.SpikeSourcePoisson(rate = stimulusFiringRate), label="stimulus"))
spikeArray = {'spike_times': myStimulus.streams}
populations.append(p.Population(nStimulusNeurons, p.SpikeSourceArray(spike_times =  myStimulus.streams), label="input"))

#populations.append(p.Population(nExcitNeurons, p.IF_curr_exp, cell_params_lif, label='excit_pop'))  # 1

populations.append(p.Population(nExcitNeurons, p.extra_models.IFCurrCombExp2E2I(cm = 0.25, i_offset = 0.0, tau_m = 10.0, tau_refrac = 2.0, exc_a_tau  = 0.224, exc_b_tau  = 2.0, inh_a_tau = 0.224, inh_b_tau = 2.0, v_reset = -6.0, v_rest = 0.0, v_thresh = 15.0), label='excit_pop'))  # 1

# Forward excitation:
projections.append(p.Projection(populations[0], populations[1], p.FixedProbabilityConnector(p_connect=e2iProbConn), p.StaticSynapse(weight=e2iWeight, delay=e2iDelay), receptor_type='excitatory'))
# Recurrent inhibition:
projections.append(p.Projection(populations[1], populations[1], p.FixedProbabilityConnector(p_connect=i2iProbConn), p.StaticSynapse(weight=i2iWeight, delay=i2iDelay), receptor_type='inhibitory'))

# XXXXXXXXXXXXXXXXXXXXX
# Run network

populations[0].record(['spikes']) # input
populations[1].record(['spikes']) # memory

p.run(runTime)

stimSpikes = None
spikes     = None

#stimSpikes =  populations[0].getSpikes(compatible_output=True)
#spikes     = populations[1].getSpikes(compatible_output=True)
stimSpikes =  populations[0].get_data('spikes')
spikes     = populations[1].get_data('spikes')

# Stim Spikes count:
counts = list()
total = 0
for i in range(nStimulusNeurons):
   counts.append(0)

nid=0
for spikeTimes in stimSpikes.segments[0].spiketrains:
   for spikeTime in spikeTimes:
      counts[int(nid)] += 1
      total += 1
   nid += 1

meanSpikeRate = (total * 1000.0/runTime ) / nStimulusNeurons
print "Stim:   total: %d,  neurons: %d,   runTime: %d,   spike rate: %.2f" % (total, nExcitNeurons, runTime, meanSpikeRate)

# Output spikes count:
counts = list()
total = 0
for i in range(nExcitNeurons):
   counts.append(0)

nid=0
for spikeTimes in spikes.segments[0].spiketrains:
   for spikeTime in spikeTimes:
      counts[int(nid)] += 1
      total += 1
   nid   += 1

meanSpikeRate = (total * 1000.0/runTime ) / nExcitNeurons
print "Output: total: %d,  neurons: %d,   runTime: %d,   spike rate: %.2f" % (total, nExcitNeurons, runTime, meanSpikeRate)

fsock=open("./with_real_pattern_recurrent_inhib_results.txt", 'a')
myString = "N: %d We2e: %.3f   Wi2i: %.3f   Pconn_i2i: %.3f Spike rate: %.2f\n" %( nExcitNeurons, e2eWeight, i2iWeight, i2iProbConn, meanSpikeRate)
fsock.write("%s\n" % myString)
fsock.close()

  
doPlots = True
if doPlots:
    Figure(
          Panel(stimSpikes.segments[0].spiketrains,
                yticks=True, ylabel="Stimulus ID", markersize=0.2, xticks = True, xlabel = "Time (ms)", xlim=(0, runTime)),
          Panel(spikes.segments[0].spiketrains,
                yticks=True, ylabel="Memory ID", markersize=0.2, xticks = True, xlabel = "Time (ms)", xlim=(0, runTime))
    )
    pylab.show()

p.end()

