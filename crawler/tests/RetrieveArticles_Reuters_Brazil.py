#!/usr/bin/python
import newspaper

# Build a Reuters crawler
reuters = newspaper.build('http://www.reuters.com/places/brazil')

# Navegating through source's articles:
for article in reuters.articles:
    print(article.url)
