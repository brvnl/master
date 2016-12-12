import shlex, subprocess
from collections import defaultdict

class ArticlesFilter:

    def __init__(self, rootPath, keyWordsList=None, negativeKeywordsList=None):
        self.rootPath = rootPath
        self.date2feeder2article = defaultdict(dict)
        self.fileList = []

        if keyWordsList is not None:
            self.keywords = "|".join(keyWordsList)
        else:
            self.keywords = ""

        if negativeKeywordsList is not None:
            self.nkeywords = "|".join(negativeKeywordsList)
        else:
            self.nkeywords = ""

    def findArticles(self):
        # Command line grep to retrieve files matching the regex in theur content

        if (self.keywords != "") & (self.nkeywords != ""):
            # Ex.: grep -L -E "(Bovespa|Brazil)" `grep -l -r -E "(ITUB4)" *`
            print "DEBUG* Both positive and negative keywords provided.\n"
            command = 'grep -L -E \"' + self.nkeywords + '\" `grep -l -r -E \"' + self.keywords + '\" ' + self.rootPath + '`'
            p = subprocess.Popen(["/bin/bash", "-c", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif (self.keywords != ""):
            print "DEBUG* Only positive keywords provided.\n"
            p = subprocess.Popen(["grep", "-l", "-r", "-E", self.keywords, self.rootPath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif (self.nkeywords != ""):
            print "DEBUG* Only negative keywords provided.\n"
            p = subprocess.Popen(["grep", "-L", "-r", "-E", self.nkeywords, self.rootPath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        self.fileList = iter(p.stdout.readline, b'')

    def printRawFileList(self):
        for file in self.fileList:
            print file

    def files2hash(self):
        for file in self.fileList:
            file = file.rstrip("\n\r")
            file = file.rstrip("\n")

            # Expecting file path as the example below:
            # /Volumes/Repository/Mestrado/Data/uol.com.br/20160210000000.BreakingNews.txt
            paths = file.split("/")

            if (len(paths) < 2):
                continue

            fileName = paths.pop()
            timestamp = fileName.split(".")[0]
            feeder = paths.pop()
            self.date2feeder2article[timestamp][feeder] = file

    def printFilesDetails(self):
        for timestamp in sorted(self.date2feeder2article):
            for feeder in sorted(self.date2feeder2article[timestamp]):
                print "INFO - timestamp=%s, feeder=%s, file=%s." %(timestamp, feeder, self.date2feeder2article[timestamp][feeder])
