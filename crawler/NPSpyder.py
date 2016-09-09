import newspaper
import re
from Data2File import getDataBasePath, article2file

class NPSpyder:

    # Initialize a source object defining the source website and the regex to filter articles
    # name: ID to be used to name folders etc.
    # sourceURL: Initial URL from where the spider will start to craw. Ex.: http://www.bloomberg.com/
    # regex: This regex will be applied to filter relevant URLs to be downloaded. Ex.: re.compile('.*(politics|economy).*', re.IGNORECASE)
    def __init__(self, name, sourceURL, regex):
        # Source`s name to create a path where data will be saved.
        self.sourceName = name

        # Setting preferences
        config = newspaper.Config()
        config.memoize_articles = True
        config.keep_article_html = False
        config.fetch_images = False
        config.language = 'en'

        # Building a Newspapper crawler...
        # defines the source website object from where the news are to be retrieved
        self.source = newspaper.build(sourceURL, config)

        # Define a regex to filter relevant article`s URLs
        self.filterRegex = regex


    # Will visit one by one of the articles available on the website, downloading pages that satisfies the filter regex
    def run(self):
        # Defining the path to save files
        path = getDataBasePath() + "/" + self.sourceName + "/"

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
            if self.filterRegex.match(str(article.url)):
                print "INFO - %s %.0f%% concluded, downloading URL: %s" %(self.sourceName, concluded, article.url)
                article.download()
                article.parse()
                article2file(article, path)
                counter += 1

        print "INFO - Done. %d out of %d articles saved to \"%s\"." %(counter, total, path)


    # Will visit and print all URLs available on the website without downloading.
    # Util to do the first analysis before defining the regex to filter and to evaluate the filter later.
    def visit(self):
        print("INFO - Visiting "+ self.sourceName +".")
        # Filtering relevant articles
        for article in self.source.articles:
            if self.filterRegex.match(str(article.url)):
                print "INFO - %s" %(article.url)
