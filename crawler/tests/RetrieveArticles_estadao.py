#!/usr/bin/python
import newspaper
import re
import time
from newspaper import Article

# Prints article's data into a file whichs filename consists of timestamp and title.
def article2file( aArticle ):
    # Extracts only the first 100 chars
    title4name = aArticle.title[:100]
    title4name = title4name.replace(" ", "")
    title4name = title4name.replace(",", "")

    try:
        date4name = aArticle.publish_date.strftime('%Y%m%d%H%M%S')
    except:
        # If cannot retrieve publish date defaults to the day it has been captured
        date4name = time.strftime('%Y%m%d000000', time.gmtime())

    path = './'
    filename = path + date4name + '.' + title4name + '.txt'
    text_file = open(filename, "w")
    text_file.write("%s" % aArticle.text.encode('utf-8'))
    text_file.close()
    return 0


# Build a estadao crawler
estadao = newspaper.build('http://www.estadao.com.br/', memoize_articles=False)

# Define a regex to filter relevant URLs
filterRegex = re.compile('.*(economia.estadao|politica.estadao).*', re.IGNORECASE)

# Filtering relevant articles
for article in estadao.articles:
    if filterRegex.match(str(article.url)):
        print("Downloading URL: " + article.url)
        article.download()
        article.parse()
        article2file(article)