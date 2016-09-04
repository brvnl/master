#!/usr/bin/python
import newspaper

# Build a Reuters crawler
google_source = newspaper.build('https://www.google.com.br/?gws_rd=ssl#tbm=nws&q=brazil+site:reuters.com')

# Navegating through source's articles:
for article in google_source.articles:
    print(article.url)
