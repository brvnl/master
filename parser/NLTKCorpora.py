from __future__ import division
from nltk.corpus import PlaintextCorpusReader 
import nltk, re, pprint

corpus_root = '/Volumes/REPOSITORY/Mestrado/Thesis/data/economist.com/'
corpus_file = '20160924000000.Thelow-rateworld.txt'
full_path = corpus_root + corpus_file

#wordlists = PlaintextCorpusReader(corpus_root, corpus_file)
#print wordlists.fileids()

raw = open(full_path).read()
tokens = nltk.word_tokenize(raw)
words = [w.lower() for w in tokens]
vocab = sorted(set(words))

print vocab