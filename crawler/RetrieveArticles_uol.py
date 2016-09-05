#!/usr/bin/python
import newspaper
import re
from Data2File import getDataBasePath, article2file


# Build a uol crawler
uol = newspaper.build('http://www.uol.com.br/', memoize_articles=False, language='pt', fetch_images=False)

# Define a regex to filter relevant URLs
filterRegex = re.compile('.*(economia.uol|noticias.uol).*', re.IGNORECASE)


# Defining the path to save files
path = getDataBasePath() + "/uol.com.br/"

print("INFO - Crawling uol.com.br")

# Articles counter
counter = 0

# Filtering relevant articles
for article in uol.articles:
    if filterRegex.match(str(article.url)):
        print("INFO - Downloading URL: " + article.url)
        article.download()
        article.parse()
        article2file(article, path)
        counter += 1

print "INFO - Done. %d articles saved to \"%s\"." %(counter, path)