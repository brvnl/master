# encoding=utf8
from parser.Calendar import Calendar
from parser.Definitions import Definitions

import logging
import datetime
import csv
import sys

#======================================================================================
# This file contains classes to help on the organization of the files. The basic concept
# of the organization is to group file names acording to a criteria, such as the publish
# data. In this case, a hash may created in which the key (timestamp) will group all ar-
# ticles publised in that given date.
#======================================================================================

# --------------------------------------------------------------------
# This base class works as an interface for the groupers, which must
# implement the methods below. These methods are used by classes such
# as Representation, which can then process the data even not knowing
# in which level it is grouped.
# --------------------------------------------------------------------
class GroupBase(object):
    def __init__(self, l_files):
        self.l_files = l_files

    def raw(self):
        return self.l_files

    def group(self):
        pass

    def getId(self):
        pass

# --------------------------------------------------------------------
# Builds a hash indexed by [date] and whose values are a [list of fil
# es] for that given date.
# --------------------------------------------------------------------
class GroupByDays(GroupBase):
    def group(self):
        logger = logging.getLogger('GroupByDays')
        logging.basicConfig(format='%(asctime)s %(levelname)s* %(message)s', level=logging.INFO)

        filesByDay = {}

        # Building a hash of [timestamp] -> [list of news files]
        for file in self.l_files:
            filename = file.rstrip("\n\r")
            filename = filename.rstrip("\n")

            # Expecting file path as the example below:
            # /Volumes/Repository/Mestrado/Data/uol.com.br/20160210000000BreakingNews.txt
            paths = filename.split("/")

            if (len(paths) < 2):
                continue

            filename = paths.pop()
            try:
                timestamp = datetime.datetime.strptime(filename[:14], '%Y%m%d%H%M%S').strftime('%Y-%m-%d')
            except:
                logger.warn("Cannot evaluate timestamp on file \"%s\". Discarded." %(filename))

            if timestamp in filesByDay:
                filesByDay[timestamp].append(file)
            else:
                filesByDay[timestamp] = [file]

        logger.info("Files organized in \"%d\" buckets." %(len(filesByDay.keys())))

        return filesByDay

    def getId(self):
        return "Days"


# --------------------------------------------------------------------
# This class has the same behavior as GroupByDays, but with the article
# has been published in an non regular day, it will be assigned to the
# imediate previous regular day instead.
# --------------------------------------------------------------------
class GroupByBusinessDays(GroupBase):
    def __init__(self, l_files, calendar=Definitions.CALENDARS_PATH + "/Regular.txt"):
        self.l_files = l_files
        self.cal = Calendar(filePath=calendar)

    def group(self):
        logger = logging.getLogger('GroupByBusinessDays')
        logging.basicConfig(format='%(asctime)s %(levelname)s* %(message)s', level=logging.INFO)

        filesByDay = {}

        # Building a hash of [timestamp] -> [list of news files]
        for file in self.l_files:
            filename = file.rstrip("\n\r")
            filename = filename.rstrip("\n")

            # Expecting file path as the example below:
            # /Volumes/Repository/Mestrado/Data/uol.com.br/20160210000000BreakingNews.txt
            paths = filename.split("/")

            if (len(paths) < 2):
                continue

            filename = paths.pop()
            try:
                timestamp = datetime.datetime.strptime(filename[:14], '%Y%m%d%H%M%S').strftime('%Y-%m-%d')
            except:
                logger.warn("Cannot evaluate timestamp on file \"%s\". Discarded.\n" %(filename))
                continue

            if (not self.cal.isBusinessDay(timestamp)):
                timestamp = self.cal.previousBusinessDay(timestamp)

            if timestamp in filesByDay:
                filesByDay[timestamp].append(file)
            else:
                filesByDay[timestamp] = [file]

        logger.info("Files organized in \"%d\" buckets.\n" %(len(filesByDay.keys())))

        return filesByDay

    def getId(self):
        return "BDays"


# --------------------------------------------------------------------
# This grouper explores the assumption that an article may impact not
# only the current day, but a number of days following (parameter days
# ). To address the issue, the same article will be assigned to the n
# days following its publication day. 
# For this grouper it is also possible to specify a calendar treatment
# by replacing the default Regular calendar by the desired one.
# --------------------------------------------------------------------
class GroupByDaysRange(GroupBase):
    def __init__(self, l_files, days=1, calendar=Definitions.CALENDARS_PATH + "/Regular.txt"):
        self.l_files = l_files
        self.days = days
        self.cal = Calendar(filePath=calendar)

    def group(self):
        logger = logging.getLogger('GroupByDaysRange')
        logging.basicConfig(format='%(asctime)s %(levelname)s* %(message)s', level=logging.INFO)

        filesByDay = {}

        # Building a hash of [timestamp] -> [list of news files]
        for file in self.l_files:
            filename = file.rstrip("\n\r")
            filename = filename.rstrip("\n")

            # Expecting file path as the example below:
            # /Volumes/Repository/Mestrado/Data/uol.com.br/20160210000000BreakingNews.txt
            paths = filename.split("/")

            if (len(paths) < 2):
                continue

            filename = paths.pop()
            try:
                timestamp = datetime.datetime.strptime(filename[:14], '%Y%m%d%H%M%S').strftime('%Y-%m-%d')
            except:
                logger.warn("Cannot evaluate timestamp on file \"%s\". Discarded." %(filename))

            for t in range(self.days):
                if timestamp in filesByDay:
                    filesByDay[timestamp].append(file)
                else:
                    filesByDay[timestamp] = [file]

                timestamp = self.cal.nextBusinessDay(timestamp)

        logger.info("Files organized in \"%d\" buckets." %(len(filesByDay.keys())))

        return filesByDay

    def getId(self):
        return "DRg-" + str(self.days)