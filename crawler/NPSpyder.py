from __future__ import print_function
import traceback
import newspaper
import re
import time
from Data2File import getDataBasePath, article2file

class NPSpyder:

    # Initialize a source object defining the source website and the regex to filter articles
    # name: ID to be used to name folders etc.
    # sourceURL: Initial URL from where the spider will start to craw. Ex.: http://www.bloomberg.com/
    # regex: This regex will be applied to filter relevant URLs to be downloaded. Ex.: re.compile('.*(politics|economy).*', re.IGNORECASE)
    def __init__(self, name, sourceURL, regex, firstRun=0):
        # Source`s name to create a path where data will be saved.
        self.sourceName = name

        # Building a Newspapper crawler...
        # defines the source website object from where the news are to be retrieved
        if (firstRun == 1):
            self.source = newspaper.build(sourceURL, language='en', fetch_images=False, memoize_articles=False)
        else:
            self.source = newspaper.build(sourceURL, language='en', fetch_images=False)

        # Define a regex to filter relevant article`s URLs
        self.filterRegex = regex


    # Will visit one by one of the articles available on the website, downloading pages that satisfies the filter regex
    def run(self):
        # Defining the path to save files
        basepath = getDataBasePath() + "/" + self.sourceName + "/"
        start_time = time.time()

        print("INFO - Crawling "+ self.sourceName +".")

        # Progress controlers
        counter = 0
        visited = 0
        concluded = 0
        total = self.source.size()

        # Filtering relevant articles
        for article in self.source.articles:
            visited += 1
            concluded = (float(visited) / total) * 100

            # Complementing the paht with the month folder: yyyyMM
            try:
                path = basepath + article.publish_date.strftime('%Y%m') + "/"
            except:
                # If cannot retrieve publish date defaults to the day it has been captured
                path = basepath + time.strftime('%Y%m', time.gmtime()) + "/"

            try:
                if self.filterRegex.match(str(article.url)):
                    print("INFO - %s %.0f%% concluded, downloading URL: %s" %(self.sourceName, concluded, article.url))
                    article.download()
                    article.parse()
                    article2file(article, path)
                    counter += 1
            except:
                # Common exception is special char on URL, try to recover by removing special chars before capture
                try:
                    theURL = re.sub('\W+','', article.url)
                    if self.filterRegex.match(str(theURL)):
                        print("INFO - %s %.0f%% concluded, downloading URL: %s" %(self.sourceName, concluded, article.url))
                        article.download()
                        article.parse()
                        article2file(article, path)
                        counter += 1

                except:
                    print("WARN - Cannot apply filter due to special char in URL: %s" %(article.url))
                    traceback.print_exc()

        print("INFO - Done. %d out of %d articles saved to \"%s\"." %(counter, total, path))
        elapsed_time = time.time() - start_time
        print("INFO - %s crawled in %d seconds." %(self.sourceName, elapsed_time))
        return counter


    # Will visit and print all URLs available on the website without downloading.
    # Util to do the first analysis before defining the regex to filter and to evaluate the filter later.
    def visit(self):
        print("INFO - Visiting "+ self.sourceName +".")
        # Filtering relevant articles
        for article in self.source.articles:
            try:
                if self.filterRegex.match(str(article.url)):
                    print("INFO - %s" %(article.url))
            except:
                # Common exception is special char on URL, try to recover by removing special chars before capture
                try:
                    theURL = re.sub('\W+','', article.url)
                    if self.filterRegex.match(str(theURL)):
                        print("INFO - %s" %(article.url))

                except:
                    print("WARN - Cannot apply filter due to special char in URL: %s" %(article.url))
        return 0
