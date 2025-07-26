import requests
import re
from bs4 import BeautifulSoup

def getTranscript(): #FOR TED TALK

    URLS = []

    for URL in URLS:
        RESPONSE = requests.get(URL+"/transcript")
        RESPONSE.raise_for_status()

        FILE = open(r"CORPUS/TedTalkTranscripts.txt", "a", encoding="utf-8")
        TITLE = re.search(r'"name":"(.*?)","', RESPONSE.text)
        TRANSCRIPT = re.search(r'"transcript":"(.*?)","', RESPONSE.text)

        if TITLE and TRANSCRIPT:
            FILE.write(TITLE.group(1)+"\n")
            FILE.write(TRANSCRIPT.group(1)+"\n\n")

def filterSentencesByToken():

    CORPUS_NAME = "EMEA"
    PATH = "C:/Users/NICK SENTERO/Downloads/en (1).txt/en (1).txt"
    FILE = open(PATH, "r", encoding="utf-8")
    CORPUS_FILE = open(f"CORPUS/{CORPUS_NAME}.txt", "w", encoding="utf-8")

    CHARACTERS = ["(", ")", "[", "]", ".", ",","?", "!", ";", ":"]

    for LINE in FILE:

        SENTENCE = LINE

        for CHARACTER in CHARACTERS:
            SENTENCE.replace(CHARACTER, " "+CHARACTER+" ")

        TOKENS = SENTENCE.split(" ")

        if len(TOKENS) <= 50:
            CORPUS_FILE.write(LINE)

def findAllArticles(url):

    art = open("wikipedia_articles.txt", "w", encoding="utf-8")
    title = ""
    i = 1
   
    wiki_url = "wikipedia.org"
    lang = "ilo"

    while True: 
        
        RESPONSE = ""
        print(f"Extracting on Page {i}")

        if i == 3:
            break

        if i > 1: 
            RESPONSE = requests.get(url+str(title))
        else:
            RESPONSE = requests.get(url+"%21")

        RESPONSE.raise_for_status()
        soup = BeautifulSoup(RESPONSE.text, "html.parser")
        content_div = soup.find('div', class_='mw-body-content') 

        if not content_div:
            print("Could not find the main content div.")
            break
    
        links = content_div.find_all('a')
    
        for link in links:
            href = link.get('href')
            title = link.get('title')

            if href and href.startswith("/wiki/") and ":" not in href and not href.startswith("/wiki/Special:"):

                full_url = f"https://ilo.wikipedia.org{href}"
                test = f"https://{lang}.{wiki_url}{href}"
                

                art.write(str({"title": title if title else link.text.strip(), "url": full_url})+"\n")
        i+=1
        
def prettifyWeb(url):

    RESPONSE = requests.get(url)
    RESPONSE.raise_for_status()
    soup = BeautifulSoup(RESPONSE.text, "html.parser")
    print(soup.prettify())

URL = ""

getTranscript()

