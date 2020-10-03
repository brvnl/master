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

# Build Estadao: Working, last revision on 02/10/2020
try:
    estadaoRegex = re.compile('.*(economia.estadao|politica.estadao).*', re.IGNORECASE)
    estadao = NPSpyderBR('estadao.com.br','http://www.estadao.com.br/', estadaoRegex)
    total += estadao.run()
    del estadao
    gc.collect()
except:
    logging.warn("Failed to capture estadao.com.br.")

# Build UOL: Working, last revision on 02/10/2020
try:
    uolRegex = re.compile('.*(economia.uol|noticias.uol).*', re.IGNORECASE)
    uol = NPSpyderBR('uol.com.br','http://www.uol.com.br/', uolRegex)
    total += uol.run()
    del uol
    gc.collect()
except:
    logging.warn("Failed to capture uol.com.br.")

# Build ADFVN: Working, last revision on 02/10/2020
try:
    adfvnRegex = re.compile('.*br.advfn.*', re.IGNORECASE)
    #adfvnRegex = re.compile('.*', re.IGNORECASE)
    adfvn = NPSpyderBR('br.advfn.com','http://br.advfn.com/', adfvnRegex)
    total += adfvn.run()
    del adfvn
    gc.collect()
except:
    logging.warn("Failed to capture br.advfn.com.")

# Build Infomoney: Working, last revision on 02/10/2020
try:
    imoneyRegex = re.compile('.*', re.IGNORECASE)
    imoney = NPSpyderBR('infomoney.com.br','http://www.infomoney.com.br/', imoneyRegex)
    total += imoney.run()
    del imoney
    gc.collect()
except:
    logging.warn("Failed to capture infomoney.com.br.")

# Build Veja: Working, last revision on 02/10/2020
try:
    vejaRegex = re.compile('.*(veja|vejasp|vejario|exame).abril.com.br.*', re.IGNORECASE)
    veja = NPSpyderBR('veja.abril.com.br','http://veja.abril.com.br/', vejaRegex)
    total += veja.run()
    del veja
    gc.collect()
except:
    logging.warn("Failed to capture veja.abril.com.br.")

# Build Investing: Working, last revision on 02/10/2020
try:
    brinvestingRegex = re.compile('.*(mercado|comunicado|indicadores-econ).*', re.IGNORECASE)
    brinvesting = NPSpyderBR('br.investing.com','https://br.investing.com/', brinvestingRegex)
    total += brinvesting.run()
    del brinvesting
    gc.collect()
except:
    logging.warn("Failed to capture br.investing.com.")

# Build Exame: Working, last revision on 02/10/2020
try:
    exameRegex = re.compile('.*(exame).com*', re.IGNORECASE)
    exame = NPSpyderBR('exame.abril.com.br','https://exame.com/', exameRegex)
    #exame = NPSpyderBR('exame.abril.com.br','http://exame.abril.com.br/', exameRegex)
    total += exame.run()
    del exame
    gc.collect()
except:
    logging.warn("Failed to capture exame.abril.com.br.")

# Build Agencia Brasil: Working, but some articles are crashing due to bad URLs. Added and last revised on 02/10/2020
try:
    agbRegex = re.compile('.*', re.IGNORECASE)
    agb = NPSpyderBR('agenciabrasil.ebc.com.br','https://agenciabrasil.ebc.com.br/', agbRegex)
    total += agb.run()
    del agb
    gc.collect()
except:
    logging.warn("Failed to capture agenciabrasil.ebc.com.br.")

# Build CVM: Working. Added and last revised on 02/10/2020
try:
    cvmRegex = re.compile('.*(pensologoinvisto|noticia).*', re.IGNORECASE)
    cvm = NPSpyderBR('cvm.gov.br','http://www.cvm.gov.br/noticias/index.html', cvmRegex)
    total += cvm.run()
    del cvm
    gc.collect()
except:
    logging.warn("Failed to capture cvm.gov.br.")

# Build Acionista: Working. Added and last revised on 02/10/2020
try:
    acionistaRegex = re.compile('.*', re.IGNORECASE)
    acionista = NPSpyderBR('acionista.com.br','https://acionista.com.br/', acionistaRegex)
    total += acionista.run()
    del acionista
    gc.collect()
except:
    logging.warn("Failed to capture acionista.com.br.")

# Build R7: Working. Added and last revised on 02/10/2020
try:
    r7Regex = re.compile('.*(noticias.r7).*', re.IGNORECASE)
    r7 = NPSpyderBR('r7.com','https://www.r7.com/', r7Regex)
    total += r7.run()
    del r7
    gc.collect()
except:
    logging.warn("Failed to capture r7.com.")

# Build Terra: Working. Added and last revised on 02/10/2020
try:
    terraRegex = re.compile('.*', re.IGNORECASE)
    terra = NPSpyderBR('terra.com.br','https://www.terra.com.br/noticias/', terraRegex)
    total += terra.run()
    del terra
    gc.collect()
