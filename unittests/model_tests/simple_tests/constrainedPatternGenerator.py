"""
   Constrained Pattern Generator

   File: constrainedPatternGenerator.py

   Class of N-of-M patterns with a constrained number of spikes in each given sub-interval of the complete pattern cycle.

   Used to provide greater predictability of signal term.


"""

import numpy, pylab, copy
from pyNN.random import NumpyRNG, RandomDistribution

class pattern(object):
    """
    """

    def __init__(self, totalNeurons, firing, cycleTime, numIntervals, numBins, rng, spikeTrain=False, jitterSD = 0.0, spuriousSpikeProb = 0.0):
        """
        """
        self.totalNeurons = totalNeurons
        self.firing = firing
        self.cycleTime = cycleTime
        self.numIntervals = numIntervals
        self.intervalWidth = cycleTime * 1.0 / numIntervals
        self.jitterSD = jitterSD
        self.spuriousSpikeProb = spuriousSpikeProb
        self.numBins = numBins
        self.binSize = (1.0*cycleTime)/(1.0*numBins)
        self.events = list()
        self.binnedPattern = numpy.zeros( (totalNeurons, numBins+1) )
        if (firing > 0):
            self.firingFrac = (totalNeurons * 1.0)/firing
        # If there is no spike train, generate a pattern:
        if not spikeTrain:
           self.generateRandomPattern(rng)
           self.binPattern()
        else:
           # Extract binned values from the spike train:
           self.extractBinnedValues(spikeTrain)
        
    def generateRandomPattern(self, rng):
        """
        """
        unordered_events = list()
        rdNeurons = RandomDistribution('uniform', [0, self.totalNeurons-1], rng)
        rdTimes   = RandomDistribution('uniform', (0, self.intervalWidth), rng)
        #randomNeurons = rdNeurons.next(self.firing)
        randomTimes   = rdTimes.next(self.firing)
        index = 0
        numPerInterval = int((1.0 * self.firing)/self.numIntervals) 
        
        usedArray = numpy.zeros(self.totalNeurons)
        index = 0
        for i in range(self.numIntervals):
           intervalStart = int(i * self.intervalWidth * 5.0)/5.0   # Snap times to 0.2 ms intervals
           for j in range(numPerInterval):
               newTime =  intervalStart + int(randomTimes[index]*5)/5.0
               # Randomly choose next neuron to fire (unique):
               neuronID = int(rdNeurons.next(1));
               while (usedArray[neuronID] > 0):
                  neuronID = int(rdNeurons.next(1));
               usedArray[neuronID] = 1
               unordered_events.append((neuronID, newTime))
               index += 1
        self.events = unordered_events

    def binPattern(self):
        """
        Generate a binned version of this pattern
        """
        for spikeEvent in self.events: 
           (neuron, spikeTime) = spikeEvent
           binNum = int(1.0*spikeTime/self.binSize)
           self.binnedPattern[neuron, binNum] += 1

    def printPattern(self):
        """
        """
        for el in self.events:
            print el

    def aboutPattern(self):
        """
        """
        percentFiring = self.firing * 1.0 / self.totalNeurons
        print "Neurons: %d, firing: %d (%.1f%%),  cycle time: %d ms" % (self.totalNeurons, self.firing, percentFiring, self.cycleTime)

    def displayPattern(self):
        """
        """
        firingFrac = 100.0 * self.firing / self.totalNeurons
        print "*************************"
        print "Total neurons: ", self.totalNeurons
        print "Firing: ", self.firing, "(", firingFrac, "%)"
        print "Cycle time: ", self.cycleTime, "ms"
        print self.events
        print ""

    def patternGraphicalView(self, pattNum):
        if self.events != None:
           pylab.figure()
           pylab.plot([i[1] for i in self.events], [i[0] for i in self.events], ".")
           pylab.xlabel('Time/ms')
           pylab.ylabel('spikes')
           pylab.title('Spikes of pattern %d' % pattNum)


    def compareSpikeTrains(self, observedSpikes, tolerance = 2.5, display=False):
        """
        Count the number of differences between this pattern and another.
        This pattern is considered to be the golden reference.
        This pattern is a pattern-formatted list, the observed spikes is a list of 
        [neuron, time] pairs in neuron-then-time order.
        """
        truePositives  = 0
        falsePositives = 0
        falseNegatives = 0
        early = 0
        late = 0
        halfCycle = self.cycleTime / 2.0
        myObservedSpikes = copy.deepcopy(observedSpikes)
        for pattSpike in self.events:
            pattNeuronID, pattTimeIndex = pattSpike
            # Is this spike present in the observed spikes:
            matched = False
            for spike in myObservedSpikes:
                neuronID, timeIndex = spike
                if pattNeuronID == neuronID:
                    #if display:
                    #    print "Pattern: ", pattTimeIndex, ",  observed: ", timeIndex
                    ## Spike must be observed before its official time, but no more than windowSz before:
                    #if timeIndex <= pattTimeIndex and (timeIndex + windowSz) >=  pattTimeIndex:
                    # spike must be observed within a tolerance value of its intended time:
                    # If difference is out by more than a half cycle, it's really closer to the spike
                    # in the next or previous cycle:
                    timeDiff = pattTimeIndex - timeIndex
                    if timeDiff > halfCycle:
                       timeDiff -= self.cycleTime
                    elif timeDiff < -halfCycle:
                       timeDiff += self.cycleTime
                    if abs(timeDiff) <= tolerance:
                        #if pattTimeIndex >= (timeIndex - tolerance) and pattTimeIndex <= (timeIndex + tolerance):
                        # Spike is in correct position, but only count it once:
                        if not matched:
                            truePositives += 1
                            matched = True
                        if timeDiff < 0:
                            late += 1   # Observed spike was too late
                        elif timeDiff > 0:
                            early += 1  # Observed spike was too early
                        # Remove this observed spike from the list so we don't use it again:
                        myObservedSpikes.remove(spike)
            # Checked against all the observed spikes. Did we find a match?
            if not matched:
                falseNegatives += 1 # Missing spike for this pattern - that's a false negative
                #print "False neg for teacher @ time ", pattTimeIndex
        # Checked all expected spikes against all observed spikes. Any left are false positives:
        falsePositives = len(myObservedSpikes)
        #print "False pos list: ", myObservedSpikes
        
        return truePositives, falsePositives, falseNegatives, early, late

    def extractBinnedValues(self, spikeTrain):
        """
        SpikeTrain is a list of neuron ID/spike time pairs. Extract them and place them in 
        the binning matrix.
        """
        for elem in spikeTrain:
            neuronID, timeStamp = elem
            binNum = int(timeStamp / self.binSize)
            if binNum > self.numBins:
               print "ERROR! in patternGenerator.extractBinnedValues() time stamp ", timeStamp,
               print "mapped to bin # ", binNum, " is too big (max ", self.numBins, ")"
               quit()
               
            if neuronID < 0 or neuronID >= self.totalNeurons:
               print "ERROR! in patternGenerator.extractBinnedValues(), neuronID ", neuronID,
               print "is not in expected range, (0 to ", self.totalNeurons, ")"
               quit()
            self.binnedPattern[neuronID, binNum] += 1

    def writePatternToFile(self, fileName):
        """
        """
        fullName = "./%s" % fileName
        fsock=open(fullName, 'w')
        for event in self.events:
           for elem in event:
              myString = "%f " % elem
              fsock.write("%s" % myString)

           fsock.write("\n")
        fsock.close()

    def writeBinsToFile(self, fileName):
        """
        """
        fullName = "./%s" % fileName
        fsock=open(fullName, 'w')
        for neuron in range(self.totalNeurons):
           header = "\n%d: " % neuron
           fsock.write("%s" % header)
           for binNum in range(self.numBins):
              if self.binnedPattern[neuron, binNum] == 1:
                 myString = "1"
              else:
                 myString = "0"
              fsock.write("%s" % myString)
           footer = "\n"
           fsock.write("%s" % footer)
        fsock.close()

    def testGenerator(self):
        """
        """
        numpy.random.seed(seed=1)
        rng = NumpyRNG(seed=1)

        patt = pattern(2000, 100, 36, 4, 18, rng, spikeTrain=False, jitterSD = 0.0, spuriousSpikeProb = 0.0)
        patt.printPattern()

