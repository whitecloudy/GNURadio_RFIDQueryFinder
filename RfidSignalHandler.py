from GNURadioComplexFileReader.IqDataReader import IqDataReader as IQreader
from Signal.SignalStartSearcher import SignalStartSearcher as StartSearcher
import numpy as np
import sys

class RfidSignalHandler:
    def __init__(self, filename, sample_rate):
        self.__iqStream = IQreader(filename)
        self.__sample_rate = sample_rate
    
    def preambleFinder(self, iqStream, avgDC, avgIQ):
        i = 0
        while i < 26:
            #find DownPulse
            for d in iqStream:
                d -= avgDC
                if abs(avgIQ)/2 > abs(d):
                    break
            #find UpPulse
            deadCount = 0
            for d in iqStream:
                d -= avgDC
                if abs(avgIQ)/2 < abs(d):
                    break
                if deadCount == 30:
                    print("Find Dead")
                    print(iqStream.getConsumedSize())
                    i = -1
                    deadCount += 1
                else:
                    deadCount += 1
            i+=1


    def process(self):
        iqStream = self.__iqStream

        avgDC = StartSearcher(self.__iqStream).getDCavg()
        avgIQ = abs(np.array(iqStream.read(100)).mean() - avgDC)

        while iqStream.getRemainSize()>10000:
            self.preambleFinder(iqStream, avgDC, avgIQ)
            iqStream.read(50)
            avg = (np.array(iqStream.read(100)).mean()-avgDC)
            print(avg.imag, ',' ,avg.real)


fileName = sys.argv[1]
rfidHandler = RfidSignalHandler(fileName, 2.5e6)
rfidHandler.process()
