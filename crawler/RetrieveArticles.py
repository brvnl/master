#!/usr/bin/python
from tldextract.tldextract import LOG
from NPSpyder import NPSpyder
from NPSpyderBR import NPSpyderBR
import logging
import re

logging.basicConfig(level=logging.CRITICAL)

# International
#--------------------------

# Build Bloomberg
bloombergRegex = re.compile('.*(articles).*', re.IGNORECASE)
bloomberg = NPSpyder('bloomberg.com','http://www.bloomberg.com/', bloombergRegex)
bloomberg.run()

# Build Reuters
reutersRegex = re.compile('.*(article).*', re.IGNORECASE)
reuters = NPSpyder('reuters.com','http://www.reuters.com/', reutersRegex)
reuters.run()

# Build The Guardian
theGuardianRegex = re.compile('.*', re.IGNORECASE)
theGuardian = NPSpyder('theguardian.com','https://www.theguardian.com/', theGuardianRegex)
theGuardian.run()


# Brazil
#--------------------------

# Build Estadao
estadaoRegex = re.compile('.*(economia.estadao|politica.estadao).*', re.IGNORECASE)
estadao = NPSpyderBR('estadao.com.br','http://www.estadao.com.br/', estadaoRegex)
estadao.run()

# Build UOL
uolRegex = re.compile('.*(economia.uol|noticias.uol).*', re.IGNORECASE)
uol = NPSpyderBR('uol.com.br','http://www.uol.com.br/', uolRegex)
uol.run()

# Build ADFVN
adfvnRegex = re.compile('.*', re.IGNORECASE)
adfvn = NPSpyderBR('br.advfn.com','http://br.advfn.com/', adfvnRegex)
adfvn.run()

