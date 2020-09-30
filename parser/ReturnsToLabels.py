import logging
from Calendar import Calendar
import pandas as pd

class BinaryLabels(object):
    def __init__(self, serie, threshould=0.0, invert_labels=False):
        self.raw = serie.copy()
        self.threshould = threshould
        self.invert_labels = invert_labels

    def process(self):
        if (self.invert_labels):
            labels = self.raw.map(lambda x: int(x < self.threshould))
        else:
            labels = self.raw.map(lambda x: int(x > self.threshould))

        return labels

    def getID(self):
        return 'bl_ts'+str(self.threshould)+'_iv'+str(self.invert_labels)


class TernaryLabels(object):
    def __init__(self, serie, change=0.01):
        self.raw = serie.copy()
        self.threshould = change

    def process(self):
        labels = self.raw.map(lambda x: 0 if (abs(x) < self.threshould) else x/abs(x))
        return labels
        
        #df = pd.DataFrame({'returns': self.raw, 'labels': labels})
        #return df


class MagnitudeLabels(object):
    def __init__(self, serie, change=0.01):
        self.raw = serie.copy()
        self.threshould = change

    def process(self):

        if type(self.threshould) is list:
            labels = self.raw.map(lambda x: 0 if (abs(x) < self.threshould[0]) else (x/abs(x) if (abs(x) < (self.threshould[1]))  else 2 * x/abs(x)))
        else:
            labels = self.raw.map(lambda x: 0 if (abs(x) < self.threshould) else (x/abs(x) if (abs(x) < (2 * self.threshould))  else 2 * x/abs(x)))
        
        return labels
        
        #df = pd.DataFrame({'returns': self.raw, 'labels': labels})
        #return df