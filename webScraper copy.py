#!/usr/bin/python3

# Description: Collect latest news from gp.se and idg.se and adds them into a file
# with a new filename every day. Write new items to the screen.
# Checks every min (default)

# Moved to public GIT: https://github.com/MC-76/webScraper


from func import MyNews, getPageInfo, checkIfExists, getPageInfoIDG, showOnlyHelp            
import os                           # Check if folder exists
import time                         # for sleep
import datetime                     # for logfilename
import sys,getopt                   # for args
from misc import highLights         # Highlight file


newsFlow = []
unProcessedNews = []

flagSilent = False
flagLinks = False                   # display links in output?
flagOnlyHiglights = False           # If True, only print if news is in highlight list

# Variables
path = './newsLog/'                 # Where newslog is stored
waitTime = 60                       # Wait in sec between polling


try:
    opts, args = getopt.getopt(sys.argv[1:],'sihl')
except: # Ignore wrong arguments
    pass

# Check application arguments
for opt, arg in opts:
    if opt=='-s':                   # Silent
        flagSilent = True
    if opt=='-i':                   # Only highlights
        flagOnlyHiglights = True
    if opt=='-h':                   # Show help (and quit)
        showOnlyHelp()
        exit()
    if opt=='-l':                   # Show links 
        flagLinks = True

# Print headers
if not flagSilent:
    print('Latest news from GP and IDG')
    if flagOnlyHiglights:
        print('Only showing highlights:')
    if flagLinks:
        print('Including links:')

lastFileDate = datetime.date.today()

# check if folder exists, if not create folder
if not os.path.exists(path):
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
        sys.exit()

while True: # Run forever
    unProcessedNews += getPageInfo('https://gp.se','c-teaser-list__item','c-teaser-list__item__label','c-teaser-list__item__title')
    unProcessedNews += getPageInfoIDG('https://idg.se','teaser teaserContainer','articleDate','not_used')
    # ... Other news
    
    for news in unProcessedNews:
        if not checkIfExists(news.title,newsFlow): # Behövs funktion för detta?
            newsFlow.append(news)

            if flagOnlyHiglights and not flagSilent:
                for word in highLights:
                    if word in news.title:
                        trimmed_title = "{:<80}".format(news.title[:80]) 
                        print(f'{news.label}\t{news.source}\t{trimmed_title}{news.url}')
                        print('\007')       # Print sound?!?                   
            else:
                if not flagSilent:  #Skum logic
                    if not flagLinks:
                        trimmed_title = "{:<160}".format(news.title[:160]) 
                        print(f'{news.label}\t{news.source}\t{trimmed_title}')
                    else:             
                            trimmed_title = "{:<80}".format(news.title[:80]) 
                            print(f'{news.label}\t{news.source}\t{trimmed_title}\t{news.url}')
                             
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
    