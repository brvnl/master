from __future__ import division
from nltk.corpus import PlaintextCorpusReader
from nltk.probability import FreqDist

class ArticleCorpus:

    def __init__(self, rootPath, fileList):
        self.rootPath = rootPath
        self.files = fileList

    def buildVocabulary(self):
        self.corpus = PlaintextCorpusReader(self.rootPath, self.files)
        self.vocabulary = sorted(set(self.corpus.words()))
        return 0

    def printVocabulary(self):
        for word in self.vocabulary:
            print word
        return 0

    def countFrequenciesPerFile(self):
        self.fdist = {}
        for file in self.corpus.fileids():
            self.fdist[file] = FreqDist(self.corpus.words(file))
        return 0

    def printFrequenciesPerFile(self):
        print "INFO - Printing frequency distribution"
        #self.fdist.plot(50, cumulative=True)
        for file in self.corpus.fileids():
            print "INFO - File %s." %(file)
            for word in self.fdist[file]:
                print "%s: %d" %(word, self.fdist[file][word])
        return 0