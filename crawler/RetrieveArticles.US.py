#!/usr/bin/python
from tldextract.tldextract import LOG
from NPSpyder import NPSpyder
from NPSpyderBR import NPSpyderBR
import logging
import re
import gc

logging.basicConfig(level=logging.CRITICAL)
total = 0

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
    economistRegex = re.compile('.*', re.IGNORECASE)
    #economistRegex = re.compile('.*(www.economist.com/news/).*', re.IGNORECASE)
    economist = NPSpyder('economist.com','http://www.economist.com/', economistRegex)
    total += economist.run()
    del economist
    gc.collect()
except:
    logging.warn("Failed to capture economist.com.")

# Build CNN
try:
    cnnRegex = re.compile('.*', re.IGNORECASE)
    cnn = NPSpyder('cnn.com','http://www.cnn.com/', cnnRegex)
    total += cnn.run()
    del cnn
    gc.collect()
except:
    logging.warn("Failed to capture cnn.com.")

print("INFO - All feeders crawled, %d articles downloaded." %(total))
