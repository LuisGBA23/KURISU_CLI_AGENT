import json 
import random

#Función para abrir un archivo y leerlo o escribirlo según el parámetro do:
def open_file(ruta: str, do= 'read_txt', modo= 'r', values_to_dump= None): 
    '''**do**= 'read_txt' (predeterminado), 'read_json', 'json_dump'

        **modo**= 'r' (predeterminado), 'w' '''
    try: 
        with open(ruta, modo, encoding='utf-8') as f: 
            if do == "read_txt": 
                return f.read()
            elif do == "read_json":
                return json.load(f)
            elif do == "json_dump": 
                json.dump(values_to_dump, f, indent= 4, ensure_ascii= False)
    except Exception as e: 
        print(f"Error leyendo/editando el archivo {ruta}: {e}")

#Elegir y retornar un valor al azar de una pool de opciones (APIs): 
def elegir_api(lista):
    try: 
        return random.choice(lista)
    except Exception as e:
        print(f"An error ocurred while trying to choice from {lista} | {e}")

#Dividir un string largo en pequeños fragmentos de cierto limite de caracteres: 
def dividir_text(text, limit= 1000):
    frags= [] #se crea una lista vacía para guardar los fragmentos
    while len(text) > limit: 
        '''usamos rfind para buscar el último espacio en blanco (para no cortar palabras) dentro 
        del rango: 0 (inicio del texto) - limite'''
        indice_corte= text.rfind(' ', 0, limit)
        if indice_corte == -1: #Si devuelve -1 (inexistente) establece el corte exactamente en el limite
            indice_corte= limit
        frags.append(text[:indice_corte]) #guarda dentro de la lista el fragmento entre el inicio del texto y el limite
        text= text[indice_corte:].lstrip() #actualiza el valor del texto para quitar el fragmento que ya guardamos (lstrip() limpia los espacios en blanco que puideron haber quedado al principio)
    if text: #se ejecuta si el texto es corto o cuando ya no supera el limite de caracteres 
        frags.append(text)
    return frags

#Función para cambiar un atributo dentro de un archivo JSON:
def set_attribute(attribute: str, value: str, conf_file: str):
    b_conf= open_file(conf_file, do= 'read_json')

    try:
        if '.' in value: 
            factored_value= float(value)
        else: 
            factored_value= int(value)
    except ValueError: 
        factored_value= value

    b_conf[attribute]= factored_value
    open_file(
    conf_file, 
    do= 'json_dump', 
    modo= 'w', 
    values_to_dump= b_conf
    )