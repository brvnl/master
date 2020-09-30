import shlex, subprocess, re
from collections import defaultdict
import os.path
import datetime
import ntpath
import pandas as pd
import sys
import glob
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from multiprocessing import Process
from multiprocessing import Pool
from multiprocessing import Manager
from multiprocessing import cpu_count
import logging

def computeParallelFind(rootpath, regex):
    returnList = glob.glob(rootpath + regex)
    
    #print("*DEBUG - Total files captured: \"%d\"." %(len(returnList)))
    return returnList


def findParallel(rp, feeders=[]):

    np = cpu_count()
    p = Pool(processes=np)
    regex = '/*/*.txt'

    # Optimizing parallel processing:
    #   - If all feeders are supposed to be considered, get all the feeders paths and distribute it to the workers.
    #   - If a subset of feeders is selected, do the find only on them.
    #   - If the number of feeders is smaller than the number of workers, distribute it one level upper.
    if not feeders:
        subpaths = glob.glob(rp + '/*')
        #print("*DEBUG - All feeders.")
    else:
        subpaths = [ rp + "/" + feeder for feeder in feeders ]
        #print("*DEBUG - Feeders subset.")

        if len(subpaths) < np: 
        #    #print("*DEBUG - Decomposing feeders.")
            decomposedFeeders = []
            for feeder in subpaths:
                decomposedFeeders.extend(glob.glob(feeder + '/*'))

            subpaths = decomposedFeeders
            regex = '/*.txt'

    #for path in subpaths:
        #print("*DEBUG - %s" %(path))

    results = [ p.apply_async(computeParallelFind, args=(paths,regex)) for paths in subpaths ]
    returnlist = []
    for r in results:
        returnlist += r.get()

    p.close()
    p.terminate()

    return returnlist

def getTimeFromPath(path):
    filename = path.rstrip("\n\r")
    filename = filename.rstrip("\n")

    # Default value if not able to parse
    timestamp = "9999-12-31"

    # Expecting file path as the example below:
    # /Volumes/Repository/Mestrado/Data/uol.com.br/20160210000000BreakingNews.txt
    paths = filename.split("/")

    if (len(paths) < 2):
        return timestamp

    filename = paths.pop()
    try:
        #logging.info("Trying to parse \"%s\"." %(filename[:14]))
        timestamp = datetime.datetime.strptime(filename[:14], '%Y%m%d%H%M%S').strftime('%Y-%m-%d')
    except:
        logging.warn("Cannot evaluate timestamp on file \"%s\". Setting default \"%s\"." %(filename, timestamp))

    return timestamp


