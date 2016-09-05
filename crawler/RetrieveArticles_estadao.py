#!/usr/bin/python
import newspaper
import re
from Data2File import getDataBasePath, article2file


# Build a estadao crawler
estadao = newspaper.build('http://www.estadao.com.br/', memoize_articles=False, language='pt', fetch_images=False)

# Define a regex to filter relevant URLs
filterRegex = re.compile('.*(economia.estadao|politica.estadao).*', re.IGNORECASE)

# Defining the path to save files
path = getDataBasePath() + "/estadao.com.br/"

print("INFO - Crawling estadao.com.br")

# Articles counter
counter = 0
visited = 0
concluded = 0
total = source.size()

# Filtering relevant articles
for article in estadao.articles:
    visited += 1
    concluded = (visited / total) * 100
    if filterRegex.match(str(article.url)):
        print "INFO - %.0f%%, Downloading URL: %s" %(concluded, article.url)
        article.download()
        article.parse()
        article2file(article, path)
        counter += 1

print "INFO - Done. %d articles saved to \"%s\"." %(counter, path)