from bs4 import BeautifulSoup as BS
import urllib2

class Sinonimos:

    def __init__(self):
        self.baseURL = "https://www.sinonimos.com.br/"
        
    def getSinonimos(self, word):
        path = self.baseURL + word + "/"
        
        usock = urllib2.urlopen(path)
        data = usock.read()
        usock.close()
        
        soup = BS(data, "lxml")
        
        sinonims = [tag.text for tag in soup.find_all('a', {'class':'sinonimo'})]
        
        print sinonims