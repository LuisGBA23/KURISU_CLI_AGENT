from typing import Any
import subprocess
from colorama import Fore, Style
import requests 
from bs4 import BeautifulSoup

def command_exec(comando: str) -> str: 
    '''## Ejecuta un comando en la terminal del sistema'''
    if comando.startswith("sudo"):
        print(Fore.RED + Style.BRIGHT + f"\nDo you want to execute: '{comando}'?")
        confirmation= input("y/n/modify: " + Fore.RESET)
        print(Style.RESET_ALL + '\n')

        if confirmation == 'y': 
            pass
        elif confirmation == 'n': 
            return
        elif confirmation == 'modify':
            print(f"Comando actual: {comando}")
            comando= input(">> ")

    try:
        comm= subprocess.run(
            comando, 
            check= True, 
            capture_output= True, 
            text= True,
            shell= True
        )

        return comm.stdout
    except subprocess.CalledProcessError as e: 
        return f"Error al ejecutar el comando: [{e.stderr}]"

def work_with_files(ruta: str, do: str='read', value: str= None) -> Any: 
    '''## Abre un archivo cuando sea necesario leer/sobreescribir o crear uno  
        ### **Argumentos:**
        1- **ruta**: *(string)* la ruta absoluta del archivo a abrir  
        2- **do**: *(string)* indica que se va a hacer con el archivo:
        > -*'read'*: es el valor predeterminado; cuando solo se va a leer el archivo  
        > -*'write'*: cuando se necesita escribir en el archivo (requiere del parametro value)  
        
        3- **value**: *(string)* el texto que se va a escribir en el archivo (solo necesario cuando *do*= 'write')'''
    try: 
        if do == "read":
            with open(ruta, 'r', encoding='utf-8') as f: 
                return f.read()
        elif do == "write": 
            with open(ruta, 'w', encoding= 'utf-8') as f: 
                if not value: 
                    return "Falta parametro 'value'"
                f.write(value)
                return "Archivo editado correctamente"
    except FileNotFoundError:
        return f"Error: El archivo '{ruta}' no fue encontrado."
    except PermissionError:
        return f"Error: Permiso denegado para acceder a '{ruta}'."
    except Exception as e:
        return f"Error al editar el archivo '{ruta}': {e}"

def specific_edit_files(ruta: str, modo: str, contenido: str= None, linea_num: int= None, search_text: str= None, texto_de_reemplazo: str= None) -> Any:
    """## Realiza operaciones de edición avanzada en un archivo.
    ### Argumentos:
    1- *ruta*: (string) La ruta absoluta del archivo a editar.  
    2- *modo*: (string) El tipo de operación a realizar ('append', 'insert_line', 'replace_text', 'delete_line').  
    3- *contenido*: (string, opcional) El texto a añadir o insertar. Necesario para 'append' e 'insert_line'.  
    4- *linea_num*: (int, opcional) El número de línea para operaciones como 'insert_line' o 'delete_line' (base 1).  
    5- *search_text*: (string, opcional) El texto a buscar para reemplazar en el modo 'replace_text'.  
    6- *texto_de_reemplazo*: (string, opcional) El texto con el que reemplazar en el modo 'replace_text'."""

    #modo 'append': añadir al final del archivo: 
    try:
        if modo == 'append': 
            if not contenido: 
                return "Error: el modo 'append requiere del parametro contenido'"
            with open(ruta, 'a', encoding= 'utf-8') as f: 
                f.write(contenido + '\n')
            return f"Contenido añadido al final de {ruta}"

        with open(ruta, 'r', encoding= 'utf-8') as f: 
            lineas= f.readlines()

        if modo == 'insert_lines': 
            if not contenido or not linea_num: 
                return "Error: el modo 'insert_lines' requiere de contenido y linea_num"
            if not (1 <= linea_num <= len(lineas)+1): 
                return f"Error: Número de línea fuera de rango (1 a {len(lineas) + 1})."

            lineas.insert(linea_num-1, contenido if contenido.endswith('\n') else contenido+'\n')

            with open(ruta, 'w', encoding= 'utf-8') as f: 
                f.writelines(lineas)
            return f"Contenido insertado en la linea {linea_num} de {ruta}"
        
        elif modo == 'replace_text': 
            if not search_text or not texto_de_reemplazo: 
                return "Error: El modo 'replace_text' requiere 'texto_a_buscar' y 'texto_de_reemplazo'."

            whole_text= "".join(lineas)
            new_text= whole_text.replace(search_text, texto_de_reemplazo)

            with open(ruta, 'w', encoding= 'utf-8') as f: 
                f.write(new_text)
            return f"Texto reemplazado en '{ruta}'."

        elif modo == 'delete_text': 
            if not linea_num: 
                return "Error: el modo 'delete_text' requiere de linea_num"
            if not (1 <= linea_num <= len(lineas)+1): 
                return f"Error: Número de línea fuera de rango (1 a {len(lineas) + 1})."

            del lineas[linea_num-1]

            with open(ruta, 'w', encoding= 'utf-8') as f: 
                f.writelines(lineas)
            return f"Línea {linea_num} eliminada de '{ruta}'."

        else:
            return "Error: Modo de edición no reconocido. Use 'append', 'insert_line', 'replace_text' o 'delete_line'."
    except FileNotFoundError:
        return f"Error: El archivo '{ruta}' no fue encontrado."
    except PermissionError:
        return f"Error: Permiso denegado para acceder a '{ruta}'."
    except Exception as e:
        return f"Error al editar el archivo '{ruta}': {e}"

def do_a_commit(ruta: str, mensaje: str) -> str: 
    '''## Realiza un commit en un repositorio git
        ### Argumentos:
        1- **ruta**: *(string)* la ruta absoluta del repositorio git  
        2- **mensaje**: *(string)* el mensaje del commit'''
    try:
        # Cambiar al directorio del repositorio
        add= subprocess.run(['git', '-C', ruta, 'add', '.'], check=True, capture_output=True, text=True)
        commit= subprocess.run(['git', '-C', ruta, 'commit', '-m', mensaje], check=True, capture_output=True, text=True)

        return f"Commit realizado en {ruta} con el mensaje: '{mensaje}' \nSalidas\n add: {add.stdout} \ncommit: {commit.stdout}"
    except subprocess.CalledProcessError as e:
        return f"Error al realizar el commit: {e}"
    except Exception as e:
        return f"Error inesperado: {e}"

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