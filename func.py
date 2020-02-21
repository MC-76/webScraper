import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import yaml


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

def read_API_key(input_key):
    with open(r'api-keys.yaml') as file:
        api_keys = yaml.load(file, Loader=yaml.FullLoader)

    return api_keys[input_key]

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

        # IDG Link wierd if news from IDG
        if '2.1085/' in url:
            url = f'https://idg.se{url}'
        else:
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

    for headlines in soup.find_all(id='supernytt'): 
        #print(headlines.prettify()) 

        for x in headlines.find_all(class_='HLf1C'):

            for item in x.find_all('h3'):
                title = item.text.strip()
                #print(item.prettify())
                #print(title)
            for link in x.find_all('a'):
                url = link.get('href')
                #print(url)
                    
                #url = f'https://gp.se{url}'
                #print(f'{title}\t{url}')
                label = datetime.now().strftime('%H:%M')
                newsCollection.append(MyNews(label,title,url,source))
    
    return newsCollection
        
def getPageInfoTimesNyTimes(inputURL,inputKEY,input_cat):
    ''' Get latest news from:
    nyTimes API
    The Top Stories API returns an array of articles currently on the specified section (arts, business, ...)
    '''
    newsCollection = []
    source = input_cat
    title = ''
    url = ''

    page = requests.get(inputURL+inputKEY)
    page.encoding = 'utf-8'
    
    myJson = json.loads(page.content)

    for article in myJson['results']: 
        title = article['title']
        url = article['url']
        label = datetime.now().strftime('%H:%M')
        
        newsCollection.append(MyNews(label,title,url,source))
    
    return newsCollection