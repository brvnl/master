import sys, logging, os.path
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

import pandas as pd

class BaseDataset(object):
    def __init__(self, X=None, Y=None, test=0.2, featureSelection=None, fromFile=None, balance=False):
        self.logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(format='%(asctime)s %(levelname)s* %(message)s', level=logging.INFO)

        if (fromFile is not None):
            hdf = pd.HDFStore(fromFile)
            self.X = hdf['X']
            self.Y = hdf['Y']
            hdf.close()
        else:
            intersection = X.index.intersection(Y.index)
            self.X = X.loc[intersection]
            self.Y = Y.loc[intersection]

        totalrecords = len(self.X.index)

        self.logger.info("Using %d timestamps from the intersection of X(%d) and Y(%d)." %(totalrecords , len(X.index), len(Y.index)))

        if (totalrecords < 2):
            raise ValueError('Not enough valid records on the dataset.')

        self.nRecordsTest = int(totalrecords * test)
        self.nRecordsTrain = totalrecords - self.nRecordsTest
        self.logger.info("Using %d rows for training and %d for testing." %(self.nRecordsTrain, self.nRecordsTest))
        self.logger.info("Series starting at %s, ending at %s." \
               %(self.Y.first('1D').index.strftime("%Y-%m-%d").item(), \
                 self.Y.last('1D').index.strftime("%Y-%m-%d").item()))

        if (featureSelection is not None):
            self.X = featureSelection.process(self.X)

    def size(self):
        return (self.nRecordsTest + self.nRecordsTrain)

    def persist(self, path):        
        hdf = pd.HDFStore(path)
        hdf['X'] = pd.DataFrame(self.X)
        hdf['Y'] = pd.DataFrame(self.Y)
        hdf.close()

    def getStatistics(self):
        train = self.getYTrain().value_counts(sort=False)
        test = self.getYTest().value_counts(sort=False)
        total = self.Y.value_counts(sort=False)
        df = pd.DataFrame({"train": train, 
                           "test": test, 
                           "total": total})
        return df

    
    def getXCVTrainIndexes(self):
        df_xtrain = self.getXTrain()

        p = 0.25
        t = len(df_xtrain)
        n = int(t * p)

        #return df_xtrain.head(n).index.values.astype(int)
        return df_xtrain.head(n).index.values.to_datetime()

    def getXCVTestIndexes(self):
        df_xtrain = self.getXTrain()

        p = 0.25
        t = len(df_xtrain)
        n = t - int(t * p)

        return df_xtrain.tail(n).index.values.to_datetime()

    def getXTrain(self):
        return self.X.head(self.nRecordsTrain)

    def getYTrain(self):
        return self.Y.head(self.nRecordsTrain)

    def getXTest(self):
        return self.X.tail(self.nRecordsTest)

    def getYTest(self):
        return self.Y.tail(self.nRecordsTest)
