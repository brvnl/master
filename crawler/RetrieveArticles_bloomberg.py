#!/usr/bin/python
import newspaper
import re
from Data2File import getDataBasePath, article2file


# Build a crawler
source = newspaper.build('http://www.bloomberg.com/', memoize_articles=False, language='en', fetch_images=False)

# Define a regex to filter relevant URLs
filterRegex = re.compile('.*(articles).*', re.IGNORECASE)

# Defining the path to save files
path = getDataBasePath() + "/bloomberg.com/"

print("INFO - Crawling bloomberg.com")

# Articles counter
counter = 0

# Filtering relevant articles
for article in source.articles:
    if filterRegex.match(str(article.url)):
        print("INFO - Downloading URL: " + article.url)
        article.download()
        article.parse()
        article2file(article, path)
        counter += 1

print "INFO - Done. %d articles saved to \"%s\"." %(counter, path)