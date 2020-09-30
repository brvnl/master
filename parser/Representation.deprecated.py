# encoding=utf8
from __future__ import division
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import stopwords
from nltk.probability import FreqDist

from multiprocessing import Process
from multiprocessing import Pool
from multiprocessing import Manager
from multiprocessing import cpu_count
from parser.Preprocessing import BaseProcessing
from parser.CustomCorpusReaders import TitleCorpusReader
from parser.CustomCorpusReaders import FullCorpusReader
from parser.CustomCorpusReaders import BodyCorpusReader

import itertools
import pandas as pd
import logging

#======================================================================================
# This file contains classes used to transform textual information into a proper machine
# learning representation.
#======================================================================================


def mergeDicts(x, y):
    z = x.copy()
    z.update(y)
    return z


def computeTF(rp, filesByDay, vocabulary, pprocess, reader):
    tempTFDict = {}
    for timestamp in sorted(filesByDay):
        # create a temporary corpus for each timestamp

        if (reader == "PlaintextCorpusReader"):
            corpus = PlaintextCorpusReader(root=rp, fileids=filesByDay[timestamp])
        elif (reader == "TitleCorpusReader"):
            corpus = TitleCorpusReader(root=rp, fileids=filesByDay[timestamp])
        elif (reader == "FullCorpusReader"):
            corpus = FullCorpusReader(root=rp, fileids=filesByDay[timestamp])
        elif (reader == "BodyCorpusReader"):
            corpus = BodyCorpusReader(root=rp, fileids=filesByDay[timestamp])
        else:
            corpus = PlaintextCorpusReader(root=rp, fileids=filesByDay[timestamp])

        # compute frequencies for the timestamp
        tempTFDict[timestamp] = FreqDist(pprocess.process(corpus.words()))

    return tempTFDict


def splitDict(aDict, nbr=2):
    size = len(aDict)
    chunk = int(size/nbr)

    l_dicts = []
    if (chunk > 1):
        i = iter(aDict.items())
        l_dicts = [ dict(itertools.islice(i, chunk)) for x in range(1, nbr) ]
        l_dicts.append(dict(i))

    else:
        l_dicts = [aDict]

    return l_dicts


#--------------------------------------------------------------------------------------
# TODO.
#--------------------------------------------------------------------------------------
class Text2TF(object):
    def __init__(self, grouper, l_vocabulary=None, rootPath="", pClass=None, curpusReader=PlaintextCorpusReader):
        self.logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(format='%(asctime)s %(levelname)s* %(message)s', level=logging.INFO)

        self.reader = curpusReader
        self.grouper = grouper
        self.rootPath = rootPath

        if (pClass is None):
            self.preprocessingClass = BaseProcessing()
        else:
            self.preprocessingClass = pClass

        if l_vocabulary is None:
            self.logger.info("Building vocabulary.")
            self.__buildVocabulary()
        else:
            self.l_vocabulary = l_vocabulary

        self.logger.info("Words retrieved in vocabulary: %d." %(len(self.l_vocabulary)))    

        self.logger.info("Calculating attributes.")

        # Data stored in dictionary format
        d_data = self.__calculate()

        # Convert dictionary to dataframe
        df_temp = pd.DataFrame.from_dict(d_data)
        self.df_data = df_temp.T

        return

    def __calculate(self):
        np = cpu_count()
        p = Pool(processes=np)

        fDict = splitDict(self.grouper.group(), np)
        results = [ p.apply_async(computeTF, args=(self.rootPath, d, self.l_vocabulary, self.preprocessingClass, self.reader)) for d in fDict ]

        d_data = {}
        for r in results:
            d_data = mergeDicts(d_data, r.get())

        p.close()
        p.terminate()

        return d_data

    def __buildVocabulary(self):
        l_files = self.grouper.raw()

        if (self.reader == "PlaintextCorpusReader"):
            corpus = PlaintextCorpusReader(root=self.rootPath, fileids=l_files)
        elif (self.reader == "TitleCorpusReader"):
            corpus = TitleCorpusReader(root=self.rootPath, fileids=l_files)
        elif (self.reader == "FullCorpusReader"):
            corpus = FullCorpusReader(root=self.rootPath, fileids=l_files)
        elif (self.reader == "BodyCorpusReader"):
            corpus = BodyCorpusReader(root=self.rootPath, fileids=l_files)
        else:
            corpus = PlaintextCorpusReader(root=self.rootPath, fileids=l_files)


        self.l_vocabulary = sorted(set(self.preprocessingClass.process(corpus.words())))

        return 0

    def getVocabulary(self):
        return self.l_vocabulary

    def getData(self):
        self.df_data.index = pd.to_datetime(self.df_data.index)
        self.df_data.fillna(0, inplace=True)
        return self.df_data

    def getID(self):
        return "TF"

    def size(self):
        return len(self.df_data.index)

    def saveToCSV(self, filepath):
        df = self.getData()
        df.to_csv(filepath, sep=",")
        self.logger.info("Data saved to: \"%s\"." %(filepath))

        return 0 


