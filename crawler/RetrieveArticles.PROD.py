#!/usr/bin/python
from tldextract.tldextract import LOG
from NPSpyder import NPSpyder
from NPSpyderBR import NPSpyderBR
import logging
import re
import gc

logging.basicConfig(level=logging.CRITICAL)

# Brazil
#--------------------------

# Build Estadao
estadaoRegex = re.compile('.*(economia.estadao|politica.estadao).*', re.IGNORECASE)
estadao = NPSpyderBR('estadao.com.br','http://www.estadao.com.br/', estadaoRegex)
estadao.run()
gc.collect()

# Build UOL
uolRegex = re.compile('.*(economia.uol|noticias.uol).*', re.IGNORECASE)
uol = NPSpyderBR('uol.com.br','http://www.uol.com.br/', uolRegex)
uol.run()
gc.collect()

# Build ADFVN
adfvnRegex = re.compile('.*', re.IGNORECASE)
adfvn = NPSpyderBR('br.advfn.com','http://br.advfn.com/', adfvnRegex)
adfvn.run()
gc.collect()


# International
#--------------------------

# Build Bloomberg
bloombergRegex = re.compile('.*(articles).*', re.IGNORECASE)
bloomberg = NPSpyder('bloomberg.com','http://www.bloomberg.com/', bloombergRegex)
bloomberg.run()
gc.collect()

# Build Reuters
reutersRegex = re.compile('.*(article).*', re.IGNORECASE)
reuters = NPSpyder('reuters.com','http://www.reuters.com/', reutersRegex)
reuters.run()
gc.collect()

# Build The Guardian
theGuardianRegex = re.compile('.*', re.IGNORECASE)
theGuardian = NPSpyder('theguardian.com','https://www.theguardian.com/', theGuardianRegex)
theGuardian.run()
gc.collect()

# Build Nasdak
nasdakRegex = re.compile('.*', re.IGNORECASE)
nasdak = NPSpyder('nasdaq.com','http://www.nasdaq.com/news/', nasdakRegex)
nasdak.run()
gc.collect()

# Build Forbes
forbesRegex = re.compile('.*(www.forbes.com/|www.forbes.com.br/).*', re.IGNORECASE)
forbes = NPSpyder('forbes.com','http://www.forbes.com/', forbesRegex)
forbes.run()
gc.collect()

# Build Investors
investorsRegex = re.compile('.*', re.IGNORECASE)
investors = NPSpyder('investors.com','http://www.investors.com/news/', investorsRegex, 1)
investors.run()
gc.collect()

# Build The Wall Street Journal
theStreetRegex = re.compile('.*(thestreet.com/story|thestreet.com/articles).*', re.IGNORECASE)
theStreet = NPSpyder('thestreet.com','https://www.thestreet.com/', theStreetRegex, 1)
theStreet.run()