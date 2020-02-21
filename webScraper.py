#!/usr/bin/python3

# Description: Collect latest news from gp.se and idg.se and adds them into a file
# with a new filename every day. Write new items to the screen.
# Checks every min (default)

# Moved to public GIT: https://github.com/MC-76/webScraper


from func import MyNews, getPageInfoGP, checkIfExists, getPageInfoIDG, getPageInfoTimesNyTimes, getPageInfoAB, showOnlyHelp, read_API_key           
import os                           # Check if folder exists
import time                         # for sleep
import datetime                     # for logfilename
import sys,getopt                   # for args
from misc import highLights, unicorn         # Highlight file
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
flagHiglights = True           # If True, only print if news is in highlight list
flagHIT = False

# Variables
path = './newsLog/'                 # Where newslog is stored
waitTime = 300                       # Wait in sec between polling (300=5min)
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
        flagHiglights = True
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
    print(unicorn)
    print('Latest news from GP, IDG and Aftonbladet')
    st.title('Latest news from GP, IDG and Aftonbladet')
    #st.divide()
    if flagHiglights:
        print('Showing highlights')
        #st.write('Showing highlights')
    if flagLinks:
        print('Including links')
        #st.write('Including links')

lastFileDate = datetime.date.today()

# Read API keys
NYT_key = read_API_key('NYT')

#Sidebar test
st.sidebar.subheader('WebScraper Settings')
flagHiglights = st.sidebar.checkbox('Highlight news',value=flagHiglights)
flagLinks = st.sidebar.checkbox('Show Links in output',value=flagLinks)

# Placeholders
st.success('Latest news')
news1 = st.empty()
news2 = st.empty()
news3 = st.empty()
news4 = st.empty()
news5 = st.empty()
news6 = st.empty()

st.write()
# check if folder exists, if not create folder
if not os.path.exists(path):
    try:
        os.mkdir(path)
        logger.info(f'Creating folder {path}')
    except OSError:
        print ("Creation of the directory %s failed" % path)
        logger.error(f'Error creating folder: {path}')
        sys.exit()

st.success('History')
while True: # Run forever
    logger.debug('Starting new loop')
    unProcessedNews += getPageInfoGP('https://gp.se','c-teaser-list__item','c-teaser-list__item__label','c-teaser-list__item__title')
    unProcessedNews += getPageInfoIDG('https://idg.se','mostPopularList','articleDate','not_used')
    unProcessedNews += getPageInfoAB('https://aftonbladet.se','HLf1C','c-teaser-list__item__title','not-used')
    unProcessedNews += getPageInfoTimesNyTimes('https://api.nytimes.com/svc/topstories/v2/world.json?api-key=',NYT_key,'NYT-World')
    # ... Other news
    
    for news in unProcessedNews:
        if not checkIfExists(news.title,newsFlow): # Behövs funktion för detta?
            newsFlow.append(news)

            trimmed_title = "{:<80}".format(news.title[:80]) 
            #output = f'{news.label}\t{news.source}\n{trimmed_title}'
            output = f'{news.label} \n'
            output += f'{trimmed_title}\n'
            

            flagHIT = False
            if flagSilent:
                pass
            else:
                if flagLinks:
                    output += f'{news.url}'

                if flagHiglights:
                    for word in highLights:
                        if word.lower() in news.title.lower():
                            flagHIT = True      
                    if flagHIT:
                        st.warning(output)
                        print('Highlight HIT!')
                        print(output)
                    else:
                        st.info(output)
                else:
                    print(output)
                    st.info(output) 
                     
                                      
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
    news1.markdown(f'**{newsFlow[top_news].label}**  \n{newsFlow[top_news].title}  \n{newsFlow[top_news].url}')
    news2.markdown(f'**{newsFlow[top_news-1].label}**  \n{newsFlow[top_news-1].title}  \n{newsFlow[top_news-1].url}')
    news3.markdown(f'**{newsFlow[top_news-2].label}**  \n{newsFlow[top_news-2].title}  \n{newsFlow[top_news-2].url}')
    news4.markdown(f'**{newsFlow[top_news-3].label}**  \n{newsFlow[top_news-3].title}  \n{newsFlow[top_news-3].url}')
  
        

    last_updated.text(f'Last updated: {datetime.datetime.now()}')
    
    
    time.sleep(waitTime)

    