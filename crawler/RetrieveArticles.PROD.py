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
try:
    estadaoRegex = re.compile('.*(economia.estadao|politica.estadao).*', re.IGNORECASE)
    estadao = NPSpyderBR('estadao.com.br','http://www.estadao.com.br/', estadaoRegex)
    total += estadao.run()
    del estadao
    gc.collect()
except:
    logging.warn("Failed to capture estadao.com.br.")

# Build UOL
try:
    uolRegex = re.compile('.*(economia.uol|noticias.uol).*', re.IGNORECASE)
    uol = NPSpyderBR('uol.com.br','http://www.uol.com.br/', uolRegex)
    total += uol.run()
    del uol
    gc.collect()
except:
    logging.warn("Failed to capture uol.com.br.")

# Build UOL Noticias
#try:
#    uolRegex = re.compile('.*(economia.uol|noticias.uol).*', re.IGNORECASE)
#    uol = NPSpyderBR('uol.com.br','https://noticias.uol.com.br/', uolRegex)
#    total += uol.run()
#    del uol
#    gc.collect()
#
#    uolRegex = re.compile('.*(economia.uol|noticias.uol).*', re.IGNORECASE)
#    uol = NPSpyderBR('uol.com.br','https://economia.uol.com.br/', uolRegex)
#    total += uol.run()
#    del uol
#    gc.collect()
#except:
#    logging.warn("Failed to capture uol.com.br.")

# Build ADFVN
try:
    adfvnRegex = re.compile('.*', re.IGNORECASE)
    adfvn = NPSpyderBR('br.advfn.com','http://br.advfn.com/', adfvnRegex)
    total += adfvn.run()
    del adfvn
    gc.collect()
except:
    logging.warn("Failed to capture br.advfn.com.")

# Build G1
try:
    g1Regex = re.compile('.*(noticia|economia|brasil|politica).*', re.IGNORECASE)
    g1 = NPSpyderBR('g1.globo.com','http://g1.globo.com/', g1Regex)
    total += g1.run()
    del g1
    gc.collect()
except:
    logging.warn("Failed to capture g1.globo.com.")


# International
#--------------------------

# Build Bloomberg
try:
    bloombergRegex = re.compile('.*(articles).*', re.IGNORECASE)
    bloomberg = NPSpyder('bloomberg.com','http://www.bloomberg.com/', bloombergRegex)
    total += bloomberg.run()
    del bloomberg
    gc.collect()
except:
    logging.warn("Failed to capture bloomberg.com.")

# Build Reuters
try:
    reutersRegex = re.compile('.*(article).*', re.IGNORECASE)
    reuters = NPSpyder('reuters.com','http://www.reuters.com/', reutersRegex)
    total += reuters.run()
    del reuters
    gc.collect()
except:
    logging.warn("Failed to capture reuters.com.")

# Build The Guardian
try:
    theGuardianRegex = re.compile('.*', re.IGNORECASE)
    theGuardian = NPSpyder('theguardian.com','https://www.theguardian.com/', theGuardianRegex)
    total += theGuardian.run()
    del theGuardian
    gc.collect()
except:
    logging.warn("Failed to capture theguardian.com.")

# Build Nasdak
try:
    nasdakRegex = re.compile('.*', re.IGNORECASE)
    nasdak = NPSpyder('nasdaq.com','http://www.nasdaq.com/news/', nasdakRegex)
    total += nasdak.run()
    del nasdak
    gc.collect()
except:
    logging.warn("Failed to capture nasdaq.com.")

# Build Forbes
try:
    forbesRegex = re.compile('.*(www.forbes.com/|www.forbes.com.br/).*', re.IGNORECASE)
    forbes = NPSpyder('forbes.com','http://www.forbes.com/', forbesRegex)
    total += forbes.run()
    del forbes
    gc.collect()
except:
    logging.warn("Failed to capture forbes.com.")

# Build Investors
try:
    investorsRegex = re.compile('.*', re.IGNORECASE)
    investors = NPSpyder('investors.com','http://www.investors.com/news/', investorsRegex)
    total += investors.run()
    del investors
    gc.collect()
except:
    logging.warn("Failed to capture investors.com.")

# Build The Wall Street Journal
try:
    theStreetRegex = re.compile('.*(thestreet.com/story|thestreet.com/articles).*', re.IGNORECASE)
    theStreet = NPSpyder('thestreet.com','https://www.thestreet.com/', theStreetRegex)
    total += theStreet.run()
    del theStreet
    gc.collect()
except:
    logging.warn("Failed to capture thestreet.com.")

# Build The Economist
try:
    economistRegex = re.compile('.*(www.economist.com/news/).*', re.IGNORECASE)
    economist = NPSpyder('economist.com','http://www.economist.com/', economistRegex)
    total += economist.run()
    del economist
    gc.collect()
except:
    logging.warn("Failed to capture economist.com.")


# New Brazil spyders
#--------------------------

# Build Investing
try:
    brinvestingRegex = re.compile('.*(mercado|comunicado|indicadores-econ).*', re.IGNORECASE)
    brinvesting = NPSpyderBR('br.investing.com','https://br.investing.com/', brinvestingRegex)
    total += brinvesting.run()
    del brinvesting
    gc.collect()
except:
    logging.warn("Failed to capture br.investing.com.")

# Build Valor Economico
try:
    valorRegex = re.compile('.*', re.IGNORECASE)
    valor = NPSpyderBR('valor.com.br','http://www.valor.com.br/', valorRegex)
    total += valor.run()
    del valor
    gc.collect()
except:
    logging.warn("Failed to capture valor.com.br.")

# Build Exame
try:
    exameRegex = re.compile('.*(exame).abril.com.br.*', re.IGNORECASE)
    exame = NPSpyderBR('exame.abril.com.br','http://exame.abril.com.br/', exameRegex)
    total += exame.run()
    del exame
    gc.collect()
except:
    logging.warn("Failed to capture exame.abril.com.br.")

# Build Veja
try:
    vejaRegex = re.compile('.*(veja|vejasp|vejario|exame).abril.com.br.*', re.IGNORECASE)
    veja = NPSpyderBR('veja.abril.com.br','http://veja.abril.com.br/', vejaRegex)
    total += veja.run()
    del veja
    gc.collect()
except:
    logging.warn("Failed to capture veja.abril.com.br.")

# Build Ultimo Instante
try:
    uInstanteRegex = re.compile('.*', re.IGNORECASE)
    uInstante = NPSpyderBR('ultimoinstante.com.br','https://www.ultimoinstante.com.br/', uInstanteRegex)
    total += uInstante.run()
    del uInstante
    gc.collect()
except:
    logging.warn("Failed to capture ultimoinstante.com.br.")

# Build Infomoney
try:
    imoneyRegex = re.compile('.*', re.IGNORECASE)
    imoney = NPSpyderBR('infomoney.com.br','http://www.infomoney.com.br/', imoneyRegex)
    total += imoney.run()
    del imoney
    gc.collect()
except:
    logging.warn("Failed to capture infomoney.com.br.")

print "INFO - All feeders crawled, %d articles downloaded." %(total)
