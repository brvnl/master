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
