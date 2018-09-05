"""
Test inhibitory2 synapses and learning rule

File: inhib2_test.py

"""
#!/usr/bin/python
import spynnaker8 as p
#import pyNN.spiNNaker as p
#import spynnaker_extra_pynn_models as q
import numpy, pylab, pickle
import math
import os, sys
import traceback
from pyNN.utility.plotting import Figure, Panel
from pyNN.random import NumpyRNG, RandomDistribution
import constrainedPatternGenerator as pg
import spikeTrains as st

vScale = 0.5

usePlasticProj = True
binWidth       = 25.0

class lib_test_inhib2():
   "Perform single simulation run with inhib network"

   def __init__(self):
      """
      """
      pass

   def simulate_network(self, excitWeight):
      """
      """

      print "Started script lib_e2iW_sweep!"
      numpy.random.seed(seed=201)
      rng = NumpyRNG(seed=400)

      timeStep = 0.2

      p.setup(timestep=timeStep, min_delay = timeStep, max_delay = timeStep * 15)
      p.set_number_of_neurons_per_core(p.IF_curr_exp, 100)
      p.set_number_of_neurons_per_core(p.extra_models.IFCurrCombExp2E2I, 32)
      p.set_number_of_neurons_per_core(p.SpikeSourceArray, 32)
      p.set_number_of_neurons_per_core(p.SpikeSourcePoisson, 32)

      populations = list()
      projections = list()
      nExcitNeurons = 4  # was 8000
      nExcitFiring  = 1  # 800
      nStimulusNeurons = 25
      nStimulusFiring = 1
      nInhibNeurons = 80  # was 2000
      nInhibFiring  = 16
      patternCycleTime = 25

      e2eProbConn = 0.08  # Prob of connections
      e2iProbConn = 0.09   ## was 0.05 but this was not enough to keep inhib firing!!!
      i2eProbConn = 0.16  #  was 0.08
      i2iProbConn = 0.16

      e2eWeight = vScale * 0.25 # 0.0125 Weights
      e2iWeight = 0.25
      i2eWeight = vScale * 0.02  # weight was 0.02. 0.03 and 0.02 too high, 0.05 and 0.035 too high. 0.02, 0.01 and 0.013 seemed too low - double excit spikes # was 0.018, reduced to dampen inhib noise to excit
      i2iWeight = 0.07 # was 0.08

      e2eDelay = RandomDistribution('normal_clipped', (1.6, 1.2, timeStep, 3.0), rng=rng)  # Delays
      e2iDelay = RandomDistribution('normal_clipped', (1.6, 1.2, timeStep, 3.0), rng=rng)
      i2eDelay = RandomDistribution('normal_clipped', (0.8, 1.2, timeStep, 1.6), rng=rng)
      i2iDelay = RandomDistribution('normal_clipped', (0.8, 1.2, timeStep, 1.6), rng=rng)

      # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
      # Construct pattern set

      numPatterns = 2
      numRepeats = 10  # was 12
      numRecallRepeats = 1 # 2
      numBins = 15
      myJitter = 0.0
      interPatternGap = 0.0
      weight_to_force_firing = 31.85 # 31.5

      stimulus = 0
      #inhib = 1
      excit = 1
      teach = 2

      inPatterns  = list()
      outPatterns = list()
      for i in range(1):   # was numPatterns):
         patt = pg.pattern(nStimulusNeurons, nStimulusFiring, patternCycleTime, 10, numBins, rng=rng, spikeTrain=False, jitterSD = myJitter, spuriousSpikeProb = 0.0)
         patt.events = list()
         for j in range(25):
            patt.events.append((j,1.0*j))
         inPatterns.append(patt)
         patt = pg.pattern(nExcitNeurons, nExcitFiring, patternCycleTime, 1, numBins, rng=rng, spikeTrain=False, jitterSD = myJitter, spuriousSpikeProb = 0.0)
         patt.events = [(1, 15.0)]
         outPatterns.append(patt)

      timeCount = 0
      patternPresentationOrder = list()
      patternPresentationOrder.append(-1)
      teachingOrder = list()
      teachingOrder.append(-1)
      # Teaching phase:
      for patt in range(1):  # was numPatterns):
          for rpt in range(numRepeats):
              patternPresentationOrder.append(patt)
              teachingOrder.append(patt)
              timeCount +=1
      # Gap:
      patternPresentationOrder.append(-1)
      patternPresentationOrder.append(-1)
      teachingOrder.append(-1)
      teachingOrder.append(-1)
      timeCount +=2
      # Recall phase (show patterns in predetermined order):
      #pattOrder = range(numPatterns)
      pattOrder = [0]
      #numpy.random.shuffle(pattOrder) # Randomise presentation order
      # Input pattern but no teacher (test phase):
      for patt in pattOrder:
          for rpt in range(numRecallRepeats):
              patternPresentationOrder.append(-1)
              teachingOrder.append(-1)
              timeCount +=1

      # Construct a stream first to see how long the simulation will last:
      myStimulus=pg.spikeStream()
      patternTiming = myStimulus.buildStream(numSources=nStimulusNeurons, patterns=inPatterns, interPatternGap=interPatternGap, offset=0.0, order=patternPresentationOrder)

      runTime = myStimulus.endTime

      myStimulus=pg.spikeStream()
      patternTiming = myStimulus.buildStream(numSources=nStimulusNeurons, patterns=inPatterns, interPatternGap=interPatternGap, offset=0.0, rng = rng, noise = None, runTime = runTime, order=patternPresentationOrder)   # noise was 1Hz

      teachingInput=pg.spikeStream()
      teachingInput.buildStream(numSources=nExcitNeurons, patterns=outPatterns, interPatternGap=interPatternGap, offset=-1.0, rng = rng, noise = None, runTime = runTime, order=teachingOrder)


      # -------------------------------------------------------------
      # Learning Parameters:
      accDecayPerSecond      = 1.0
      # Excitatory: (used in stimulus to excit forward connections)
      potentiationRateExcit  = 0.99 # was 0.5 # 1.0 # SD! was 0.8
      accPotThresholdExcit   = 4 # was +6
      depressionRateExcit    = 0.0 # was 0.11 # 0.0  # was 0.4
      accDepThresholdExcit   = -10 # was -6
      meanPreWindowExcit     = 16.0 # 8
      meanPostWindowExcit    = 8.0 # 8
      maxWeightExcit         = e2eWeight # 0.2 # was 0.175
      minWeightExcit         = 0.00
      # Excitatory2: (teaching input)
      potentiationRateExcit2 = 0.0 # 1.0 # SD! was 0.8
      accPotThresholdExcit2  = 7
      depressionRateExcit2   = 0.0 # was 0.11 # 0.0  # was 0.4
      accDepThresholdExcit2  = -7
      meanPreWindowExcit2    = 11.0 # 8
      meanPostWindowExcit2   = 12.0 # 8
      maxWeightExcit2        = weight_to_force_firing # 31.00
      minWeightExcit2        = 0.00
      # Inhibitory: (used in inhib to excit forward connections)
      potentiationRateInhib  = 0.0
      accPotThresholdInhib   = 4
      depressionRateInhib    = 0.0
      accDepThresholdInhib   = -27
      meanPreWindowInhib     = 11.0
      meanPostWindowInhib    = 3.0
      maxWeightInhib         = i2eWeight # 0.02  # was 0.1
      minWeightInhib         = 0.0
      # Inhibitory2: (used in inhib to inhib lateral connections)
      potentiationRateInhib2 = 0.0
      accPotThresholdInhib2  = 2 # was 7
      depressionRateInhib2   = 0.9
      accDepThresholdInhib2  = -20
      meanPreWindowInhib2_fwd= 14.0
      meanPreWindowInhib2_rec= 10.0
      meanPostWindowInhib2   = 6.0
      maxWeightInhib2        = i2iWeight # 0.06  # was 0.1
      minWeightInhib2        = 0.75 * i2iWeight # 0.0

      total_delay            = 0.2

      # Forward params: min inhib2 synaptic value is zero
      cyclic_stdp_timing_params_fwd = p.extra_models.TimingDependenceCyclic(accum_decay = accDecayPerSecond,
                  accum_dep_thresh_excit  = accDepThresholdExcit, accum_pot_thresh_excit  = accPotThresholdExcit,
                     pre_window_tc_excit  = meanPreWindowExcit,     post_window_tc_excit  = meanPostWindowExcit,
                  accum_dep_thresh_excit2 = accDepThresholdExcit2, accum_pot_thresh_excit2 = accPotThresholdExcit2,
                     pre_window_tc_excit2 = meanPreWindowExcit2,     post_window_tc_excit2 = meanPostWindowExcit2,
                  accum_dep_thresh_inhib  = accDepThresholdInhib, accum_pot_thresh_inhib  = accPotThresholdInhib,
                     pre_window_tc_inhib  = meanPreWindowInhib,     post_window_tc_inhib  = meanPostWindowInhib,
                  accum_dep_thresh_inhib2 = accDepThresholdInhib2, accum_pot_thresh_inhib2 = accPotThresholdInhib2,
                     pre_window_tc_inhib2 = meanPreWindowInhib2_fwd, post_window_tc_inhib2 = meanPostWindowInhib2)

      cyclic_stdp_timing_params_rec = p.extra_models.TimingDependenceCyclic(accum_decay = accDecayPerSecond,
                  accum_dep_thresh_excit  = accDepThresholdExcit, accum_pot_thresh_excit  = accPotThresholdExcit,
                     pre_window_tc_excit  = meanPreWindowExcit,     post_window_tc_excit  = meanPostWindowExcit,
                  accum_dep_thresh_excit2 = accDepThresholdExcit2, accum_pot_thresh_excit2 = accPotThresholdExcit2,
                     pre_window_tc_excit2 = meanPreWindowExcit2,     post_window_tc_excit2 = meanPostWindowExcit2,
                  accum_dep_thresh_inhib  = accDepThresholdInhib, accum_pot_thresh_inhib  = accPotThresholdInhib,
                     pre_window_tc_inhib  = meanPreWindowInhib,     post_window_tc_inhib  = meanPostWindowInhib,
                  accum_dep_thresh_inhib2 = accDepThresholdInhib2, accum_pot_thresh_inhib2 = accPotThresholdInhib2,
                     pre_window_tc_inhib2 = meanPreWindowInhib2_rec, post_window_tc_inhib2 = meanPostWindowInhib2)

      # Forward params: min inhib2 synaptic value is zero
      cyclic_stdp_weight_params_fwd = p.extra_models.WeightDependenceCyclic(
             w_min_excit = minWeightExcit, w_max_excit = maxWeightExcit, A_plus_excit = potentiationRateExcit, A_minus_excit = depressionRateExcit,
             w_min_excit2 = minWeightExcit2, w_max_excit2 = maxWeightExcit2, A_plus_excit2 = potentiationRateExcit2, A_minus_excit2 = depressionRateExcit2,
             w_min_inhib = minWeightInhib, w_max_inhib = maxWeightInhib, A_plus_inhib = potentiationRateInhib, A_minus_inhib = depressionRateInhib,
             w_min_inhib2 = 0.0, w_max_inhib2 = i2eWeight, A_plus_inhib2 = potentiationRateInhib2, A_minus_inhib2 = depressionRateInhib2)

      # Recurrent params: have large minimum weight inhib2
      cyclic_stdp_weight_params_rec = p.extra_models.WeightDependenceCyclic(
             w_min_excit = minWeightExcit, w_max_excit = maxWeightExcit, A_plus_excit = potentiationRateExcit, A_minus_excit = depressionRateExcit,
             w_min_excit2 = minWeightExcit2, w_max_excit2 = maxWeightExcit2, A_plus_excit2 = potentiationRateExcit2, A_minus_excit2 = depressionRateExcit2,
             w_min_inhib = minWeightInhib, w_max_inhib = maxWeightInhib, A_plus_inhib = potentiationRateInhib, A_minus_inhib = depressionRateInhib,
             w_min_inhib2 = minWeightInhib2, w_max_inhib2 = maxWeightInhib2, A_plus_inhib2 = potentiationRateInhib2, A_minus_inhib2 = depressionRateInhib2)

      stdp_model_se = p.STDPMechanism(timing_dependence = cyclic_stdp_timing_params_fwd,
                                      weight_dependence = cyclic_stdp_weight_params_fwd,
                                      weight = i2eWeight, delay = e2eDelay)

      stdp_model_ie = p.STDPMechanism(timing_dependence = cyclic_stdp_timing_params_fwd,
                                      weight_dependence = cyclic_stdp_weight_params_fwd,
                                      weight = i2eWeight, delay = i2eDelay)

      stdp_model_i = p.STDPMechanism(timing_dependence = cyclic_stdp_timing_params_rec,
                                      weight_dependence = cyclic_stdp_weight_params_rec,
                                      weight = i2iWeight, delay = i2eDelay)

      #### Populations:
      # Stimulus population:
      populations.append(p.Population(nStimulusNeurons, p.SpikeSourceArray(spike_times =  myStimulus.streams), label="excitinput")) # 0

      # Inhib population:
      # Changed inh_b_tau from 2 to 4
      #inhib_tau_m = 3.0
      #populations.append(p.Population(nInhibNeurons, p.extra_models.IFCurrCombExp2E2I(cm = 0.25, i_offset = 0.0, tau_m = inhib_tau_m, tau_refrac = 2.0,
      #                                exc_a_tau  = 0.224, exc_b_tau  = 2.0, inh_a_tau = 0.224, inh_b_tau = 4.0, inh2_a_tau = 0.6, inh2_b_tau = 3.0,
      #                                v_reset = -6.0, v_rest = 0.0, v_thresh = 15.0), label='inhib_pop'))  # 1

      # excit population:
      populations.append(p.Population(nExcitNeurons, p.extra_models.IFCurrCombExp2E2I(cm = 0.25, i_offset = 0.0, tau_m = 10.0, tau_refrac = 2.0,
                                      exc_a_tau  = 0.224, exc_b_tau  = 2.0, inh_a_tau = 0.224, inh_b_tau = 4.0,
                                      exc2_a_tau = 0.2, exc2_b_tau = 0.02, inh2_a_tau = 0.6, inh2_b_tau = 3.0,
                                      v_reset = vScale*(-6.0), v_rest = 0.0, v_thresh = vScale*15.0), label='excit_pop'))  # 2

      # Teaching population:
      populations.append(p.Population(nExcitNeurons, p.SpikeSourceArray(spike_times = teachingInput.streams), label='teaching_ss_array')) # 3

      # Stimulus -to- inhib population:
      #populations.append(p.Population(nStimulusNeurons, p.SpikeSourceArray(spike_times =  myStimulus.streams), label="inhibinput")) # 4

      #### Projections:
      # Forward excitation (stimulus to excit):
      conn_list = list()
      w = 0.0
      for j in range(nStimulusNeurons):
         for i in range(nExcitNeurons):
             conn_list.append((j, i, w, #1))#(10*w)%2.4))
             j*i*0.2 % 2.4))
             w += 0.01


      for conn in conn_list:
          print conn_list.index(conn), conn

      projections.append(p.Projection(populations[stimulus], populations[excit], p.FromListConnector(conn_list),
                                       synapse_type=stdp_model_ie, receptor_type='inhibitory2'))
      projID = 0
      s2eProj = projID

       # Teaching input: (teach to excit, backward)
      projections.append(p.Projection(populations[teach], populations[excit], p.OneToOneConnector(),
                         p.StaticSynapse(weight=weight_to_force_firing, delay=timeStep), receptor_type='excitatory2'))
      projID += 1
      t2eProj = projID

      # XXXXXXXXXXXXXXXXXXXXX
      # Run network

      populations[stimulus].record(['spikes']) # input
      populations[excit].record(['spikes']) # excit layer
      populations[excit].record('v') # excit layer

      runTime = 10
      print "Run time is ", runTime

      p.run(runTime)

      stimSpikes = None
      spikes     = None

      excitPotentials = populations[excit].get_data('v')
      #potentials = populations[inhib].get_data('v')
      stimSpikes = populations[stimulus].get_data('spikes')
      spikes     = populations[excit].get_data('spikes')
      #inhibSpikes= populations[inhib].get_data('spikes')

      # ===============================
      # Stim Spikes count:
      counts = list()
      total = 0
      for i in range(nStimulusNeurons):
         counts.append(0)

      bins = list()
      spikeCountBins = int(1.0*runTime/binWidth) + 2

      for i in range(spikeCountBins):
         bins.append(0)

      nid=0
      for spikeTimes in stimSpikes.segments[0].spiketrains:
         for spikeTime in spikeTimes:
            counts[int(nid)] += 1
            bins[int(spikeTime/binWidth)] += 1
            total += 1
         nid += 1

      meanSpikeRate = (total * 1000.0/runTime ) / nStimulusNeurons
      print "Stim:   total: %d,  neurons: %d,   runTime: %d,   spike rate: %.2f" % (total, nStimulusNeurons, runTime, meanSpikeRate)

      # ===============================
      # Output Spikes count:
      counts = list()
      diffs = list()
      lastTime = list()
      total = 0
      for i in range(nExcitNeurons):
         counts.append(0)
         diffs.append([])
         lastTime.append(0.0)

      #mySpikes = spikes.segments[0].spiketrains
      #print "Number of spike trains is ", len(mySpikes)

      if True:
         nid=0
         for spikeTimes in spikes.segments[0].spiketrains:
            for spikeTime in spikeTimes:
               counts[int(nid)] += 1
               newDiff = float(spikeTime) - lastTime[int(nid)]
               newEntry = diffs[int(nid)]
               newEntry.append(newDiff)
               diffs[int(nid)] = newEntry
               lastTime[int(nid)] = float(spikeTime)
               total += 1
            try:
               print "Spikes this neuron: ", counts[int(nid)], "  Rate: ", counts[int(nid)]*1000.0/runTime
            except:
               print "Index causing problem was ", int(nid), " when counts has length ", len(counts)
               quit()
            nid   += 1

         meanExcitSpikeRate = (total * 1000.0/runTime ) / nExcitNeurons
         print "Excit: total: %d,  neurons: %d,   runTime: %d,   spike rate: %.2f" % (total, nExcitNeurons, runTime, meanExcitSpikeRate)


      # XXXXXXXXXXXXXXXXXXXXXX
      # Weight Statistics

      # stats for learning, stimulus-2-excit weights:
      if True:
         count_pos = 0
         count_plus = 0
         count_minus = 0
         significantWeight = maxWeightExcit / 2.0
         weightUse = {}
         gotAll = False
         failCount = 0
         while (gotAll != True and failCount < 10):
            try:
               final_weights = projections[s2eProj].get(attribute_names=['weight'], format='list', with_address=False)
               wName = "./w_s2e"
               numpy.save(wName, final_weights)
               gotAll = True
            except:
               failCount += 1
               final_weights = list()
               traceback.print_exc()
               os.system('date')
            idx = 0
            for w in final_weights:
               print "Synapse: {}, Weight: {}".format(idx, w)
               idx += 1

            myIndex = 0
            #print "   *** Weight values ***"
            outIdx = 0
            inIdx = 0
            for j in final_weights:
                  #print "%d : %d  - %d  : %.5f " %(outIdx, inIdx, myIndex, j)
                  myIndex += 1
                  if outIdx < 3:
                     outIdx += 1
                  else:
                     outIdx = 0
                     inIdx += 1
                     #print "="
                  partCount = 0
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
                      count_minus += 1

         #print "*** stimulus-2-excit weights (inhibitory): ****"
         #print "High weights: ", count_plus
         #print "Low weights: ", count_minus
         #print "Weight usage: ", weightUse
         #for k in weightUse.keys():
         #   print k, "   ", weightUse[k]
      # End if False (weight stats)

      os.system('date')

      doPlots = True
      if doPlots:
          Figure(
                Panel(excitPotentials.segments[0].filter(name='v')[0], ylabel="Excit Pot (mV)", yticks=True, xlabel = "Time (ms)", xlim=(0, runTime)),
          #      Panel(potentials.segments[0].filter(name='v')[0], ylabel="Inhib Pot (mV)", yticks=True, xlabel = "Time (ms)", xlim=(0, runTime)),
          #)
          #pylab.show()
          #Figure(
                Panel(stimSpikes.segments[0].spiketrains,
                      yticks=True, ylabel="Stimulus spikes", markersize=0.2, xticks = True, xlabel = "Time (ms)", xlim=(0, runTime)),
          #      Panel(inhibSpikes.segments[0].spiketrains,
          #            yticks=True, ylabel="Inib spikes", markersize=0.2, xticks = True, xlabel = "Time (ms)", xlim=(0, runTime)),
                Panel(spikes.segments[0].spiketrains,
                      yticks=True, ylabel="Memory neuron ID", markersize=0.5, xticks = True, xlabel = "Time (ms)", xlim=(0, runTime))
          )
          pylab.show()

      p.end()

      return meanSpikeRate, meanExcitSpikeRate


network = lib_test_inhib2()

a, b = network.simulate_network(0.01)

