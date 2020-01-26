import requests
from bs4 import BeautifulSoup
from datetime import datetime

class MyNews(object):
    def __init__(self,label,title,url,source):
        self.label = label
        self.title = title
        self.url = url
        self.source = source
        #self.category = category 

def checkIfExists(title, newsFlow):
    for item in newsFlow:
        if item.title in title:
            return True
    return False

def showOnlyHelp():
    print('WebSraper 1.0')
    print('''usage: [-s|-i|-h|-l]
             -s: silent, only write news to newslog
             -i: only show news in highlight list
             -h: show this help text
             -l: output with links''')
  
def getPageInfoGP(inputURL,inputClass,inputLabel,inputTitle):
    ''' Get latest news from:
    gp.se'''
    newsCollection = []
    source = 'GP'

    page = requests.get(inputURL)
    soup = BeautifulSoup(page.text, 'html.parser')

    for headlines in soup.find_all(class_=inputClass):              
        for item in headlines.find_all(class_=inputTitle):
            title = item.text.strip()
        for link in headlines.find_all('a'):
            url = link.get('href')
            
        url = f'https://gp.se{url}'
        label = datetime.now().strftime('%H:%M')
        newsCollection.append(MyNews(label,title,url,source))
    
    return newsCollection

#Special for IDG
def getPageInfoIDG(inputURL,inputClass,inputLabel,inputTitle):
    ''' Get latest news from:
    idg.se'''
    newsCollection = []
    source = 'IDG'

    page = requests.get(inputURL)
    soup = BeautifulSoup(page.text, 'html.parser')

    for headlines in soup.find_all(class_='mostPopularList'):
        for label in headlines.find_all(class_=inputLabel):
            label = label.text.strip()
            for link in headlines.find_all('a'):
                title = link.get('title')
                url = link.get('href')

        url = f'https:{url}'
        label = datetime.now().strftime('%H:%M')
        newsCollection.append(MyNews(label,title,url,source))
    
    return newsCollection

def getPageInfoAB(inputURL,inputClass,inputLabel,inputTitle):
    ''' Get latest news from:
    aftonbladet.se'''
    newsCollection = []
    source = 'AB'
    title = ''
    url = ''

    page = requests.get(inputURL)
    soup = BeautifulSoup(page.text, 'html.parser')

    for headlines in soup.find_all('h3'): 
        
        #print(headlines)             
        #for item in headlines.find_all(class_=inputTitle):
        #    title = item.text.strip()
                
        for item in headlines.find_all('h3'):
            title = item.text.strip()
            #print(title)
        for link in headlines.find_all('a'):
            url = link.get('href')
            #print(url)

    # for headlines in soup.find_all(id="supernytt"):
    #     for label in headlines.find_all(class_='HLf1C'):
    #         label = label.text.strip()
    #         for link in headlines.find_all('a'):
    #             title = link.get('title')
    #             url = link.get('href')

            
        #url = f'https://gp.se{url}'
        label = datetime.now().strftime('%H:%M')
        newsCollection.append(MyNews(label,title,url,source))
    
    return newsCollection
        
