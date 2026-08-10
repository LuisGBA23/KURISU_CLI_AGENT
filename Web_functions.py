from typing import Any
import requests 
from bs4 import BeautifulSoup
from ddgs import DDGS

_last_html_content = ""

def make_http_request(url: str, metodo: str= 'GET', headers: dict= {}, body: Any= None, timeout: int= 30) -> Any:
    """## Realiza una solicitud HTTP a una URL específica.
    ### Argumentos:
    1- *url*: (string) La URL a la que se realizará la solicitud.  
    2- *metodo*: (string, opcional) El método HTTP a utilizar ('GET', 'POST', 'PUT', 'DELETE'). Por defecto es 'GET'.  
    3- *headers*: (dict, opcional) Un diccionario de encabezados HTTP a incluir en la solicitud.  
    4- *body*: (Any, opcional) El cuerpo de la solicitud para métodos como 'POST' o 'PUT'.  
    5- *timeout*: (integer) El tiempo máximo que la función esperará a una respuesta"""

    if isinstance(headers, dict):
        headers["User-Agent"]= "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    
    try: 
        if metodo.upper() == "GET": 
            response= requests.get(url= url, headers= headers, timeout= timeout)
        elif metodo.upper() == "POST": 
            response= requests.post(url= url, headers= headers, data= body, timeout= timeout)
        elif metodo.upper() == "PUT": 
            response= requests.put(url= url, headers= headers, data= body, timeout= timeout)
        elif metodo.upper() == "DELETE":
            response= requests.delete(url= url, headers= headers, timeout= timeout)
        else:
            return f"Error: Método HTTP '{metodo}' no soportado."
        response.raise_for_status()  # Lanza un error para códigos de estado HTTP 4xx/5xx

        # Guardamos el HTML completo en caché para que html_parser lo pueda leer de forma eficiente
        global _last_html_content
        _last_html_content = response.text

        # Si el contenido es HTML, evitamos enviar todo el texto al modelo para no saturar el contexto
        content_type = response.headers.get("Content-Type", "").lower()
        is_html = "text/html" in content_type or response.text.lstrip().startswith(("<html", "<!doctype html", "<!DOCTYPE html"))
        
        if is_html:
            body_content = f"[HTML Content Cached. Size: {len(response.text)} characters. Call html_parser() (without arguments) to extract text and links without sending the raw HTML.]"
        else:
            body_content = response.text

        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": body_content,
            "error": response.reason 
        }
    except requests.exceptions.RequestException as e:
        return {
            "status_code": None,
            "headers": {},
            "body": None,
            "error": str(e)
        }

def html_parser(html: str = None) -> dict:
    '''## Parsea código en HTML para obtener datos específicos (texto y enlaces).  
    ### Argumentos:  
    1- *html*: (string, opcional) El texto plano en HTML a parsear. Si se omite o es None, se utilizará automáticamente el HTML de la última solicitud HTTP realizada con make_http_request (¡usa esta opción sin argumentos para ahorrar tokens y mejorar velocidad!).'''

    global _last_html_content
    html_to_parse = html if html else _last_html_content

    if not html_to_parse:
        return {
            "texto": None,
            "links": None,
            "error": "No hay contenido HTML para parsear. Proporciona el argumento 'html' o realiza una solicitud HTTP primero."
        }

    soup= BeautifulSoup(html_to_parse, 'html.parser')

    texto= soup.get_text(strip= True, separator= ' ')
    links= soup.find_all(attrs= {'href' : True})
    new_links= []
    for link in links: 
        ref= link.get('href')
        titulo= link.get('title') if link.get('title') else str(ref)
        new_links.append({titulo : ref})

    return {
        "texto": texto if texto else None,
        "links": new_links if new_links else None
    }

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