"""
Cyclic-stdp network

File: cyclic_stdp_network.py

"""
#!/usr/bin/python
import spynnaker8 as p
import numpy, pylab, pickle
import traceback
import os, sys
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt
from pyNN.random import NumpyRNG, RandomDistribution
import constrainedPatternGenerator as pg
import spikeTrains as st

numpy.random.seed(seed=1)
rng = NumpyRNG(seed=1)

# Reset the board before starting:

timeStep = 0.1 # 0.313 is just on the cusp, was 0.2, works with: 0.2, 0.25, 0.3. Fails with: 0.5, 0.4, 0.333, 0.325

backgroundNoise = False
noiseSpikeFreq = 1.6 # Hz per neuron, added to signal gives 7Hz spike rate
fullyConnected = False

p.setup(timestep=timeStep, min_delay = timeStep, max_delay = timeStep * 14)
p.set_number_of_neurons_per_core(p.IF_curr_exp, 200)
p.set_number_of_neurons_per_core(p.extra_models.IFCondCombExp2E2I, 40) # was 80)
p.set_number_of_neurons_per_core(p.extra_models.IFCurrCombExp2E2I, 40) # was 80)
p.set_number_of_neurons_per_core(p.SpikeSourceArray, 50)

nSourceNeurons = 32000 # number of input (excitatory) neurons
nExcitNeurons  = 3200 # number of excitatory neurons in the recurrent memory
sourcePartitionSz = 80 # Number of spike sources in a single projection
inhibPartitionSz = 4

nInhibNeurons  = nExcitNeurons / 4  # number of inhibitory neurons in the recurrent memory
inhibFiringRate = 14.0

numPartitions = 1.0 * nSourceNeurons / sourcePartitionSz
if numPartitions != int(numPartitions):
   print "Invalid excit partition size! Exiting!!!"
   quit()
numPartitions = int(numPartitions)

numInhibPartitions = 1.0 * nInhibNeurons / inhibPartitionSz
if numInhibPartitions != int(numInhibPartitions):
   print "Invalid inhib partition size! Exiting!!!"
   quit()
numInhibPartitions = int(numInhibPartitions)

nTeachNeurons  = nExcitNeurons
total_delay    = timeStep   # 5*timeStep # ms # works with 5, 4


dendriticDelayFraction = 1.0

#!param
ProbFiring     = 0.025
myJitter       = 0.0 # was 0.25 # was 0.119
#-----
delay_e2e      = RandomDistribution('uniform', (timeStep, timeStep * 5.0), rng=rng) # was 0.8 # ms
pconn_e2e      = 0.1

# 0.6 0.2
delay_e2i      = p.RandomDistribution('normal_clipped', mu=0.2, sigma=0.4, low=timeStep, high=timeStep * 5.0, rng=rng) # Was 0.2 # ms
pconn_e2i      = 0.08
weight_e2i     = 0.12  # Working with no i2i when 0.12

delay_i2e      = p.RandomDistribution('normal_clipped', mu=0.2, sigma=0.4, low=timeStep, high=timeStep * 5.0, rng=rng) # 0.2 # XXX was 0.2 # ms
pconn_i2e      = 0.2  # 0.2 was too little
weight_i2e     = 0.15

