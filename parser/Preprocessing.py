# encoding=utf8
from unicodedata import normalize 
from nltk.corpus import stopwords
from nltk.stem.rslp import RSLPStemmer
import snowballstemmer
from multiprocessing import Pool
from multiprocessing import cpu_count
import logging

#--------------------------------------------------------------------------------------
# This file contains functions used for different types of preprocessing transformations, 
# including steaming, case normalization and so forth.
# All the functions receives a list a of words and returns a processed list.
# For optimizing purposes, since some of the transformation may be applied together ins
# tead of in sequence, the functions may apply more than one transformations at one time.
#--------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------
# Auxiliar:
#--------------------------------------------------------------------------------------
def getVocabulary(rawWordList):
    return sorted(list(set(rawWordList)))

def splitList(rawWordList, n):
    csize = len(rawWordList) / n
    chunks = [rawWordList[x:x+csize] for x in xrange(0, len(rawWordList), csize)]
    return chunks

def removeSpecialChars(str):
    return normalize("NFKD", str).encode("ASCII", 'ignore').decode('ASCII')

##=====================================================================================
## Word level:
##=====================================================================================
#--------------------------------------------------------------------------------------
# Basic:
#--------------------------------------------------------------------------------------
class BaseProcessing(object):
    def __init__(self, pprocess=None):
        self.pprocessing = pprocess
        self.id = ""

    def process(self, rawWordList):
        if (self.pprocessing is None):
            return rawWordList
        else:
            return self.pprocessing.process(rawWordList)

    def getID(self):
        if (self.pprocessing is None):
            return self.id
        else:
            return self.pprocessing.getID() + "-" + self.id
        


class ToLowerAlphaAndStopWords(BaseProcessing):
    def __init__(self, pprocess=None, stopwords=None):

        super(ToLowerAlphaAndStopWords, self).__init__(pprocess)
        self.id = "LAS"

        if (stopwords is None):
            self.stopwords = stopwords.words('portuguese')
        else:
            self.stopwords = stopwords

    def process(self, rawWordList):
        wordList = super(ToLowerAlphaAndStopWords, self).process(rawWordList)
        #pontuationFilteredWordList = [ removeSpecialChars(w.lower()) for w in wordList if (w.isalpha()) and (w.lower() not in self.stopwords)]
        pontuationFilteredWordList = [ removeSpecialChars(w.lower()) for w in wordList if w.isalpha() ]
        pontuationFilteredWordList = [ w for w in pontuationFilteredWordList if w.lower() not in self.stopwords ]

        return pontuationFilteredWordList

#--------------------------------------------------------------------------------------
# Radical extraction:
#--------------------------------------------------------------------------------------
class SteammingNLTK(BaseProcessing):
    def __init__(self, pprocess=None):
        super(SteammingNLTK, self).__init__(pprocess)
        self.id = "SNLTK"

    def process(self, rawWordList):
        wordList = super(SteammingNLTK, self).process(rawWordList)

        stemmer = RSLPStemmer()
        steammedWordList = [stemmer.stem(w) for w in wordList]

        return steammedWordList

class SteammingSnowBall(BaseProcessing):
    def __init__(self, pprocess=None):
        super(SteammingSnowBall, self).__init__(pprocess)
        self.id = "SSnow"

    def process(self, rawWordList):
        wordList = super(SteammingSnowBall, self).process(rawWordList)
        stemmer = snowballstemmer.stemmer('portuguese')
        steammedWordList = stemmer.stemWords(wordList)

        return steammedWordList

#--------------------------------------------------------------------------------------
# Semantics:
#--------------------------------------------------------------------------------------
class WordExpansion(BaseProcessing):
    def __init__(self, pprocess=None):
        super(WordExpansion, self).__init__(pprocess)
        self.id = "WExp"

    def process(self, rawWordList):
        wordList = super(WordExpansion, self).process(rawWordList)
        return wordList