class ArticlesFilter:

    def __init__(self, rootPath, keyWordsList=None, negativeKeywordsList=None, feeders=None):
        self.logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(format='%(asctime)s %(levelname)s* %(message)s', level=logging.INFO)

        self.rootPath = rootPath
        self.date2feeder2article = defaultdict(dict)
        self.fileList = pd.DataFrame({'file':[]})

        self.logger.info("Using articles root path: %s." %(self.rootPath))

        if (keyWordsList is not None) and (keyWordsList):
            self.keywords = "|".join(keyWordsList)
            self.logger.info("Positive keywords list: %s." %(self.keywords))
        else:
            self.keywords = ""

        if (negativeKeywordsList is not None) and (keyWordsList):
            self.nkeywords = "|".join(negativeKeywordsList)
            self.logger.info("Negative keywords list: %s." %(self.nkeywords))
        else:
            self.nkeywords = ""

        self.feeders = feeders
        self.logger.info("Feeders list: %s." %("|".join(self.feeders)))

    def findArticles(self):
        # Command line grep to retrieve files matching the regex in theur content

        if (self.keywords != "") & (self.nkeywords != ""):
            # Ex.: grep -L -E "(Bovespa|Brazil)" `grep -l -r -E "(ITUB4)" *`
            #print("*DEBUG - Running find with positive and negative keywords.")
            command = 'grep -L -E \"' + self.nkeywords + '\" `grep -l -r -E \"' + self.keywords + '\" ' + self.rootPath + '`'
            p = subprocess.Popen(["/bin/bash", "-c", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif (self.keywords != ""):
            #print("*DEBUG - Running find with positive keywords.")
            p = subprocess.Popen(["grep", "-l", "-r", "-E", self.keywords, self.rootPath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif (self.nkeywords != ""):
            #print("*DEBUG - Running find with negative keywords.")
            p = subprocess.Popen(["grep", "-L", "-r", "-E", self.nkeywords, self.rootPath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            #print("*DEBUG - Running find parallel.")
            rawFileList = findParallel(self.rootPath, feeders=self.feeders)

            # find /Volumes/MESTRADO/implementation/data -name "*.txt"
            #p = subprocess.Popen(["find", self.rootPath, "-name", "*.txt"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            #rawFileList = glob.glob(self.rootPath + '/*/*/*.txt')


        if (self.keywords != "") | (self.nkeywords != ""):
            rawFileList = iter(p.stdout.readline, b'')
            rawFileList = [s.rstrip("\n\r").rstrip("\n") for s in rawFileList]
            #rawFileList = [s.rstrip("\n\r") for s in rawFileList]
            #rawFileList = [s.rstrip("\n")   for s in rawFileList]

        if self.feeders:
            feedersRgx = re.compile("|".join(self.feeders))
            rawFileList = [s for s in rawFileList if (re.search(feedersRgx,s)) and (os.path.isfile(s))]
            #rawFileList = [s for s in rawFileList if re.search(feedersRgx,s)]

        self.fileList = pd.DataFrame({'file':rawFileList})
        self.fileList["date"] = self.fileList['file'].apply(lambda row: getTimeFromPath(row))
        self.fileList['date'] = pd.to_datetime(self.fileList['date'], format='%Y-%m-%d')
        self.fileList.set_index('date', inplace=True)
        self.fileList.sort_index(inplace=True)

        self.logger.info("Files retrieved by the filter: %d." %( len(self.fileList.index)))
        #self.fileList = [s for s in rawFileList if ]

    def files2hash(self):
        l_datecolumn = []
        l_feedercolumn = []
        l_filecolumn = []

        for file in self.fileList['file']:

            # Expecting file path as the example below:
            # /Volumes/Repository/Mestrado/Data/uol.com.br/20160210000000.BreakingNews.txt
            paths = file.split("/")

            if (len(paths) < 2):
                continue

            fileName = paths.pop()
            
            # Extract "20160210" from ""20160210000000.BreakingNews.txt"
            date = fileName[:8]
            
            feeder = paths.pop()
            feeder = paths.pop()
            
            #print "*DEBUG - %s, %s, %s" %(date, feeder, file)
            l_datecolumn.append(date)
            l_feedercolumn.append(feeder)
            l_filecolumn.append(file)
            
            #try:
            #    self.date2feeder2article[date][feeder].append(file)
            #except:
            #    self.date2feeder2article[date][feeder] = [file]

        # Convert lists to pandas dataframe
        self.date2feeder2article = pd.DataFrame({
            'date': l_datecolumn,
            'feeder': l_feedercolumn,
            'file': l_filecolumn
        })
    
    def filterDateRange(self, start, end):
        try:
            self.logger.info("Filtering files from \"%s\" to \"%s\"." %(start, end))
            self.fileList = self.fileList.loc[start:end]
            return 0
        except:
            self.logger.warn("Unable to filter file list with \"%s\" as start and \"%s\" as end." %(start, end))
            return 1

    def printRawFileList(self):
        for file in self.fileList['file']:
            print file

    def getFilesDetails(self):
        return self.date2feeder2article

    def printFilesDetails(self):
        print(self.date2feeder2article.to_string())
                
    def printFilesDetailsCSV(self):
        self.date2feeder2article.to_csv(sys.stdout)
                
    def printDailyCount(self):
        df = self.date2feeder2article.groupby(['date','feeder'])['file'].count()\
               .reset_index(name="count") \
               .reindex(columns=['date', 'feeder', 'count'])

        dfp = df.pivot(index='date', columns='feeder', values='count')
        print(dfp.to_string())

    def plotDailyCount(self, start=None, end=None, total=False, totalonly=False):
        df = self.date2feeder2article

        # Filtering
        if (not ((start is None) | (end is None))):
            dff = df.loc[df.date.between(left=start, right=end)]
        else:
            dff = df

        # Counting 
        dfc = dff.groupby(['date','feeder'])['file'].count()\
               .reset_index(name="count") \
               .reindex(columns=['date', 'feeder', 'count'])

        # Pivoting
        dfp = dfc.pivot(index='date', columns='feeder', values='count')

        if (total | totalonly):
            dfp['total'] = (pd.Series(dfp.sum(axis=1),name='total'))

        if (totalonly):
            dfp = dfp['total']
            dfp.index = pd.to_datetime(dfp.index)

        # Casting index to date format
        dfp.index = pd.to_datetime(dfp.index)

        #print(dfp.to_string())
        #print(dfp.describe())
        #print(dfp.dtypes)

        # Plotting
        ax = dfp.plot(title="Number of Articles", use_index=True, rot=45, sharex=True, grid=True, fontsize=5)
        #ax.set(xticks=range(dfp.index), xticklabels=dfp.index)

        #ax.autoscale(enable=False, axis='x')

        #ax.set_xticks(dfp.index)
        #ax.set_xticks(ax.get_xticks()[::7])
        #ax.set_xticklabels(xt)
        
        #ax.set_xlim(start, end)
        #ax.set_xlim(dfp.index.min(), dfp.index.max())
        #ax.tick_params(axis='both', which='major', labelsize=5)

        #ax.figure.autofmt_xdate()
        
        ax.xaxis.set_major_locator(mdates.WeekdayLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%a %Y%m%d'))
        plt.legend(fontsize="xx-small")

        plt.show()

    def printDailyCountCSV(self):
        df = self.date2feeder2article.groupby(['date','feeder'])['file'].count()\
               .reset_index(name="count") \
               .reindex(columns=['date', 'feeder', 'count'])

        dfp = df.pivot(index='date', columns='feeder', values='count')
        dfp.to_csv(sys.stdout)

    def getTitlesTimeSeries(self):
        l_datecolumn = []
        l_titlecolumn = []

        newts = {}
        for file in self.fileList['file']:
            file = file.rstrip("\n\r")
            file = file.rstrip("\n")

            # Expecting file path as the example below:
            # /Volumes/Repository/Mestrado/Data/uol.com.br/20160210000000.BreakingNews.txt
            paths = file.split("/")

            if (len(paths) < 2):
                continue

            fileName = paths.pop()
            timestamp = datetime.datetime.strptime(fileName[:14], '%Y%m%d%H%M%S').strftime('%Y-%m-%d')
            feeder = paths.pop()
            feeder = paths.pop()

            with open(file, "r") as article:
                # First read the URL ...
                title = article.readline()
                # ... then read the title
                title = article.readline()

            title = title.rstrip("\n\r")
            title = title.rstrip("\n")

            l_datecolumn.append(timestamp)
            l_titlecolumn.append(title)

        newts = pd.DataFrame({
            'date': l_datecolumn,
            'title': l_titlecolumn
        })

        return newts

    def getFileList(self):
        return self.fileList['file']

    def getFileListSize(self):
        return len(self.fileList['file'])

    def getFileNames(self):
        filenames = [ntpath.basename(file) for file in self.fileList['file']]
        return filenames
    