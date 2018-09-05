
import numpy

class spikeTrains(object):
    """
    """

    def __init__(self):
        """
        """
        pass

    def filterSpikes(self, inputSpikes, startTime, duration):
        """
        """
        newSpikeList = list()
        for elem in inputSpikes:
           neuronID, timeStamp = elem
           newTime = timeStamp - startTime

           if (newTime < duration and newTime >= 0):
               newSpikeList.append([neuronID, newTime])

        print "Found ", len(newSpikeList), " spikes"
        return newSpikeList
