import requests
from bs4 import BeautifulSoup

header= {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

with requests.session() as session: 
    try:
        response= session.get("https://es.wikipedia.org/wiki/Steins;Gate", timeout= (5, 10), headers= header)
        response.raise_for_status()
        print(response.status_code)

        if response.status_code == 200: 
            soup= BeautifulSoup(response.text, 'html.parser')
            text= soup.find_all('p')
            links= {}
            print(f"\nHTML: \n")
            for obj in text: 
                if a:= obj.find('a'):
                    links[a.get('title')]= a.get('href')

                print(obj.text+'\n')
            print("\nLINKS: \n")
            for tit, ref in links.items(): 
                print(f"{tit} -> {ref}")
        else: 
            print("error we")
            print(response.status_code)
    except Exception as e: 
        print(f"esxcepcion: {e}")