except:
    logging.warn("Failed to capture terra.com.br.")

# Build poder360: Working. Added and last revised on 02/10/2020
try:
    poderRegex = re.compile('.*', re.IGNORECASE)
    poder = NPSpyderBR('poder360.com.br','https://www.poder360.com.br/', poderRegex)
    total += poder.run()
    del poder
    gc.collect()
except:
    logging.warn("Failed to capture poder460.com.br.")

# Build IG: Working. Added and last revised on 02/10/2020
try:
    igRegex = re.compile('.*', re.IGNORECASE)
    ig = NPSpyderBR('ig.com.br','https://www.ig.com.br/', igRegex)
    total += ig.run()
    del ig
    gc.collect()
except:
    logging.warn("Failed to capture ig.com.br.")

# Build Gazeta: Working. Added and last revised on 02/10/2020
try:
    gazetaRegex = re.compile('.*', re.IGNORECASE)
    gazeta = NPSpyderBR('gazetanews.com','https://www.gazetanews.com/', gazetaRegex)
    total += gazeta.run()
    del gazeta
    gc.collect()
except:
    logging.warn("Failed to capture gazetanews.com.")

# Build ZeroHora: Working. Added and last revised on 02/10/2020
try:
    gzhRegex = re.compile('.*', re.IGNORECASE)
    gzh = NPSpyderBR('gauchazh.clicrbs.com.br','https://gauchazh.clicrbs.com.br/', gzhRegex)
    total += gzh.run()
    del gzh
    gc.collect()
except:
    logging.warn("Failed to capture gauchazh.clicrbs.com.br.")

# Build Correio Braziliense: Working. Added and last revised on 02/10/2020
try:
    correiobRegex = re.compile('.*', re.IGNORECASE)
    correiob = NPSpyderBR('correiobraziliense.com.br','https://www.correiobraziliense.com.br/', correiobRegex)
    total += correiob.run()
    del correiob
    gc.collect()
except:
    logging.warn("Failed to capture correiobraziliense.com.br.")

# Build Reuters BR: Working. Added and last revised on 02/10/2020
try:
    reutersbrRegex = re.compile('.*(br.reuters).*', re.IGNORECASE)
    reutersbr = NPSpyderBR('br.reuters.com','https://br.reuters.com/', reutersbrRegex)
    total += reutersbr.run()
    del reutersbr
    gc.collect()
except:
    logging.warn("Failed to capture br.reuters.com.")

# Build Money Times: Working. Added and last revised on 02/10/2020
try:
    moneytimesRegex = re.compile('.*', re.IGNORECASE)
    moneytimes = NPSpyderBR('moneytimes.com.br','https://www.moneytimes.com.br/', moneytimesRegex)
    total += moneytimes.run()
    del moneytimes
    gc.collect()
except:
    logging.warn("Failed to capture moneytimes.com.br.")

# Build CNN Brasil: Working. Added and last revised on 02/10/2020
try:
    cnnbRegex = re.compile('.*(cnnbrasil).*', re.IGNORECASE)
    cnnb = NPSpyderBR('cnnbrasil.com.br','https://www.cnnbrasil.com.br/', cnnbRegex)
    total += cnnb.run()
    del cnnb
    gc.collect()
except:
    logging.warn("Failed to capture cnnbrasil.com.br.")


'''
# Build Metropole: Working. Added and last revised on 02/10/2020
try:
    metropoleRegex = re.compile('.*', re.IGNORECASE)
    metropole = NPSpyderBR('metropoles.com','https://www.metropoles.com', metropoleRegex)
    total += metrople.run()
    del metrople
    gc.collect()
except:
    logging.warn("Failed to capture metropoles.com.")

# Build Valor Economico
try:
    valorRegex = re.compile('.*', re.IGNORECASE)
    valor = NPSpyderBR('valor.com.br','https://valor.globo.com/', valorRegex)
    #valor = NPSpyderBR('valor.com.br','http://www.valor.com.br/', valorRegex)
    total += valor.run()
    del valor
    gc.collect()
except:
    logging.warn("Failed to capture valor.com.br.")

# Build Ultimo Instante
try:
    uInstanteRegex = re.compile('.*', re.IGNORECASE)
    uInstante = NPSpyderBR('ultimoinstante.com.br','https://www.ultimoinstante.com.br/', uInstanteRegex, firstRun=1)
    total += uInstante.run()
    del uInstante
    gc.collect()
except:
    logging.warn("Failed to capture ultimoinstante.com.br.")

# Build G1
try:
    g1Regex = re.compile('.*(noticia|economia|brasil|politica).*', re.IGNORECASE)
    g1 = NPSpyderBR('g1.globo.com','http://g1.globo.com/', g1Regex)
    total += g1.run()
    del g1
    gc.collect()
except:
    logging.warn("Failed to capture g1.globo.com.")

'''

print("INFO - All feeders crawled, %d articles downloaded." %(total))
