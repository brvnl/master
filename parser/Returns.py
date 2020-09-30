import logging
from Calendar import Calendar
import pandas as pd

def ret(array):
    return (array[-1]/array[0] - 1)

class MultiplicativeReturns(object):
    def __init__(self, serie, bw=1, fw=0):
        self.raw = serie.copy()
        self.th_backward = bw
        self.th_foward = fw

    def process(self):
        self.raw.sort_index(ascending=True, inplace=True)

        if (self.th_foward > 0):
            w = self.th_backward + (self.th_foward + 1)
            r = self.raw.rolling(window=w).apply(ret, raw=True).shift(-1 * self.th_foward)
        else:
            r = self.raw.pct_change(self.th_backward)

        return r.dropna()

    def getID(self):
        return "mr-bw" + str(self.th_backward) + "-fw" + str(self.th_foward)


class OpenCloseMultiplicativeReturns(object):
    def __init__(self, openserie, closeserie, bw=0, fw=0):
        self.openserie = openserie.copy()
        self.closeserie = closeserie.copy()
        self.th_backward = bw
        self.th_foward = fw

        self.openserie.sort_index(ascending=True, inplace=True)
        self.closeserie.sort_index(ascending=True, inplace=True)

    def process(self):
        openseries_s = self.openserie.shift(self.th_backward)
        closeseries_s = self.closeserie.shift(-1 * self.th_foward)

        r = closeseries_s / openseries_s
        r.dropna()
        r = r -1

        return r

    def getID(self):
        return "ocmr-bw" + str(self.th_backward) + "-fw" + str(self.th_foward)


class AbsoluteMultiplicativeReturns(MultiplicativeReturns):
    def process(self):
        r = super(AbsoluteMultiplicativeReturns, self).process()
        return r.abs()

    def getID(self):
        return "amr-bw" + str(self.th_backward) + "-fw" + str(self.th_foward)


class AbnormalMultiplicativeReturns(MultiplicativeReturns):
    def __init__(self, serie, mserie, bw=1, fw=0, t='additive'):
        r = super(AbnormalMultiplicativeReturns, self).__init__(serie, bw=bw, fw=fw)
        self.mserie = mserie.copy()
        self.type = t

    def process(self):
        r = super(AbnormalMultiplicativeReturns, self).process()
        mr = MultiplicativeReturns(self.mserie, bw=self.th_backward, fw=self.th_foward)
        m = mr.process()

        if (self.type == 'additive'):
            ar = r.subtract(m)
        else:
            ar = r.divide(m)

        return ar.dropna()

    def getID(self):
        return "abnmr-bw" + str(self.th_backward) + "-fw" + str(self.th_foward)


class OpenCloseAbnormalMultiplicativeReturns(object):
    def __init__(self, openserie, closeserie, openmarket, closemarket, bw=0, fw=0):
        self.openserie = openserie.copy()
        self.closeserie = closeserie.copy()
        self.openmarket = openmarket.copy()
        self.closemarket = closemarket.copy()

        self.th_backward = bw
        self.th_foward = fw

    def process(self):
        sr = OpenCloseMultiplicativeReturns(openserie=self.openserie, closeserie=self.closeserie, bw=self.th_backward, fw=self.th_foward)
        mr = OpenCloseMultiplicativeReturns(openserie=self.openmarket, closeserie=self.closemarket, bw=self.th_backward, fw=self.th_foward)

        sr_s = sr.process()
        mr_s = mr.process()

        r = sr_s.subtract(mr_s)
        return r.dropna()

    def getID(self):
        return "ocabnmr-bw" + str(self.th_backward) + "-fw" + str(self.th_foward)