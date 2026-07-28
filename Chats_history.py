from google import genai
from google.genai import types
import pickle
import os

def guardar_historial(path: str, chat_list): 
    with open(path, 'wb') as f:
        pickle.dump(chat_list, f)

def cargar_historial(path: str): 
    if os.path.exists(path) and os.path.getsize(path) > 0: 
        with open(path, 'rb') as f:
            return pickle.load(f)
    return {}

def clear_history(chat_list, canal):
    chat_list[canal]= []