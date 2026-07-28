from typing import Any
import subprocess
import json

def command_exec(comando: str) -> str: 
    '''## Ejecuta un comando en la terminal del sistema (Debian)'''
    if comando.startswith("sudo"):
        print(f"Do you want to execute: {comando}?")
        confirmation= input("y/n/modify: ")

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
    '''## Abre un archivo cuando sea necesario leer o escribir en uno  
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
    except Exception as e: 
        return f"Error leyendo/editando el archivo {ruta}: {e}"