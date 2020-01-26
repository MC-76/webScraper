#!/usr/bin/python3

# Use the BeautifulSoup and requests Python packages to print out a list of all the article titles on the New York Times homepage.

# Ref : https://www.practicepython.org/exercise/2014/06/06/17-decode-a-web-page.html
# Status: PASSED 2020-01-18

# Doc: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# pip3 install bs4
# pip3 install requests

# Description: Collect latest news from gp.se and adds them into a file
# with a new filename every day. Write new items to the screen.
# Checks every min.

# TODO: Create systemlogg
# TODO: Spara ner texten från artiklar
# TODO: Publicera i Flask
# OK Markera om en artikel finns med i register
# TODO: Hämta inställningar från en ini fil
# OK Ändra så att man kollar efter title och inte label
# TODO: Fixa hjälpmeny
# OK Fixa folder om den inte finns
# OK Gör om label så att den hämtar tid från os (efter gp och idg har olika tider)
# TODO: Fixa länk, står https://gp.se framför alla länkar

# Moved to public GIT: https://github.com/MC-76/webScraper



from func import MyNews, getPageInfo, checkIfExists, getPageInfoIDG             # News Class (not really needed)
#from func import checkIfExists      # Check if item has been showed
import os                           # Check if folder exists
# import requests
# from bs4 import BeautifulSoup
import time                         # for sleep
import datetime                     # for logfilename
import sys,getopt                   # for args
from misc import highLights
#from globals import Globals

newsFlow = []
unProcessedNews = []
#globalVar = Globals()              # Class with global vars
flagSilent = False
flagLinks = False                   # display links in output?
flagOnlyHiglights = False           # If True, only print if news is in highlight list
path = './newsLog/'                 # Where newslog is stored
waitTime = 60                       # Wait in sec between polling

#check arg (-s = silent, only write to logg)
#-i Only print if object is in highLight list
try:
    opts, args = getopt.getopt(sys.argv[1:],'sil')
except: # Ignore wrong arguments
    pass

# Check application arguments
for opt, arg in opts:
    if opt=='-s':                   # Silent
        flagSilent = True
    if opt=='-i':                   # Only highlights
        flagOnlyHiglights = True
    if opt=='-l':                   # Show links 
        flagLinks = True

if not flagSilent:
    print('Latest news from https://gp.se:')
    if flagOnlyHiglights:
        print('Only showing highlights:')
counter = 0
lastFileDate = datetime.date.today()

# check if folder exists, if not create folder
if not os.path.exists(path):
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
        sys.exit()

while True: # Run forever
    # TODO : ADD tempNews to a bigger list like gp.se + idg.se
    unProcessedNews += getPageInfo('https://gp.se','c-teaser-list__item','c-teaser-list__item__label','c-teaser-list__item__title')
    unProcessedNews += getPageInfoIDG('https://idg.se','teaser teaserContainer','articleDate','not_used')
    ## NEXT

    for news in unProcessedNews:
        if not checkIfExists(news.title,newsFlow):
            newsFlow.append(news)

            if flagOnlyHiglights:
                for word in highLights:
                    if word in title:
                        if not flagSilent:
                            print('\007')       # Print sound?!?
                            print(f'{news.label}   {news.title}   https://{news.url}')
                    #print(f'*** {word} is found! ***')
            else:
                if not flagSilent:
                    if not flagLinks:
                            print(f'{news.label}   {news.title}')
                    else:
                            print(f'{news.label}   {news.title}   https://gp.se{news.url}')    
            
            
            # Clear buffer when new date
            if lastFileDate != datetime.date.today():
                newsFlow.clear()
                #print('Buffer cleared!')

            with open(f'{path}{datetime.date.today()}-newsLog.txt','a') as fp:
                lastFileDate = datetime.date.today()
                fp.write(str(f'{lastFileDate},{news.label},{news.title},https://gp.se{news.url}\n'))

    # Clear unprocessed Que...should be processed by now       
    unProcessedNews.clear()
    time.sleep(waitTime)
    