class spikeStream(object):
    """
    """
    def __init__(self):
        """
        """
        self.streams = list()
        self.endTime = 0

    def buildStream(self, numSources=None, patterns=None, interPatternGap=10, rng=None, offset=0.0,order=None, noise=None, runTime = 0, printTimes = False):
        """
        """
        suppressPatternSpikes = False
        # Establish a list of times at which pattern start firing:
        patternTimes = list()
        numRandoms = 0
        # Create empty streams, one per source neuron:
        if noise is not None:
           if rng == None:
              print "ERROR in buildStream() - Noise added but no RNG specified!"
              quit()
           rdTimes = RandomDistribution('exponential', [1000.0/noise], rng=rng)
        for i in range(numSources):
             baseList = list()
             if (noise is not None):
                # Fill array with Poisson spikes at given background freq:
                timeIdx = 0
                while (timeIdx < runTime):
                   randomDelay = rdTimes.next(1)[0]
                   timeIdx += randomDelay
                   baseList.append(int(timeIdx*5)/5.0)
                   numRandoms += 1
             self.streams.append(baseList)

        # Go through order parameter, which is a list of the patterns to be appended.
        # For each one, append it.
        timePtr = 0
        jitterDistribution = RandomDistribution('normal', (0.0, patterns[0].jitterSD), rng = rng)
        for entry in order:
            if entry == -1:
                # Add blank entry:
                patternEntry = [entry, timePtr]
                patternTimes.append(patternEntry)
                # Create a gap (20ms):
                timePtr += 25
            else:
                #print "Pattern ", entry, " starts at time ", timePtr
                if printTimes:
                    print "Pattern ", entry, " starts at time ", timePtr
                if entry >= len(patterns):
                    print "ERROR: Pattern set requested pattern ", entry, \
                          " and pattern set has only ", len(patterns), " patterns"
                    return -1
                elif entry < 0:
                    print "ERROR: Entry less than zero requested!"
                    return -1
                patternEntry = [entry, timePtr]
                patternTimes.append(patternEntry)
                pattern = patterns[entry]
                biggestTimestamp = 0
                for element in pattern.events:
                    index, timestamp = element
                    timestamp += offset
                    if patterns[0].jitterSD > 0:
                        newNum = jitterDistribution.next(1)
                        #print "Base T: ", timestamp, " : ", newNum,
                        timestamp += newNum
                        if timestamp < 0:
                           timestamp = 0.0
                        #print ", new: ", timestamp
                    biggestTimestamp = max(biggestTimestamp, timestamp)
                    if suppressPatternSpikes == False:
                        self.streams[index].append(timePtr + timestamp)
                timePtr += pattern.cycleTime + interPatternGap
        self.endTime = timePtr

        for i in range(len(self.streams)):
           self.streams[i].sort()
        return patternTimes