# -------------------------------------------------------------
# Learning Parameters:
accDecayPerSecond      = 1.0
# Excitatory:
potentiationRateExcit  = 0.8 # was 0.5 # 1.0 # SD! was 0.8
accPotThresholdExcit   = 6 # was 6
depressionRateExcit    = 0.0 # was 0.11 # 0.0  # was 0.4
accDepThresholdExcit   = -6
meanPreWindowExcit     = 12.0 # 8
meanPostWindowExcit    = 8.0 # 8
maxWeightExcit         = 0.5/20.0 # was 5 was 0.175
minWeightExcit         = 0.1
# Excitatory2:
potentiationRateExcit2 = 0.0 # 1.0 # SD! was 0.8
accPotThresholdExcit2  = 7
depressionRateExcit2   = 0.0 # was 0.11 # 0.0  # was 0.4
accDepThresholdExcit2  = -7
meanPreWindowExcit2    = 11.0 # 8
meanPostWindowExcit2   = 12.0 # 8
maxWeightExcit2        = 0.01
minWeightExcit2        = 0.00
# Inhibitory:
potentiationRateInhib  = 9.0
accPotThresholdInhib   = 7
depressionRateInhib    = 10.0
accDepThresholdInhib   = -7
meanPreWindowInhib     = 6.0
meanPostWindowInhib    = 7.0
maxWeightInhib         = 0.00  # was 0.1
minWeightInhib         = 0.00
# Inhibitory2:
potentiationRateInhib2 = 13.0
accPotThresholdInhib2  = 7
depressionRateInhib2   = 14.0
accDepThresholdInhib2  = -7
meanPreWindowInhib2    = 10.0
meanPostWindowInhib2   = 10.0
inhib2PotIncrement     = 0.0
inhib2DepDecrement     = 0.0
#inhib2PotIncrement     = 0.015  # How much to add to weight if activity too high
#inhib2DepDecrement     = 0.005  # How much to take away if activity too low
maxWeightInhib2        = 0.0  # was 0.1
minWeightInhib2        = 0.0

# -------------------------------------------------------------

nSourceFiring  = int(nSourceNeurons * ProbFiring)
nExcitFiring   = int(nExcitNeurons * ProbFiring)

patternCycleTime = 30
numPatterns = int(sys.argv[1])
numRepeats  = 12 # was 15
numRecallRepeats  = 3
binSize = 4
numBins = patternCycleTime/binSize
interPatternGap = 0    # was 10
potentiationRate = 0.80
accPotThreshold = 5
depressionRate = 0.40  # was 0.66
accDepThreshold = -5
meanPostWindow = 8.0

baseline_excit_weight = minWeightExcit # 0.0
initial_inhib_weight = 0.00   # SD was 0.01 until 10/2/18
weight_to_force_firing = 0.05
# Max_weight for 30K neurons: 0.18, for 40K neurons: 0.135
max_weight = 0.6 # was 0.25          # 0.8               # Max weight! was 0.66 in best run so far
min_weight = 0.0
#--- How much charge in one spike with appropriate diff-of-Gaussians shape?
T1 = 2.0; T2 = 0.224; a1 = 3.5; a2 = 3.5 # Gives Same shape and size as Kunkel, Diesman Alpha synapse
T1_teach = 0.02; T2_teach = 0.2; # Aiming for exp-type decay, with sharp onset for teaching input.
T1_inhib2 = 3.0; T2_inhib2 = 0.6 # Create much wider pulse for inhib2, so that it provides smooth subtraction from background level

print "Pattern cycle time: ", patternCycleTime
print "Source neurons: ", nSourceNeurons
print "Excit neurons: ", nExcitNeurons
print "Inhib neurons: ", nInhibNeurons
print "Source firing: ", nSourceFiring
print "Excit firing: ", nExcitFiring
print "Jitter SD: ", myJitter
print "Pattern cycle time: ", patternCycleTime, "ms"
print "Num patterns: ", numPatterns
print "Num repeats during learning: ", numRepeats
print "Num repeats during recall: ", numRecallRepeats
print "Num partitions: ", numPartitions
print "Partition size: ", sourcePartitionSz
print "Inhib partition sz: ", inhibPartitionSz

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# Construct pattern set

inPatterns = list()
outPatterns = list()
for i in range(numPatterns):
   patt = pg.pattern(nSourceNeurons, nSourceFiring, patternCycleTime, 10, numBins, rng, spikeTrain=False, jitterSD = myJitter, spuriousSpikeProb = 0.0)
   inPatterns.append(patt)
   patt = pg.pattern(nExcitNeurons, nExcitFiring, patternCycleTime, 10, numBins, rng, spikeTrain=False, jitterSD = myJitter, spuriousSpikeProb = 0.0)
   #patt.events=[(i, 11.0)]
   #patt.events=[]
   outPatterns.append(patt)

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
# Gap:
patternPresentationOrder.append(-1)
patternPresentationOrder.append(-1)
timeCount +=2
# Recall phase (show patterns in random order):
pattOrder = range(numPatterns)
numpy.random.shuffle(pattOrder) # Randomise presentation order
for patt in pattOrder:
    for rpt in range(numRecallRepeats):
        patternPresentationOrder.append(patt)
        timeCount +=1

