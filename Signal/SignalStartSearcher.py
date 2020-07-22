from GNURadioComplexFileReader.IqDataReader import IqDataReader as IQreader
import numpy as np

class SignalStartSearcher:
    def __init__(self, iqStream, *, initIgnoreSampleNum =1000, dcSampleNum =5000, kValue=0.2):
        if iqStream.getRemainSize() < (initIgnoreSampleNum+dcSampleNum):
            raise ValueError
        else:
            self.iqStream = iqStream
            #data will be ignored
            iqStream.read(initIgnoreSampleNum)
            
            #data that will be used to calculate average
            sampleDatas = np.array(iqStream.read(dcSampleNum))
            self.dc_avg = sampleDatas.mean()
            self.dc_std = sampleDatas.std()
            self.kValue = kValue

            self.find_start_point()
            
    def find_start_point(self):
        iqStream = self.iqStream
        threshold = complex(0)
        findFlag = False

        for d in iqStream:
            d -= self.dc_avg
            threshold = self.kValue*d + (1-self.kValue)*threshold

            if abs(threshold) > self.dc_std * 4:
                print("find signal start")
                print(iqStream.getConsumedSize())
                break
            
        return iqStream

    def getDCavg(self):
        return self.dc_avg


