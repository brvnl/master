# encoding=utf8
from unicodedata import normalize 
from sklearn.feature_selection import VarianceThreshold
import logging
import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectPercentile, chi2, mutual_info_regression,f_regression,f_classif
from sklearn.preprocessing import KBinsDiscretizer
from nltk.corpus import stopwords

#--------------------------------------------------------------------------------------
# To do.
#--------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------
# Basic:
#--------------------------------------------------------------------------------------
class _BaseSelection(object):
    def __init__(self, previousSelection=None):
        self.previous = previousSelection
        self.logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(format='%(asctime)s %(levelname)s* %(message)s', level=logging.INFO)
        self.id = ""

    def process(self, attributes):
        if (self.previous is None):
            return attributes
        else:
            return self.previous.process(attributes)

    def getID(self):
        if (self.previous is None):
            return self.id
        else:
            return self.previous.getID() + "-" + self.id


class RemoveConstantAttributes(_BaseSelection):
    def __init__(self, previousSelection=None):
        super(RemoveConstantAttributes, self).__init__(previousSelection)
        self.id = "LV"

    def process(self, attributes):
        newAttr = super(RemoveConstantAttributes, self).process(attributes)
        selector = VarianceThreshold()
        selector.fit(newAttr)

        df =  newAttr[newAttr.columns[selector.get_support(indices=True)]]

        nColumnsBefore = len(newAttr.columns)
        nColumnsAfter = len(df.columns)
        self.logger.info("%s: Reduced from %d to %d features (%.2f %%)." %(self.__class__.__name__, \
            nColumnsBefore, \
            nColumnsAfter, \
            (100 * float(nColumnsAfter)/nColumnsBefore)))

        return df

class CustomChi2(_BaseSelection):
    def __init__(self, y, percent=None, previousSelection=None):
        super(CustomChi2, self).__init__(previousSelection)
        self.y = y
        self.percent = percent
        self.id = "Chi2_pc" + str(self.percent)

    def process(self, attributes):
        X = super(CustomChi2, self).process(attributes)

        #bins = [0, 0.33, 0.66, 1]
        #labels = [1,2,3]
        #X_binned = pd.cut(X, bins=bins, labels=labels)

        #bins = np.linspace(X.values.min(), X.values.max(), 3)
        #X_binned = X.groupby(np.digitize(X, bins))
        est = KBinsDiscretizer(n_bins=3, encode='ordinal', strategy='uniform')
        est.fit(X)  
        X_binned = pd.DataFrame(est.transform(X), columns=X.columns.values)

        #print(X_binned[:1].to_string())

        selector = SelectPercentile(chi2, percentile=(self.percent*100))
        selector.fit(X_binned, self.y)

        si = selector.get_support(indices=True)
        df =  X[X.columns[si]]

        nColumnsBefore = len(X.columns)
        nColumnsAfter = len(df.columns)
        self.logger.info("%s: Reduced from %d to %d features (%.2f %%)." %(self.__class__.__name__, \
            nColumnsBefore, \
            nColumnsAfter, \
            (100 * float(nColumnsAfter)/nColumnsBefore)))

        return df

class CustomMutualInfo(_BaseSelection):
    def __init__(self, y, percent=None, previousSelection=None):
        super(CustomMutualInfo, self).__init__(previousSelection)
        self.y = y
        self.percent = percent
        self.id = "MI_pc" + str(self.percent)

    def process(self, attributes):
        X = super(CustomMutualInfo, self).process(attributes)

        selector = SelectPercentile(mutual_info_regression, percentile=(self.percent*100))
        selector.fit(X, self.y)
        df =  X[X.columns[selector.get_support(indices=True)]]

        nColumnsBefore = len(X.columns)
        nColumnsAfter = len(df.columns)
        self.logger.info("%s: Reduced from %d to %d features (%.2f %%)." %(self.__class__.__name__, \
            nColumnsBefore, \
            nColumnsAfter, \
            (100 * float(nColumnsAfter)/nColumnsBefore)))

        return df

class CustomFScore(_BaseSelection):
    def __init__(self, y, percent=None, previousSelection=None, classification=False):
        super(CustomFScore, self).__init__(previousSelection)
        self.y = y
        self.percent = percent
        self.id = "FM_pc" + str(self.percent)
        self.classification = classification

    def process(self, attributes):
        X = super(CustomFScore, self).process(attributes)

        if (self.classification):
            selector = SelectPercentile(f_classif, percentile=(self.percent*100))
        else:
            selector = SelectPercentile(f_regression, percentile=(self.percent*100))

        selector.fit(X, self.y)
        df =  X[X.columns[selector.get_support(indices=True)]]

        nColumnsBefore = len(X.columns)
        nColumnsAfter = len(df.columns)
        self.logger.info("%s: Reduced from %d to %d features (%.2f %%)." %(self.__class__.__name__, \
            nColumnsBefore, \
            nColumnsAfter, \
            (100 * float(nColumnsAfter)/nColumnsBefore)))

        return df

