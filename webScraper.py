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
# DONE: Fixa länk, står https://gp.se framför alla länkar
# DONE: FIX SOURCE
# DONE: Ta bort dubble // i idg länk
# DONE: Begränsa output när man visar länkar
# TODO: Städa kod!
# TODO: Fixa if logic --- igna if not -- endast if flag osv


# Moved to public GIT: https://github.com/MC-76/webScraper



from func import MyNews, getPageInfo, checkIfExists, getPageInfoIDG             

import os                           # Check if folder exists

import time                         # for sleep
import datetime                     # for logfilename
import sys,getopt                   # for args
from misc import highLights
#from globals import Globals

newsFlow = []
unProcessedNews = []
flagSilent = False
flagLinks = False                   # display links in output?
flagOnlyHiglights = False           # If True, only print if news is in highlight list
path = './newsLog/'                 # Where newslog is stored
waitTime = 60                       # Wait in sec between polling
#MAX_TITLE_LENGHT = 40               # Max lenght of title URL when showing links




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
        if not checkIfExists(news.title,newsFlow): # Behövs funktion för detta?
            newsFlow.append(news)

            if flagOnlyHiglights and not flagSilent:
                for word in highLights:
                    if word in news.title:
                        #if not flagSilent:
                        trimmed_title = "{:<80}".format(news.title[:80]) 
                        print(f'{news.label}\t{news.source}\t{trimmed_title}{news.url}')  # FUL OUTPUT, BEGRÄNSA TILL 25 tecken eller liknande
                        print('\007')       # Print sound?!?
                    #print(f'*** {word} is found! ***')
            else:
                if not flagSilent:  #Skum logic
                    if not flagLinks:
                        trimmed_title = "{:<160}".format(news.title[:160]) 
                        print(f'{news.label}\t{news.source}\t{trimmed_title}')
                    else:
                            # Always trim?              
                            trimmed_title = "{:<80}".format(news.title[:80]) 
                            print(f'{news.label}\t{news.source}\t{trimmed_title}\t{news.url}')
                            #print(f'{news.label}\t{news.source}\t{news.title[:<trim].}\t\t{news.url}')
                        # else:
                        #     print('*')
                        #     print(f'{news.label}\t{news.source}\t{news.title}\t{news.url}')
            
            
            # Clear buffer when new date
            if lastFileDate != datetime.date.today():
                newsFlow.clear()
                #print('Buffer cleared!')

            # Save news
            with open(f'{path}{datetime.date.today()}-newsLog.txt','a') as fp:
                lastFileDate = datetime.date.today()
                fp.write(str(f'{lastFileDate},{news.label},{news.source},{news.title},{news.url}\n'))

    # Clear unprocessed Que...should be processed by now       
    unProcessedNews.clear()
    time.sleep(waitTime)
    