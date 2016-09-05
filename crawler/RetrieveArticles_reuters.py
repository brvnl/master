#!/usr/bin/python
import newspaper
import re
from Data2File import getDataBasePath, article2file


# Build a crawler
source = newspaper.build('http://www.reuters.com/', memoize_articles=False, language='en', fetch_images=False)

# Define a regex to filter relevant URLs
filterRegex = re.compile('.*(article).*', re.IGNORECASE)

# Defining the path to save files
path = getDataBasePath() + "reuters.com/"

print("INFO - Crawling reuters.com")

# Articles counter
counter = 0
visited = 0
concluded = 0
total = source.size()

# Filtering relevant articles
for article in source.articles:
    visited += 1
    concluded = (visited / total) * 100
    if filterRegex.match(str(article.url)):
        print "INFO - %.0f%%, Downloading URL: %s" %(concluded, article.url)
        article.download()
        article.parse()
        article2file(article, path)
        counter += 1

print "INFO - Done. %d articles saved to \"%s\"." %(counter, path)