import requests
from bs4 import BeautifulSoup
from ddgs import DDGS

header= {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

'''with requests.session() as session: 
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
        print(f"esxcepcion: {e}")'''

def busqueda_internet(query: str) -> str:
    '''## Realiza una búsqueda web  
    ### Argumentos:  
    1- *query*: (string) la búsqueda a realizar'''
    try:
        with DDGS() as ddgs:
            results= list(ddgs.text(query, max_results= 10))

        if not results: 
            return f"No se encontraron resultados para {query}"

        format_results= []
        for i, res in enumerate(results, 1):
            format_results.append(
                f"Result {i}:\nTitle: {res.get('title')}\nURL: {res.get('href')}\nSnippet: {res.get('body')}\n"
            )
        return "\n".join(format_results)
        
    except Exception as e:
        return f"Error executing search: {str(e)}"

print(busqueda_internet('Unmei no farfalla letra'))