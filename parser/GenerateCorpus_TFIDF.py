# -*- coding: utf-8 -*-
import sys, logging, os, csv
import numpy as np
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

from sklearn import tree
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import confusion_matrix
from parser.Definitions import Definitions
from financial.MonetaryReturn import MonetaryReturn
from classifiers.CorrCoefSummarization import CorrCoefSummarization

from parser.ArticlesFilter import ArticlesFilter
from parser.Definitions import Definitions
from parser.Representation import Text2TF
from parser.Representation import Text2TFIDF
from parser.Representation import Text2TFIDF_Salton88
from parser.ArticleOrganizer import GroupByDays
from parser.ArticleOrganizer import GroupByDaysRange
from parser.Preprocessing import ToLowerAlphaAndStopWords
from parser.Preprocessing import SteammingSnowBall
from parser.SerieLoaders import ExameSeriesLoader
from parser.SerieLoaders import UOLSeriesLoader
from parser.Definitions import Definitions
from parser.Returns import MultiplicativeReturns
from parser.Returns import AbsoluteMultiplicativeReturns
from parser.ReturnsToLabels import BinaryLabels
from parser.ReturnsToLabels import TernaryLabels
from parser.ReturnsToLabels import MagnitudeLabels
from parser.Dataset import BaseDataset
from parser.AttributeSelection import RemoveConstantAttributes
import numpy as np
import pandas as pd
import time


timestamp = time.strftime('%Y%m%d%H%M%S')
path = Definitions.TEST_RESULTS_PATH + "/Dataset_" + timestamp + "/"
os.makedirs(path)

formatter = logging.Formatter('%(asctime)s %(levelname)s* %(message)s')
logging.basicConfig(format='%(asctime)s %(levelname)s* %(message)s', 
                    level=logging.INFO)

logger = logging.getLogger("GenereteBinaryDataset")
hdl1 = logging.FileHandler("{0}{1}.log".format(path, "GenerateBinaryCorpus"))
hdl1.setFormatter(formatter)
logger.addHandler(hdl1)

logger.info("==============================XXX==============================")
logger.info("Binary Corpus generation: V1.0")
logger.info("==============================XXX==============================")

# SETUP DOCUMENTS DATA
logger.info("Retrieving documents")
feeders = [ "uol.com.br", ### BOM
            "br.advfn.com", ### BOM
            "estadao.com.br", ### BOM
            "g1.globo.com",  ### RUIM
            "valor.com.br", ### BOM
            "br.investing.com", ### BOM
            "exame.abril.com.br", ### BOM
            "infomoney.com.br", ### RUIM
            "ultimoinstante.com.br", ### BOM
            "veja.abril.com.br" ] ### BOM

#feeders = [ "ultimoinstante.com.br" ]

aFilter = ArticlesFilter(rootPath=Definitions.CORPUS_DATASET_BASE_PATH, feeders=feeders)
evaluation_feeders = ",".join(feeders)
aFilter.findArticles()
aFilter.filterDateRange(start='2016-08-01', end='2018-08-01')

logger.info("Organizing articles into buckets")
logger.info("  - GroupByDaysRange(CalBRLSP, 1)")
gp1 = GroupByDaysRange(aFilter.getFileList(), calendar=Definitions.CALENDARS_PATH + "/CalBRLSP.txt", days=1)
logger.info("  - GroupByDaysRange(CalBRLSP, 5)")
gp5 = GroupByDaysRange(aFilter.getFileList(), calendar=Definitions.CALENDARS_PATH + "/CalBRLSP.txt", days=5)
logger.info("  - GroupByDaysRange(CalBRLSP, 21)")
gp21 = GroupByDaysRange(aFilter.getFileList(), calendar=Definitions.CALENDARS_PATH + "/CalBRLSP.txt", days=21)

logger.info("Applying preprocessing and generating representation")
pp1 = ToLowerAlphaAndStopWords(stopwords=[])
pp2 = SteammingSnowBall(pprocess=pp1)

evaluation_preproc = pp2.getID()
fs = RemoveConstantAttributes()

logger.info("  - Text2TFIDF(gp1, RemoveConstantAttributes)")
X_11 = fs.process(attributes=Text2TFIDF_Salton88(grouper=gp1, rootPath="", pClass=pp2, corpusReader="FullCorpusReader").getData())
logger.info("Saving: \"%s\"." %(path+"tfidfs_ft_gp1_tas_rc.h5"))
X_11.to_hdf(path+"tfidfs_ft_gp1_tas_rc.h5", key="X")

logger.info("  - Text2TFIDF(gp5, RemoveConstantAttributes)")
X_15 = fs.process(attributes=Text2TFIDF_Salton88(grouper=gp5, rootPath="", pClass=pp2, corpusReader="FullCorpusReader").getData())
logger.info("Saving: \"%s\"." %(path+"tfidfs_ft_gp5_tas_rc.h5"))
X_15.to_hdf(path+"tfidfs_ft_gp5_tas_rc.h5", key="X")

logger.info("  - Text2TFIDF(gp21, RemoveConstantAttributes)")
X_121 = fs.process(attributes=Text2TFIDF_Salton88(grouper=gp21, rootPath="", pClass=pp2, corpusReader="FullCorpusReader").getData())
logger.info("Saving: \"%s\"." %(path+"tfidfs_ft_gp21_tas_rc.h5"))
X_121.to_hdf(path+"tfidfs_ft_gp21_tas_rc.h5", key="X")


logger.info("Done.")
hdl1.close()