"""
Process reuslts files for the Simple Associative Memory

File: process_results.py

"""
#!/usr/bin/python
import spynnaker8 as p
import numpy, pylab, pickle
import os, sys
from pyNN.random import NumpyRNG, RandomDistribution
import constrainedPatternGenerator as pg
import spikeTrains as st

# Read back files containing data from one run:
#cell_params_lif = numpy.load("./myResults/patts_1/neuronParams.npy")
netInfo         = numpy.load("./myResults/patts_1/networkParams")
inPatterns      = numpy.load("./myResults/patts_1/inputPatterns")
outPatterns     = numpy.load("./myResults/patts_1/outputPatterns")
patternTiming   = numpy.load("./myResults/patts_1/patternTiming")
spikes          = numpy.load("./myResults/patts_1/outputSpikesFile.npy")

# Get needed variables from the info structure:
patternCycleTime = netInfo['cycleTime']
numPatterns      = netInfo['numPatterns']
numRecallRepeats = netInfo['numRecallRepeats']
nExcitNeurons    = netInfo['excitNeurons']
ProbFiring       = netInfo['probFiring']

numFiring = ProbFiring * nExcitNeurons

tolerance        = 2.5 # ms

spikeTrain = st.spikeTrains()
inRecall = False
pastStart = False
done = False
count = 0
maxFP = 0
maxFN = 0
#runningTP = 0
#runningFP = 0
#runningFN = 0
pairCount = 0

#toleranceList = [0.5, 1.0, 1.5, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
toleranceList = [0.4, 1.0, 2.0, 3.0, 4.0, 5.0, 8.0]
tolBins = len(toleranceList)
runningTP = list()
runningFP = list()
runningFN = list()
for i in range(tolBins):
    runningTP.append(0)
    runningFP.append(0)
    runningFN.append(0)

for patt in patternTiming:
   pattNo, timeStamp = patt
   if pattNo == -1 and pastStart == False:
       pastStart = True
   elif pattNo == -1 and pastStart == True and inRecall == False:
       inRecall = True
   elif pattNo != -1 and inRecall == True:
      #print "Pattern no: ", pattNo, ",  start time: ", timeStamp
      # Extract the spikes at the time stamp for this pattern:
      trimmedSpikes = spikeTrain.filterSpikes(spikes, timeStamp, patternCycleTime)
      # Compare against all patterns:
      if True:  # pairCount == 1:
         # For each tolerance, get the match:
         tolCount = 0
         for tol in toleranceList:
            if pattNo == 0  and tolCount == 0:
               display = True
            else:
               display=False
            truePos, falsePos, falseNeg, early, late = outPatterns[pattNo].compareSpikeTrains(trimmedSpikes, tolerance=tol, display=display)
            print "Start time: %d ms, Pattern: %d, tol: %.1f, TP: %4d, FP: %4d, FN: %4d, early: %d, late:%d"% (timeStamp, pattNo, tol, truePos, falsePos, falseNeg, early, late)
            runningTP[tolCount] += truePos
            runningFP[tolCount] += falsePos
            runningFN[tolCount] += falseNeg
            tolCount += 1

      pairCount = 1 - pairCount

print "Results for ", numPatterns, " patterns "
print numFiring, " of ", nExcitNeurons
for i in range(tolBins):
    avFP = (runningFP[i]*1.0)/(numPatterns * numRecallRepeats)
    avFN = (runningFN[i]*1.0)/(numPatterns * numRecallRepeats)
    avTP = (runningTP[i]*1.0)/(numPatterns * numRecallRepeats)
    print "Tolerance: %.1f,     mean TP: %.2f, FP: %.2f,  FN: %.2f\n" %(toleranceList[i], avTP, avFP, avFN)


