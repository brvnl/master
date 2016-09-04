#!/usr/bin/python
import newspaper
import re

listOfWords = ['http://economia.estadao.com.br/noticias/negocios,campanha-fala-de-talento-e-nao-em-deficiencia,10000072608',
			   'http://emais.estadao.com.br/noticias/moda-beleza,estrelas-de-hollywood-posam-para-calendario-pirelli-2017,10000072734',
			   'http://publicidade.estadao.com.br/pay-made-order-essay-experienced-authors/']
			   
filterRegex = re.compile('.*(economia|publicidade).*', re.IGNORECASE)

# Filtering relevant articles
for article in listOfWords:
	if filterRegex.match(str(article)):
		print(article)
		#articlesOfInterest.append(article)

# Printing filtered articles
#for article in articlesOfInterest.articles:
#	print(article.url)