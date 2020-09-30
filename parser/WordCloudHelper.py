# encoding=utf8
from __future__ import division
from wordcloud import WordCloud, STOPWORDS
import logging
import matplotlib.pyplot as plt
#from parser.ArticleCorpus import ArticleCorpus
from nltk.corpus import PlaintextCorpusReader
from parser.CustomCorpusReaders import TitleCorpusReader
from parser.CustomCorpusReaders import FullCorpusReader
from parser.CustomCorpusReaders import BodyCorpusReader
from parser.Preprocessing import toLowerAlphaAndStopWords
from nltk.corpus import stopwords
from nltk.probability import FreqDist

# Main class
#----------------------
class WordCloudHelper:

    # CONSTRUCTOR
    #----------------------
    def __init__(self, aFilter):
        self.filter = aFilter
        self.logger = logging.getLogger('WordCloudHelper')
        self.stopwords = stopwords.words('portuguese')

        logging.basicConfig(format='%(asctime)s %(levelname)s* %(message)s', level=logging.INFO)


    def setStopWords(self, l_stopwords):
        self.stopwords = l_stopwords


    def _getData(self):
        self.filter.findArticles()
        flist = self.filter.getFileList().values.tolist()

        print("*DEBUG - Number of files: %d." %(len(flist)))

        tempcorpus = TitleCorpusReader("", flist)
        #tempcorpus = PlaintextCorpusReader("", flist)
        #tempcorpus = FullCorpusReader("", flist)
        #tempcorpus = BodyCorpusReader("", flist)

        print("*DEBUG - Word Counter Original: %d." %(len(tempcorpus.words())))
        #processedWords = tempcorpus.words()
        processedWords = toLowerAlphaAndStopWords(tempcorpus.words())

        print("*DEBUG - Word Counter Processed: %d." %(len(processedWords)))
        self.thedata = FreqDist(processedWords)


    def showWordCloud(self, mwords=10):
        self._getData()

        wc = WordCloud(
            width=800,
            height=400,
            background_color='white',
            max_words=mwords,
            stopwords=self.stopwords
        )

        wc.generate_from_frequencies(self.thedata)
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        #plt.show()



