import requests
from bs4 import BeautifulSoup
from datetime import datetime

class MyNews(object):
    def __init__(self,label,title,url,source):
        self.label = label
        self.title = title
        self.url = url
        self.source = source

def checkIfExists(title, newsFlow):
    for item in newsFlow:
        if item.title in title:
            return True
    return False


def getPageInfo(inputURL,inputClass,inputLabel,inputTitle):
    newsCollection = []
    source = 'GP'

    page = requests.get(inputURL)
    soup = BeautifulSoup(page.text, 'html.parser')

    for headlines in soup.find_all(class_=inputClass):
                    
        for item in headlines.find_all(class_=inputTitle):
            title = item.text.strip()
        for link in headlines.find_all('a'):
            url = link.get('href')
            url = f'https://gp.se{url}'     # URL FIX FOR GP?
        label = datetime.now().strftime('%H:%M')

        newsItem = MyNews(label,title,url,source)
        newsCollection.append(newsItem)
    
    return newsCollection

#Special for IDG
def getPageInfoIDG(inputURL,inputClass,inputLabel,inputTitle):
    newsCollection = []
    label = ''
    title = ''
    url = ''
    source = 'IDG'

    page = requests.get(inputURL)
    soup = BeautifulSoup(page.text, 'html.parser')

    for headlines in soup.find_all(class_='mostPopularList'):
        for label in headlines.find_all(class_=inputLabel): # OK articleDate
            label = label.text.strip()
            for link in headlines.find_all('a'):
                title = link.get('title')
                url = link.get('href')
                url = f'https:{url}'     # URL FIX FOR GP?
                label = datetime.now().strftime('%H:%M')
            # for link in headlines.find_all('a'):
            #     pass
                #print(link.get('title'))
                #print(link.text.strip())
        

        newsItemIDG = MyNews(label,title,url,source)
        newsCollection.append(newsItemIDG)
    
    return newsCollection
        
