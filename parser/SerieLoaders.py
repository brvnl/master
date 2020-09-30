import csv
import datetime
import pandas as pd
import logging

class ExameSeriesLoader(object):
    def __init__(self, filePath):
        self.filePath = filePath
        self.__readDataToDataframe()

    def __readDataToDataframe(self):
        self.raw_serie = pd.read_csv(self.filePath, decimal=",", names=['date', 'price', 'return', 'volume'], skiprows=1)
        self.raw_serie['date'] = pd.to_datetime(self.raw_serie['date'], format='%d/%m/%Y')
        self.raw_serie.set_index('date', inplace=True)

    def getData(self):
        return self.raw_serie


class UOLSeriesLoader(object):
    def __init__(self, filePath):
        self.filePath = filePath
        self.__readDataToDataframe()

    def __readDataToDataframe(self):
        uol_columns = [ 'date', 
                        'price', 
                        'min', 
                        'max',
                        'return',
                        'percent',
                        'volume']

        self.raw_serie = pd.read_csv(self.filePath, decimal=",", names=uol_columns, skiprows=1)
        self.raw_serie['date'] = pd.to_datetime(self.raw_serie['date'], format='%Y-%m-%d')
        self.raw_serie.set_index('date', inplace=True)

    def getData(self):
        return self.raw_serie


class YahooSeriesLoader(object):
    def __init__(self, filePath):
        self.filePath = filePath
        self.__readDataToDataframe()

    def __readDataToDataframe(self):
        uol_columns = [ 'date', 
                        'open', 
                        'max', 
                        'min',
                        'close',
                        'adj close',
                        'volume']

        self.raw_serie = pd.read_csv(self.filePath, decimal=",", names=uol_columns, skiprows=1)
        self.raw_serie['date'] = pd.to_datetime(self.raw_serie['date'], format='%Y-%m-%d')
        self.raw_serie.set_index('date', inplace=True)

    def getData(self):
        return self.raw_serie