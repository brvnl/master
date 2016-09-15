#!/usr/bin/python
from tldextract.tldextract import LOG
from NPSpyder import NPSpyder
from NPSpyderBR import NPSpyderBR
import logging
import re
import gc

logging.basicConfig(level=logging.CRITICAL)
total = 0

# Brazil
#--------------------------

# Build Estadao
estadaoRegex = re.compile('.*(economia.estadao|politica.estadao).*', re.IGNORECASE)
estadao = NPSpyderBR('estadao.com.br','http://www.estadao.com.br/', estadaoRegex)
total += estadao.run()
gc.collect()

# Build UOL
uolRegex = re.compile('.*(economia.uol|noticias.uol).*', re.IGNORECASE)
uol = NPSpyderBR('uol.com.br','http://www.uol.com.br/', uolRegex)
total += uol.run()
gc.collect()

# Build ADFVN
adfvnRegex = re.compile('.*', re.IGNORECASE)
adfvn = NPSpyderBR('br.advfn.com','http://br.advfn.com/', adfvnRegex)
total += adfvn.run()
gc.collect()

# Build G1
g1Regex = re.compile('.*(noticia|economia|brasil|politica).*', re.IGNORECASE)
g1 = NPSpyderBR('g1.globo.com','http://g1.globo.com/', g1Regex, 1)
total += g1.run()
gc.collect()

# International
#--------------------------

# Build Bloomberg
bloombergRegex = re.compile('.*(articles).*', re.IGNORECASE)
bloomberg = NPSpyder('bloomberg.com','http://www.bloomberg.com/', bloombergRegex)
total += bloomberg.run()
gc.collect()

# Build Reuters
reutersRegex = re.compile('.*(article).*', re.IGNORECASE)
reuters = NPSpyder('reuters.com','http://www.reuters.com/', reutersRegex)
total += reuters.run()
gc.collect()

# Build The Guardian
theGuardianRegex = re.compile('.*', re.IGNORECASE)
theGuardian = NPSpyder('theguardian.com','https://www.theguardian.com/', theGuardianRegex)
total += theGuardian.run()
gc.collect()

# Build Nasdak
nasdakRegex = re.compile('.*', re.IGNORECASE)
nasdak = NPSpyder('nasdaq.com','http://www.nasdaq.com/news/', nasdakRegex)
total += nasdak.run()
gc.collect()

# Build Forbes
forbesRegex = re.compile('.*(www.forbes.com/|www.forbes.com.br/).*', re.IGNORECASE)
forbes = NPSpyder('forbes.com','http://www.forbes.com/', forbesRegex)
total += forbes.run()
gc.collect()

# Build Investors
investorsRegex = re.compile('.*', re.IGNORECASE)
investors = NPSpyder('investors.com','http://www.investors.com/news/', investorsRegex)
total += investors.run()
gc.collect()

# Build The Wall Street Journal
theStreetRegex = re.compile('.*(thestreet.com/story|thestreet.com/articles).*', re.IGNORECASE)
theStreet = NPSpyder('thestreet.com','https://www.thestreet.com/', theStreetRegex)
total += theStreet.run()
gc.collect()

# Build The Economist
economistRegex = re.compile('.*(www.economist.com/news/).*', re.IGNORECASE)
economist = NPSpyder('economist.com','http://www.economist.com/', economistRegex)
total += economist.run()
gc.collect()

print "INFO - All feeders crawled, %d articles downloaded." %(total)