class CorrCoef(_BaseSelection):
    def __init__(self, returns_serie, threshould=None, percent=None, previousSelection=None):
        super(CorrCoef, self).__init__(previousSelection)
        self.returns = returns_serie
        self.threshould = threshould
        self.percent = percent

        if (self.threshould is not None):
            self.id = "CC_th" + str(self.threshould)
        else:
            if (self.percent is None):
                self.percent = 0.75
            self.id = "CC_pc" + str(self.percent)
        
        self.df_corr = None

    def setPercent(self, pct):
        self.percent = pct
        self.id = "CC_pc" + str(self.percent)

    def precalc(self, newAttr):
        # Getting date intersection between the two datasets
        intersection = newAttr.index.intersection(self.returns.index)
        newAttr = newAttr.loc[intersection]
        r = self.returns.loc[intersection]

        corr_list = [ newAttr[w].corr(r) for w in newAttr.columns.values ]
        self.df_corr = pd.DataFrame({'correlation':corr_list, 'token':newAttr.columns.values})
        self.df_corr["correlation"] = pd.to_numeric(self.df_corr["correlation"])


    def process(self, attributes):
        newAttr = super(CorrCoef, self).process(attributes)

        if (self.df_corr is None):
            self.precalc(newAttr)
        
        if (self.percent == 1):
            nColumnsBefore = len(newAttr.columns)
            nColumnsAfter = len(newAttr.columns)
            self.logger.info("%s: Reduced from %d to %d features (%.2f %%)." %(self.__class__.__name__, \
                nColumnsBefore, \
                nColumnsAfter, \
                (100 * float(nColumnsAfter)/nColumnsBefore)))
                
            return newAttr

        if (self.threshould is not None):
            rows2remove = self.df_corr[abs(self.df_corr['correlation']) < self.threshould ]
            df = newAttr.drop(columns=rows2remove['token'].tolist())

        else:
            self.df_corr['correlation'] = self.df_corr['correlation'].abs()
            tokens2keep = self.df_corr.sort_values('correlation', ascending=False)
            tokens2keep = tokens2keep.head(int(len(tokens2keep)*(self.percent)))
            df = newAttr[tokens2keep['token'].tolist()]

        nColumnsBefore = len(newAttr.columns)
        nColumnsAfter = len(df.columns)
        self.logger.info("%s: Reduced from %d to %d features (%.2f %%)." %(self.__class__.__name__, \
            nColumnsBefore, \
            nColumnsAfter, \
            (100 * float(nColumnsAfter)/nColumnsBefore)))

        return df  

class RemoveStopWords(_BaseSelection):
    def __init__(self, previousSelection=None):
        super(RemoveStopWords, self).__init__(previousSelection)
        self.id = "RSW"

    def process(self, attributes):
        X = super(RemoveStopWords, self).process(attributes)
        sw = stopwords.words('portuguese')
        
        fcolumns = [w for w in X.columns if w not in sw ]
        df = X[fcolumns]

        nColumnsBefore = len(X.columns)
        nColumnsAfter = len(df.columns)
        self.logger.info("%s: Reduced from %d to %d features (%.2f %%)." %(self.__class__.__name__, \
            nColumnsBefore, \
            nColumnsAfter, \
            (100 * float(nColumnsAfter)/nColumnsBefore)))

        return df


class WhiteList(_BaseSelection):
    def __init__(self, wlist, previousSelection=None):
        super(WhiteList, self).__init__(previousSelection)
        self.id = "WL"
        self.wl = wlist

    def process(self, attributes):
        X = super(WhiteList, self).process(attributes)
        
        fcolumns = list(set(X.columns) & set(self.wl))
        #fcolumns = [w for w in X.columns if w in self.wl ]
        df = X[fcolumns]

        nColumnsBefore = len(X.columns)
        nColumnsAfter = len(df.columns)
        self.logger.info("%s: Reduced from %d to %d features (%.2f %%)." %(self.__class__.__name__, \
            nColumnsBefore, \
            nColumnsAfter, \
            (100 * float(nColumnsAfter)/nColumnsBefore)))

        return df