# Construct a stream first to see how long the simulaton will last:
myStimulus=pg.spikeStream()
patternTiming = myStimulus.buildStream(numSources=nSourceNeurons, patterns=inPatterns, interPatternGap=interPatternGap, offset=0.0, order=patternPresentationOrder)

runTime = myStimulus.endTime + 500

myStimulus=pg.spikeStream()
patternTiming = myStimulus.buildStream(numSources=nSourceNeurons, patterns=inPatterns, interPatternGap=interPatternGap, offset=0.0, rng = rng, noise = None, runTime = runTime, order=patternPresentationOrder)

teachingInput=pg.spikeStream()
teachingInput.buildStream(numSources=nExcitNeurons, patterns=outPatterns, interPatternGap=interPatternGap, offset=-1.0, rng = rng, noise = None, runTime = runTime, order=teachingOrder)

print "***"
print "Run time is ", runTime, " ms"
print "***"

# Save network info:
netInfo= dict()
netInfo['sourceNeurons']    = nSourceNeurons
netInfo['excitNeurons']     = nExcitNeurons
netInfo['probFiring']       = ProbFiring
netInfo['backgroundNoise']  = backgroundNoise
netInfo['noiseSpikeFreq']   = noiseSpikeFreq
netInfo['fullyConnected']   = fullyConnected
netInfo['jitter']           = myJitter
netInfo['totalDelay']       = total_delay
netInfo['dendriticFrac']    = dendriticDelayFraction
netInfo['cycleTime']        = patternCycleTime
netInfo['numPatterns']      = numPatterns
netInfo['numRepeats']       = numRepeats
netInfo['numRecallRepeats'] = numRecallRepeats
netInfo['runTime']          = runTime
#netInfo['potRate']          = potentiationRate
#netInfo['depRate']          = depressionRate
#netInfo['potThresh']        = accPotThreshold
#netInfo['depThresh']        = accDepThreshold
netInfo['potentiationRateExcit']  = potentiationRateExcit
netInfo['accPotThresholdExcit']   = accPotThresholdExcit
netInfo['depressionRateExcit']    = depressionRateExcit
netInfo['accDepThresholdExcit']   = accDepThresholdExcit
netInfo['meanPreWindowExcit']     = meanPreWindowExcit
netInfo['meanPostWindowExcit']    = meanPostWindowExcit
netInfo['potentiationRateExcit2'] = potentiationRateExcit2
netInfo['accPotThresholdExcit2']  = accPotThresholdExcit2
netInfo['depressionRateExcit2']   = depressionRateExcit2
netInfo['accDepThresholdExcit2']  = accDepThresholdExcit2
netInfo['meanPreWindowExcit2']    = meanPreWindowExcit2
netInfo['meanPostWindowExcit2']   = meanPostWindowExcit2
netInfo['potentiationRateInhib']  = potentiationRateInhib
netInfo['accPotThresholdInhib']   = accPotThresholdInhib
netInfo['depressionRateInhib']    = depressionRateInhib
netInfo['accDepThresholdInhib']   = accDepThresholdInhib
netInfo['meanPreWindowInhib']     = meanPreWindowInhib
netInfo['meanPostWindowInhib']    = meanPostWindowInhib
netInfo['inhib2PotIncrement']     = inhib2PotIncrement
netInfo['inhib2DepDecrement']     = inhib2DepDecrement
netInfo['potentiationRateInhib2'] = potentiationRateInhib2
netInfo['accPotThresholdInhib2']  = accPotThresholdInhib2
netInfo['depressionRateInhib2']   = depressionRateInhib2
netInfo['accDepThresholdInhib2']  = accDepThresholdInhib2
netInfo['meanPreWindowInhib2']    = meanPreWindowInhib2
netInfo['meanPostWindowInhib2']   = meanPostWindowInhib2
netInfo['maxWeightExcit']         = maxWeightExcit;
netInfo['minWeightExcit']         = maxWeightExcit;
netInfo['maxWeightExcit2']        = maxWeightExcit2;
netInfo['minWeightExcit2']        = maxWeightExcit2;
netInfo['maxWeightInhib']         = maxWeightInhib;
netInfo['minWeightInhib']         = minWeightInhib;
netInfo['maxWeightInhib2']        = maxWeightInhib2;
netInfo['minWeightInhib2']        = minWeightInhib2;
dirName = "./myResults/patts_%d" % numPatterns
os.system("mkdir %s" % dirName)
os.system("cp ./cyclic_stdp_network.py %s" % dirName)
os.system("cp ./spikeTrains.py %s" % dirName)
os.system("cp ./constrainedPatternGenerator.py %s" % dirName)
with open(dirName+"/networkParams", "wb") as outfile:
    pickle.dump(netInfo, outfile, protocol=pickle.HIGHEST_PROTOCOL)
