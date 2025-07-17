import requests
import re
from bs4 import BeautifulSoup

def getTranscript(url): #FOR TED TALK

    resp = requests.get(url+"/transcript")
    resp.raise_for_status()
    match = re.search(r'"transcript":"(.*?)","', resp.text)

    if match:
        print(match.group(1))

def findAllArticles(url):

    art = open("wikipedia_articles.txt", "w", encoding="utf-8")
    title = ""
    i = 1
   
    wiki_url = "wikipedia.org"
    lang = "ilo"

    while True: 
        
        resp = ""
        print(f"Extracting on Page {i}")

        if i == 3:
            break

        if i > 1: 
            resp = requests.get(url+str(title))
        else:
            resp = requests.get(url+"%21")

        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
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

    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    print(soup.prettify())

url = "https://www.ted.com/talks/hawa_abdi_deqo_mohamed_mother_and_daughter_doctor_heroes"

getTranscript(url)

