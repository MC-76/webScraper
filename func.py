import requests
from bs4 import BeautifulSoup
from datetime import datetime

class MyNews(object):
    def __init__(self,label,title,url):
        self.label = label
        self.title = title
        self.url = url

def checkIfExists(title, newsFlow):
    for item in newsFlow:
        if item.title in title:
            return True
    return False

# Vad vill jag?
#skicka in url, samt inställningar, skicka tillbaka en lista med inlästa nyheter
def getPageInfo(inputURL,inputClass,inputLabel,inputTitle):
    newsCollection = []

    page = requests.get(inputURL)
    soup = BeautifulSoup(page.text, 'html.parser')

    for headlines in soup.find_all(class_=inputClass):
        #for label in headlines.find_all(class_=inputLabel):
            #label = label.text.strip()
            
        for item in headlines.find_all(class_=inputTitle):
            title = item.text.strip()
        for link in headlines.find_all('a'):
            url = link.get('href')
        label = datetime.now().strftime('%H:%M')

        newsItem = MyNews(label,title,url)
        newsCollection.append(newsItem)
    
    return newsCollection

#Special for IDG
def getPageInfoIDG(inputURL,inputClass,inputLabel,inputTitle):
    newsCollection = []
    label = ''
    title = ''
    url = ''

    page = requests.get(inputURL)
    soup = BeautifulSoup(page.text, 'html.parser')

    for headlines in soup.find_all(class_='mostPopularList'):
        #print(headlines.text)
        for label in headlines.find_all(class_=inputLabel): # OK articleDate
            #print(label.text.strip())
            label = label.text.strip()
            for link in headlines.find_all('a'):
                title = link.get('title')
                url = link.get('href')
                label = datetime.now().strftime('%H:%M')
                #print(link.get('title'))
                #print(link.get('href'))
            for link in headlines.find_all('a'):
                pass
                #print(link.get('title'))
                #print(link.text.strip())
        

        newsItemIDG = MyNews(label,title,url)
        newsCollection.append(newsItemIDG)
    
    return newsCollection
        