with open(dirName+"/inputPatterns", "wb") as outfile:
    pickle.dump(inPatterns, outfile, protocol=pickle.HIGHEST_PROTOCOL)
with open(dirName+"/outputPatterns", "wb") as outfile:
    pickle.dump(outPatterns, outfile, protocol=pickle.HIGHEST_PROTOCOL)
with open(dirName+"/patternTiming", "wb") as outfile:
    pickle.dump(patternTiming, outfile, protocol=pickle.HIGHEST_PROTOCOL)
with open(dirName+"/teachStream", "wb") as outfile:
    pickle.dump(teachingInput.streams, outfile, protocol=pickle.HIGHEST_PROTOCOL)

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# Construct Network

populations = list()
projections = list()

stimulus = 0
inhib = numPartitions
excit  = numPartitions #+ numInhibPartitions
teacher = excit + 1
print "I/P Partitions: ", numPartitions
print "Layer excit: ", excit
print "Teacher: ",teacher

teachingSpikeArray = {'spike_times': teachingInput.streams}

for i in range(numPartitions):
    arrayLabel = "ssArray%d" % i
    startIdx = i * sourcePartitionSz
    endIdx = startIdx + sourcePartitionSz
    streamSubset = myStimulus.streams[startIdx:endIdx]
    spikeArray = {'spike_times': streamSubset}
    populations.append(p.Population(sourcePartitionSz, p.SpikeSourceArray(spike_times = streamSubset), label=arrayLabel))

if False:
  for i in range(numInhibPartitions):
    arrayLabel = "sspInhib%d" % i
    startIdx = i * inhibPartitionSz
    endIdx = startIdx + inhibPartitionSz
    streamSubset = myStimulus.streams[startIdx:endIdx]
    populations.append(p.Population(inhibPartitionSz, p.SpikeSourcePoisson, {'rate': inhibFiringRate}, label=arrayLabel))

#populations.append(p.Population(nInhibNeurons, p.SpikeSourcePoisson, {'rate': inhibFiringRate}, label="inhib_pop"))

#populations.append(p.Population(nExcitNeurons, p.extra_models.IFCondCombExp2E2I(cm = 0.25, i_offset = 0.0, tau_m = 10.0, tau_refrac = 2.0, exc_a_tau  = T2, exc_b_tau  = T1, exc2_a_tau = T2_teach, exc2_b_tau = T1_teach, inh2_a_tau = T2_inhib2, inh2_b_tau = T1_inhib2, v_reset = -6.0, v_rest = 0.0, v_thresh = 15.0), label='excit_pop'))  # 1
populations.append(p.Population(nExcitNeurons, p.extra_models.IFCondCombExp2E2I(cm = 0.25, i_offset = 0.0, tau_m = 15.0, tau_refrac = 2.0, exc_a_tau  = T2, exc_b_tau  = T1, exc2_a_tau = T2_teach, exc2_b_tau = T1_teach, inh2_a_tau = T2_inhib2, inh2_b_tau = T1_inhib2, v_reset = -6.0, v_rest = 0.0, v_thresh = 15.0), label='excit_pop'))  # 1

