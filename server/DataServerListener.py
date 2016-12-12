import sys
import socket
import os.path
import fileinput
import re
import logging
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

from parser.ArticlesFilter import ArticlesFilter


## STATIC VARIABLES
##----------------------------
logging.basicConfig(format='%(asctime)s %(levelname)s* %(message)s', level=logging.INFO)
corpus_root = '../../data/'
KEYWORDS_FILES_PATH="../../keywords/"
stmp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
stmp.connect(("gmail.com",80))
host = stmp.getsockname()[0]

port = 22005


## AUXILIARY ROUTINES
##----------------------------
def mychomp(usr):
    return usr.rstrip("\r\n").rstrip("\n")

def unifyLineFeed(text):
    newText = re.sub('(\r\n)+', '\n', text)
    newText = re.sub('(\n)+', '\n', newText)
    return newText

def getKeywords(usr):
    # Saves the keywords on a different file
    fname = KEYWORDS_FILES_PATH + usr + ".pos"
    file = open(fname, 'r')
    keywords = file.read()
    keywords = keywords.rstrip("\r\n")
    keywords = keywords.rstrip("\n")
    keywordsList = keywords.split(",")
    file.close()

    return keywordsList

def getNKeywords(usr):
    # Saves the keywords on a different file
    fname = KEYWORDS_FILES_PATH + usr + ".neg"
    file = open(fname, 'r')
    keywords = file.read()
    keywords = keywords.rstrip("\r\n")
    keywords = keywords.rstrip("\n")
    keywordsList = keywords.split(",")
    file.close()

    return keywordsList

def getBasicData(fname):
    file = open(fname, 'r')
    url = file.readline()
    title = file.readline()
    file.close()
    return [url, title]

def getFullText(fname):
    file = open(fname, 'r')

    with open(fname) as f:
        lines = f.readlines()

    nonemptyllines = [x for x in lines if x]
    text = "\n".join(nonemptyllines[2:])
    text = unifyLineFeed(text)
    return text.split("\r\n")


## MAIN PROGRAM
##----------------------------
logging.info("Starting data service...")
soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
logging.info("Socket created.")

try:
    #Bind socket to local host and port
    soc.bind((host, port))
except socket.error as msg:
    logging.error('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    exit()

soc.listen(10)
logging.info("Listening on host %s:%d." %(host, port))

while True:
    conn, addr = soc.accept()

    logging.info("Got connection from %s." %(str(addr)))
    msg = conn.recv(1024)

    # Remove first bytes added by Java
    msg = re.sub('^[^@]*@', '@', msg)

    logging.info("Request:" + msg)
    parameters = msg.split(";")

    if (len(parameters) <= 1):
        continue

    operation = '@' + parameters[0].split('@')[1]
    if (operation == "@fetchUserArticles"):
        usr = parameters[1]
        usr = usr.split(":")[1]
        usr = usr.rstrip("\r\n")
        usr = usr.rstrip("\n")

        feeders = parameters[3]
        feeders = feeders.split(":")[1]
        feeders = feeders.rstrip("\r\n")
        feeders = feeders.rstrip("\n")
        feedersList = feeders.split("OV=I=XseparatorX=I=VO")

        tw = parameters[4]
        tw = tw.split(":")[1]
        tw = tw.rstrip("\r\n")
        tw = int(tw.rstrip("\n"))

        logging.info("Fetching articles for user \"%s\"." %(usr))
        logging.info("Parameters: feeders=\"%s\"; timewindow=\"%s\"." %(feeders, tw))

        keys = getKeywords(usr)
        nkeys = getNKeywords(usr)
        logging.info("User keys: \"%s\"." %("|".join(keys)))
        logging.info("User nkeys: \"%s\"." %("|".join(nkeys)))

        aFilter = ArticlesFilter(corpus_root, keys, nkeys)
        aFilter.findArticles()
        aFilter.files2hash()

        counter = 0
        timestamps = sorted(aFilter.date2feeder2article.keys(), reverse=True)
        for timestamp in timestamps[:tw]:
            for feeder in sorted(aFilter.date2feeder2article[timestamp]):
                if feeder in feedersList:
                    id = aFilter.date2feeder2article[timestamp][feeder]
                    url, title = getBasicData(id)
                    articleSummary = mychomp(id) + "|" + mychomp(url) + "|" + mychomp(title) + "|" + mychomp(timestamp) + "\r\n"
                    sent = conn.send(articleSummary)
                    counter += 1
        logging.info("%d articles sent to client." %(counter))
        sent = conn.send("Done\r\n")

    elif (operation == "@getKeywords"):
        usr = parameters[1]
        usr = usr.split(":")[1]
        usr = usr.rstrip("\r\n")
        usr = usr.rstrip("\n")

        logging.info("Getting keywords for user \"%s\"." %(usr))
        keys = getKeywords(usr)
        nkeys = getNKeywords(usr)
        strKeys = ", ".join(keys)
        strNKeys = ", ".join(nkeys)
        strKeys = strKeys + "|" + strNKeys
        sent = conn.send(strKeys)

    elif (operation == "@fetchFullText"):
        id = mychomp(";".join(parameters[1:]))

        logging.info("Fetching full text for \"%s\"." %(id))

        textLines = getFullText(id)

        for aline in textLines:
            sent = conn.send(aline + "\r\n\r\n")

        sent = conn.send("Done\r\n")

    logging.info("Request concluded.")
    conn.close()

soc.close()

exit()
