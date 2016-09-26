from __future__ import division
from nltk.corpus import PlaintextCorpusReader
import nltk, re, pprint
from ArticleCorpus import ArticleCorpus

corpus_root = '/Volumes/REPOSITORY/Mestrado/Thesis/data/economist.com/'
files = ['20160924000000.Sangfroidcity.txt', \
         '20160924000000.Indecisiontime.txt', \
         '20160922144408.LittleLondons.txt', \
         '20160922144407.Millennialfalcon.txt']

aCorpus = ArticleCorpus(corpus_root, files)
aCorpus.buildVocabulary()
#aCorpus.printVocabulary()
aCorpus.countFrequenciesPerFile()
aCorpus.printFrequenciesPerFile()