#populations[excit].set(v_reset=-18.0)
populations[excit].set(e_rev_E=20.0)
populations[excit].set(e_rev_E2=56.0)
populations[excit].set(e_rev_I=-10.0)
populations[excit].set(e_rev_I2=-5.0)

#populations.append(p.Population(nExcitNeurons, p.extra_models.IF_curr_comb_exp_2E2I, cell_params_lif_2E2I, label='excit_pop'))  # numInhibPartitions + 1

populations.append(p.Population(nTeachNeurons, p.SpikeSourceArray, teachingSpikeArray, label='teaching_ss_array'))

stdp_model = p.STDPMechanism(
      timing_dependence=p.extra_models.TimingDependenceCyclic(accum_decay = accDecayPerSecond,
            accum_dep_thresh_excit  = accDepThresholdExcit, accum_pot_thresh_excit  = accPotThresholdExcit,
               pre_window_tc_excit  = meanPreWindowExcit,     post_window_tc_excit  = meanPostWindowExcit,
            accum_dep_thresh_excit2 = accDepThresholdExcit2, accum_pot_thresh_excit2 = accPotThresholdExcit2,
               pre_window_tc_excit2 = meanPreWindowExcit2,     post_window_tc_excit2 = meanPostWindowExcit2,
            accum_dep_thresh_inhib  = accDepThresholdInhib, accum_pot_thresh_inhib  = accPotThresholdInhib,
               pre_window_tc_inhib  = meanPreWindowInhib,     post_window_tc_inhib  = meanPostWindowInhib,
            accum_dep_thresh_inhib2 = accDepThresholdInhib2, accum_pot_thresh_inhib2 = accPotThresholdInhib2,
               pre_window_tc_inhib2 = meanPreWindowInhib2,     post_window_tc_inhib2 = meanPostWindowInhib2),

            weight_dependence = p.extra_models.WeightDependenceCyclic(
       w_min_excit = minWeightExcit, w_max_excit = maxWeightExcit, A_plus_excit = potentiationRateExcit, A_minus_excit = depressionRateExcit,
       w_min_excit2 = minWeightExcit2, w_max_excit2 = maxWeightExcit2, A_plus_excit2 = potentiationRateExcit2, A_minus_excit2 = depressionRateExcit2,
       w_min_inhib = minWeightInhib, w_max_inhib = maxWeightInhib, A_plus_inhib = potentiationRateInhib, A_minus_inhib = depressionRateInhib,
       w_min_inhib2 = minWeightInhib2, w_max_inhib2 = maxWeightInhib2, A_plus_inhib2 = potentiationRateInhib2, A_minus_inhib2 = depressionRateInhib2),
       weight = baseline_excit_weight, delay = timeStep * 10.0)

#stdp_model_std = p.STDPMechanism(
#        timing_dependence=p.SpikePairRule(
#            tau_plus=16.7, tau_minus=23.7),
#        weight_dependence=p.AdditiveWeightDependence(
#            w_min=0.0, w_max=1.0, A_plus=0.005, A_minus=0.005),
# )

# Partition main projections into a number of sub-projections:
for i in range(numPartitions):
   if fullyConnected:
      projections.append(p.Projection(populations[i], populations[excit], p.AllToAllConnector(), receptor_type='excitatory', synapse_type=stdp_model))
   else:
      projections.append(p.Projection(populations[i], populations[excit], p.FixedProbabilityConnector(p_connect=pconn_e2e), receptor_type='excitatory', synapse_type=stdp_model))
      #projections.append(p.Projection(populations[i], populations[excit], p.FixedProbabilityConnector(p_connect=pconn_e2e), p.StaticSynapse(weight=weight_to_force_firing, delay=timeStep), receptor_type='excitatory'))
      #projections.append(p.Projection(populations[i], populations[excit], p.FixedProbabilityConnector(p_connect=pconn_e2e), p.StaticSynapse(weight=baseline_excit_weight, delay=timeStep), receptor_type='excitatory'))

