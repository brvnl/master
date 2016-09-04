#!/usr/bin/python
import newspaper

# Build a folhasp crawler
estadao = newspaper.build('http://economia.estadao.com.br')

# Navegating through source's articles:
for article in estadao.articles:
    print(article.url)
