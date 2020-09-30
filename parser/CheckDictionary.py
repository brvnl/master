# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as BS
import urllib2

class CheckDicio:
    def __init__(self, url="https://www.dicio.com.br/"):
        self.baseURL = url

    def _check(self, word):
        path = self.baseURL + word + "/"

        try:
            usock = urllib2.urlopen(path)
            rcode = usock.getcode()
            usock.close()
            rcode = 0
        except urllib2.HTTPError, e:
            rcode = e.code
        except urllib2.URLError, e:
            rcode = -1
            print(e.reason)
        except:
            rcode = -2
    
        #print('%s = %s' %(word, rcode))
        return rcode
        
    def check(self, word):
        if type(word) is list:
            r = {}
            for w in word:
                r[w] = self._check(w)
        else:
            r = self._check(w)
        
        return r
            

class CheckMichaelis:
    def __init__(self, url="http://michaelis.uol.com.br/busca?r=0&f=0&t=0&palavra="):
        self.baseURL = url
        
    def check(self, word):
        path = self.baseURL + word
        
        try:
            usock = urllib2.urlopen(path)
            data = usock.read()
            usock.close()

            soup = BS(data, "lxml")
            if (soup.title.string == u'Verbete não encontrado | Michaelis On-line'):
                rcode = -3
            else:
                rcode = 0 
        except urllib2.HTTPError, e:
            rcode = e.code
        except urllib2.URLError, e:
            rcode = -1
            print(e.reason)
        except:
            rcode = -2
        
        return rcode

class CheckPriberam:
    def __init__(self, url="https://dicionario.priberam.org/"):
        self.baseURL = url
        
    def check(self, word):
        path = self.baseURL + word + "/"
        
        try:
            usock = urllib2.urlopen(path)
            rcode = usock.getcode()
            data = usock.read()
            usock.close()

            soup = BS(data, "lxml")
            
            error = [tag.text for tag in soup.find_all('div', {'class':'alert alert-info'})]
            if (len(error) > 0 ):
                rcode = -3
            else:
                rcode = 0 
        except urllib2.HTTPError, e:
            rcode = e.code
        except urllib2.URLError, e:
            rcode = -1
            print(e.reason)
        except:
            rcode = -2
        
        return rcode

class CheckInformal:
    def __init__(self, url="http://www.dicionarioinformal.com.br/"):
        self.baseURL = url
        
    def check(self, word):
        path = self.baseURL + word + "/"
        
        try:
            req = urllib2.Request(url=path, headers={'User-Agent': 'Mozilla/5.0'}) 
            usock = urllib2.urlopen(req)
            rcode = usock.getcode()
            usock.close()
        except urllib2.HTTPError, e:
            rcode = e.code
        except urllib2.URLError, e:
            rcode = -1
            print(e.reason)
        except:
            rcode = -2
        
        return rcode

class CheckAberto:
    def __init__(self, url='http://dicionario-aberto.net/search/'):
        self.baseURL = url
        
    def check(self, word):
        path = self.baseURL + word
        
        try:
            usock = urllib2.urlopen(path)
            rcode = usock.getcode()
            data = usock.read()
            usock.close()

            soup = BS(data, "lxml")
            
            error = [tag.text for tag in soup.find_all('div', {'class':'notfound'})]
            if (len(error) > 0 ):
                rcode = -3
            else:
                rcode = 0 
        except urllib2.HTTPError, e:
            rcode = e.code
        except urllib2.URLError, e:
            rcode = -1
            print(e.reason)
        except:
            rcode = -2
        
        return rcode