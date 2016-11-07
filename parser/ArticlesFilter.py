import shlex, subprocess
from collections import defaultdict

class ArticlesFilter:

    def __init__(self, rootPath, keyWordsList):
        self.rootPath = rootPath
        # Will produce a string on the form pattern1|pattern2|pattern3...
        self.keywords = "|".join(keyWordsList)
        self.date2feeder2article = defaultdict(dict)
        self.fileList = []

    def findArticles(self):
        # Command line grep to retrieve files matching the regex in theur content
        p = subprocess.Popen(["grep", "-l", "-r", "-E", self.keywords, self.rootPath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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