inhibProj = numPartitions
# projections from inhibitory neurons to excitatory, to provide inhib-2 synapses, used to maintain activity at 7Hz level:
#if False:
# for i in range(numInhibPartitions):
#   projections.append(p.Projection(populations[inhib+i], populations[excit], p.FixedProbabilityConnector(p_connect=pconn_i2e), p.StaticSynapse(weight=initial_inhib_weight, delay=delay_i2e), receptor_type='inhibitory2', ##Broken!!! synapse_dynamics=p.SynapseDynamics(slow=stdp_model)))

# Teaching input with target pattern (uses excit-2 synapses with more exponential shaping):
projections.append(p.Projection(populations[teacher], populations[excit], p.OneToOneConnector(), p.StaticSynapse(weight=weight_to_force_firing, delay=timeStep), receptor_type='excitatory2'))

# XXXXXXXXXXXXXXXXXXXXX
# Run network

populations[stimulus].record(['spikes'])
populations[excit].record(['spikes'])
#populations[excit].record(['v'], indexes=[0,1,2,3,4,5])
populations[teacher].record(['spikes'])

# Only get the membrane potential for small networks:
#populations[excit].record_v(indexes=range(0, nExcitNeurons, 16), sampling_interval=0.2)

os.system('date')
p.run(runTime)
os.system('date')

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# Get output spikes and save them to file

v = None
gsyn = None
stimSpikes = None
spikes = None
inhibSpikes = None
teachSpikes = None

# Get spikes the old way for processing:
if True:
   gotAll = False
   failCount = 0
   while (gotAll != True and failCount < 10):
      try:
         spikes = populations[excit].spinnaker_get_data('spikes')
         gotAll = True
      except:
         failCount += 1
         final_weights = list()
         traceback.print_exc()
         os.system('date')

   numpy.save(dirName+"/outputSpikesFile", spikes)

# Get spikes the new way for plotting:
spikes = None
if True:
   gotAll = False
   failCount = 0
   while (gotAll != True and failCount < 10):
      try:
         spikes = populations[excit].get_data('spikes')
         gotAll = True
      except:
         failCount += 1
         final_weights = list()
         traceback.print_exc()
         os.system('date')

# Get membrane potentials:
memPots = None
if False:
   gotAll = False
   failCount = 0
   while (gotAll != True and failCount < 10):
      try:
         memPots = populations[excit].get_data('v')
         gotAll = True
      except:
         failCount += 1
         final_weights = list()
         traceback.print_exc()
         os.system('date')

# Get stim spikes:
stimSpikes = None
if True:
   gotAll = False
   failCount = 0
   while (gotAll != True and failCount < 10):
      try:
         stimSpikes = populations[stimulus].get_data('spikes')
         gotAll = True
      except:
         failCount += 1
         final_weights = list()
         traceback.print_exc()
         os.system('date')

# Get teach spikes:
teachSpikes = None
if True:
   gotAll = False
   failCount = 0
   while (gotAll != True and failCount < 10):
      try:
         teachSpikes = populations[teacher].get_data('spikes')
         gotAll = True
      except:
         failCount += 1
         final_weights = list()
         traceback.print_exc()
         os.system('date')


#stimSpikes  =  populations[stimulus].get_data('spikes')
#teachSpikes =  populations[teacher].get_data('spikes')

os.system('date')

# XXXXXXXXXXXXXXXXXXXXXX
# Weight Statistics