#--------------------------------------------------------------------------------------
# Each word will be marked as 1, when the word is present in the give document, or 0, 
# otherwise.
#--------------------------------------------------------------------------------------
class Text2BoW(Text2TF):
    def __init__(self, grouper, l_vocabulary=None, rootPath="", pClass=None, corpusReader=PlaintextCorpusReader): 
        super(Text2BoW, self).__init__(grouper, l_vocabulary, rootPath, pClass, corpusReader)
        self.df_data = self.df_data.applymap(lambda x: int(x > 1))

    def getID(self):
        return "BoW"


#--------------------------------------------------------------------------------------
# TODO.
#--------------------------------------------------------------------------------------
class Text2TFIDF(Text2TF):
    def __init__(self, grouper, l_vocabulary=None, rootPath="", pClass=None, corpusReader=PlaintextCorpusReader):
        super(Text2TFIDF, self).__init__(grouper, l_vocabulary, rootPath, pClass, corpusReader)

        l_files = self.grouper.raw()
        if (self.reader == "PlaintextCorpusReader"):
            tempcorpus = PlaintextCorpusReader(root=self.rootPath, fileids=l_files)
        elif (self.reader == "TitleCorpusReader"):
            tempcorpus = TitleCorpusReader(root=self.rootPath, fileids=l_files)
        elif (self.reader == "FullCorpusReader"):
            tempcorpus = FullCorpusReader(root=self.rootPath, fileids=l_files)
        elif (self.reader == "BodyCorpusReader"):
            tempcorpus = BodyCorpusReader(root=self.rootPath, fileids=l_files)
        else:
            tempcorpus = PlaintextCorpusReader(root=self.rootPath, fileids=l_files)

        corpusFreqDist = FreqDist(self.preprocessingClass.process(tempcorpus.words()))

        for wordColumn in self.df_data:
            dfreq = corpusFreqDist.get(wordColumn, 1)
            self.df_data[wordColumn] = self.df_data[wordColumn].map(lambda x: x / dfreq)

    def getID(self):
        return "TF-IDF"


#--------------------------------------------------------------------------------------
# TODO.
#--------------------------------------------------------------------------------------
class Text2TFIDFW(Text2TFIDF):
    def __init__(self, grouper, l_vocabulary=None, rootPath="", N=1, pClass=None, corpusReader=PlaintextCorpusReader):
        super(Text2TFIDFW, self).__init__(grouper=grouper, l_vocabulary=l_vocabulary, rootPath=rootPath, 
                    pClass=pClass, corpusReader=corpusReader)

        
        factors = [ (2.0/(N+1))*(1 - 2.0/(N+1))**i for i in range(N)]
        factors[0] = 1
        factors.reverse()

        #self.df_data[:10].to_csv(path_or_buf="./dataset_tfidf.csv")
        self.df_data.fillna(0, inplace=True)
        #'''
        ma = self.df_data.rolling(window=N).apply(lambda x: (x * factors).sum())
        #ma[:10].to_csv(path_or_buf="./dataset_ewtfidf.csv")
        self.df_data = ma.dropna(axis=0, how="all").copy()
        #'''

    def getID(self):
        return "EW-TF-IDF"

#--------------------------------------------------------------------------------------
# TODO.
#--------------------------------------------------------------------------------------
class Text2NGram():
    def __init__(self):
        return 

    def getID(self):
        return "NGram"