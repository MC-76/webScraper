#!/usr/bin/python3

# Description: Collect latest news from gp.se and idg.se and adds them into a file
# with a new filename every day. Write new items to the screen.
# Checks every min (default)

# Moved to public GIT: https://github.com/MC-76/webScraper


from func import MyNews, getPageInfoGP, checkIfExists, getPageInfoIDG, getPageInfoAB, showOnlyHelp            
import os                           # Check if folder exists
import time                         # for sleep
import datetime                     # for logfilename
import sys,getopt                   # for args
from misc import highLights         # Highlight file
import logging
import streamlit as st

#Create and configure logger 
logging.basicConfig(filename="system.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w') 
  
#Creating an object 
logger=logging.getLogger() 
  
#Setting the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG) 

logger.info('Initialising log...')  

#Test messages 
# logger.debug("Harmless debug Message") 
# logger.info("Just an information") 
# logger.warning("Its a Warning") 
# logger.error("Did you try to divide by zero") 
# logger.critical("Internet is down") 

newsFlow = []
unProcessedNews = []

flagSilent = False
flagLinks = True                   # display links in output?
flagOnlyHiglights = False           # If True, only print if news is in highlight list

# Variables
path = './newsLog/'                 # Where newslog is stored
waitTime = 60                       # Wait in sec between polling
logger.info(f'Application setting: path={path}') 
logger.info(f'Application setting: waitTime={waitTime}') 


try:
    opts, args = getopt.getopt(sys.argv[1:],'sihl')
except: # Ignore wrong arguments
    pass

# Check application arguments
for opt, arg in opts:
    if opt=='-s':                   # Silent
        flagSilent = True
        logger.info('Application Flag: flagSilent')  
    if opt=='-i':                   # Only highlights
        flagOnlyHiglights = True
        logger.info('Application Flag: flagOnlyHiglights')  
    if opt=='-h':                   # Show help (and quit)
        showOnlyHelp()
        logger.info('Application Flag: Show help')
        exit()
    if opt=='-l':                   # Show links 
        flagLinks = True
        logger.info('Application Flag: flagLinks')

# Print headers
if not flagSilent:
    last_updated = st.empty()
    print('Latest news from GP, IDG and Aftonbladet')
    st.title('Latest news from GP, IDG and Aftonbladet')
    #st.divide()
    if flagOnlyHiglights:
        print('Only showing highlights:')
        st.write('Only showing highlights:')
    if flagLinks:
        print('Including links:')
        st.subheader('Including links:')

lastFileDate = datetime.date.today()

# Placeholders
st.subheader('Latest news:')
news1 = st.empty()
news2 = st.empty()
news3 = st.empty()
news4 = st.empty()
news5 = st.empty()
news6 = st.empty()




# check if folder exists, if not create folder
if not os.path.exists(path):
    try:
        os.mkdir(path)
        logger.info(f'Creating folder {path}')
    except OSError:
        print ("Creation of the directory %s failed" % path)
        logger.error(f'Error creating folder: {path}')
        sys.exit()

while True: # Run forever
    logger.debug('Starting new loop')
    unProcessedNews += getPageInfoGP('https://gp.se','c-teaser-list__item','c-teaser-list__item__label','c-teaser-list__item__title')
    unProcessedNews += getPageInfoIDG('https://idg.se','mostPopularList','articleDate','not_used')
    unProcessedNews += getPageInfoAB('https://aftonbladet.se','HLf1C','c-teaser-list__item__title','not-used')
    # ... Other news
    
    for news in unProcessedNews:
        if not checkIfExists(news.title,newsFlow): # Behövs funktion för detta?
            newsFlow.append(news)

            trimmed_title = "{:<80}".format(news.title[:80]) 
            output = f'{news.label}\t{news.source}\t{trimmed_title}\t'

            if flagSilent:
                pass
            else:
                if flagLinks:
                    output += f'{news.url}'

                if flagOnlyHiglights:
                    for word in highLights:
                        if word in news.title:
                            logger.info(f'Highlight hit: {word}')
                            print('\007')       # Print sound?!?    
                            print(output)     
                            st.write(output)              
                else:                
                    print(output)
                    st.write(output)

                                      
            # Clear buffer when new date
            if lastFileDate != datetime.date.today():
                newsFlow.clear()
                logger.info('Clearing newsFlow buffer')

            # Save news - Behöver denna göra den varje gång, kanske skall göras i slutet av loop?
            with open(f'{path}{datetime.date.today()}-newsLog.txt','a') as fp:
                lastFileDate = datetime.date.today()
                fp.write(str(f'{lastFileDate},{news.label},{news.source},{news.title},{news.url}\n'))
                logger.info('Saving news to file')

    # Clear unprocessed Que...should be processed by now       
    unProcessedNews.clear()
   
    top_news = len(newsFlow)-1
    #while top_news > 0:
    news1.text(f'{newsFlow[top_news].label}\n{newsFlow[top_news].title}\n{newsFlow[top_news].url}')
    news2.text(f'{newsFlow[top_news-1].label}\n{newsFlow[top_news-1].title}\n{newsFlow[top_news-1].url}')
    news3.text(f'{newsFlow[top_news-2].label}\n{newsFlow[top_news-2].title}\n{newsFlow[top_news-2].url}')
    news4.text(f'{newsFlow[top_news-3].label}\n{newsFlow[top_news-3].title}\n{newsFlow[top_news-3].url}')
  
        

    last_updated.text(f'Last updated: {datetime.datetime.now()}')
    
    
    time.sleep(waitTime)

    