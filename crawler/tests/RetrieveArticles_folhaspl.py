#!/usr/bin/python
import newspaper

# Build a folhasp crawler
folhasp = newspaper.build('http://www.folha.uol.com.br/')

# Navegating through source's articles:
for article in folhasp.articles:
    print(article.url)