# stats for learning, excitatory weights:
if True:
   count_pos = 0
   count_plus = 0
   count_minus = 0
   significantWeight = maxWeightExcit / 5.0
   weightUse = {}
   for i in range(numPartitions):
       gotAll = False
       failCount = 0
       while (gotAll != True and failCount < 10):
          try:
             final_weights = projections[i].get(attribute_names=['weight'], format='list', with_address=False)
             #final_weights = projections[i].getWeights(format="list")
             wName = dirName + "/w_%d" % i
             numpy.save(wName, final_weights)
             gotAll = True
          except:
             failCount += 1
             final_weights = list()
             traceback.print_exc()
             os.system('date')
       for j in final_weights:
                partCount = 0
            #for j in row:
                myString=j
                if myString in weightUse:
                    weightUse[myString] += 1
                else:
                    weightUse[myString] = 1
                if j > 0.0:
                    count_pos += 1
                    partCount += 1
                if j > significantWeight:
                    count_plus += 1
                    partCount += 1
                if j <= 0.0:
                    count_minus += 1
       # Clear memory holding unneeded weight data:
       projections[i]._host_based_synapse_list = None

   print "*** excit-1 weights: ****"
   print "Positive weights: ", count_pos
   print "High weights: ", count_plus
   print "Low weights: ", count_minus
   print "Weight usage: ", weightUse
   fsock=open(dirName+"/weights.txt", 'a')
   myString = "Positive weights: %d\nHigh: %d\nLow: %d\n" %(count_pos, count_plus, count_minus)
   fsock.write("%s\n" % myString)
   for key in weightUse.keys():
      myString = "%.6f  :  %d " % (key, weightUse[key])
      fsock.write("%s\n" % myString)
   fsock.close()

# End if False (weight stats)

# Weight stats for inhib-2 weights (maintains network activity at constant level):
if False:
   count_plus = 0
   count_minus = 0
   w_count = 0.0
   numI2Weights = 0
   weightUse = {}
   for i in range(numInhibPartitions):
       gotAll = False
       failCount = 0
       while (gotAll != True and failCount < 10):
          try:
             final_weights = projections[inhibProj+i].getWeights(format="list")
             gotAll = True
          except:
             failCount += 1
             final_weights = list()
             traceback.print_exc()
             os.system('date')
       numI2Weights += len(final_weights)
       for j in final_weights:
                partCount = 0
                w_count += j
            #for j in row:
                myString=j
                if myString in weightUse:
                    weightUse[myString] += 1
                else:
                    weightUse[myString] = 1
                if j > 0.0:
                    count_plus += 1
                    partCount += 1
                if j <= 0.0:
                    count_minus += 1
       # Clear memory holding unneeded weight data:
       projections[inhibProj+i]._host_based_synapse_list = None

   print "Inhib partitions: ", numInhibPartitions
   print "NumI2 weights ", numI2Weights
   mean_inhib2_weight = -1
   if numI2Weights > 0:
      mean_inhib2_weight = (1.0 * w_count) / numI2Weights


   print "*** inhib-2 weights: ****"
   print "High weights: ", count_plus
   print "Low weights: ", count_minus
   print "Mean weight: ", mean_inhib2_weight
   print "Weight usage: ", weightUse
# End if False (weight stats)

os.system('date')

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# Draw Plots

doPlots = True
if doPlots:
    Figure(
        Panel(stimSpikes.segments[0].spiketrains,
              yticks=True, ylabel="Stimulus ID", xticks = True, xlabel = "Stim Time (ms)", xlim=(0, runTime)),
        Panel(teachSpikes.segments[0].spiketrains,
              yticks=True, ylabel="Teach ID", xticks = True, xlabel = "Teach Time (ms)", xlim=(0, runTime)),
        Panel(spikes.segments[0].spiketrains,
              yticks=True, ylabel="Memory ID", xticks = True, xlabel = "Memory Time (ms)", xlim=(0, runTime))
        #Panel(memPots.segments[0].filter(name='v')[0], ylabel="Membrane potential (mV)", yticks=True, xlim=(0, runTime))
        # data_labels=[pop_src1.label],
        #Panel(exc_data.segments[0].filter(name='gsyn_exc')[0],
        #      ylabel="gsyn excitatory (mV)",
        #      data_labels=[pop_src1.label], yticks=True, xlim=(0, runtime)),
        #Panel(exc_data.segments[0].filter(name='gsyn_inh')[0],
        #      ylabel="gsyn inhibitory (mV)",
        #      data_labels=[pop_src1.label], yticks=True, xlim=(0, runtime)),
    #     Panel(exc_data.segments[0].spiketrains,
    #           yticks=True, markersize=0.2, xlim=(0, runtime)),
        #annotations="Post-synaptic neuron firing frequency: {} Hz".format(
        #len(exc_data.segments[0].spiketrains[0]))
    )
    plt.show()

    os.system('date')

p.end()

