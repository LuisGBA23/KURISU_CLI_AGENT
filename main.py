"""
main.py

Este archivo es el punto de entrada principal para el Agente de IA CLI de Alto Rendimiento (Kurisu CLI Agent).
Gestiona la carga de configuración, inicializa el modelo de IA, maneja la interacción del usuario
(entrada de texto y voz), procesa comandos especiales y guarda el historial de chat.
También incluye mecanismos para la gestión de errores de la API y la notificación de finalización de tareas.
"""
from google import genai
from google.genai import types
from dotenv import load_dotenv
from winotify import Notification, audio
import os
import sys
import platform
import time
from colorama import Fore, Style
import Utilities, Chats_history, Voice_comms
import Functions, Web_functions, Spotify_functions

load_dotenv()
API_LIST= os.getenv("GEMINI_KEYS").split(',')
if not API_LIST: 
    raise ValueError("missing env vars")
CONFIG_PATH= Utilities.get_path_to_parent_dict(__file__, 'configs', 'Kurisu_config.json')
SYS_INST_PATH= Utilities.get_path_to_parent_dict(__file__, 'configs', 'system_instruction.md')
HISTORIAL_PATH= Utilities.get_path_to_parent_dict(__file__, 'configs', 'historial.pkl')
KURISU_ICON_PATH= Utilities.get_path_to_parent_dict(__file__, 'public', 'Kurisu_icon.png')
REGISTRY= [
    Functions.command_exec, 
    Functions.work_with_files, 
    Functions.specific_edit_files, 
    Functions.do_a_commit,
    Web_functions.busqueda_internet,
    Web_functions.make_http_request,
    Web_functions.html_parser,
    Spotify_functions.playback_manage,
    Spotify_functions.search_and_start_song,
]

def cargar_conf(): 
    kurisu_config= Utilities.open_file(CONFIG_PATH, do= 'read_json')
    system_instruction= Utilities.open_file(SYS_INST_PATH)
    config_mod= types.GenerateContentConfig(
        tools= REGISTRY,
        system_instruction= system_instruction,
        temperature= kurisu_config['temperature'],
        top_p= kurisu_config['top_p']
    )
    return kurisu_config, config_mod

def get_context() -> dict[str, str]: 
    context= {
        "directorio_actual" : os.getcwd(),
        "usuario_actual" : os.getlogin(),
        "sistema_operativo" : f"{sys.platform} {platform.release()}",
        "arquitectura_cpu" : platform.machine(),
        "entorno_shell" : os.getenv('SHELL') if sys.platform != 'win32' else os.getenv('COMSPEC'),
        "nota" : "Si el nombre de una cancion está en japonés romanizado, tradúcelo a japonés con hiragana o katakana antes de buscarlo en Spotify. Ignora este mensaje si la solicitud no tiene relación con canciones en japonés romanizado."
    }
    return context

start_on_voice= False
while True:
    try:
        chosen_api= Utilities.elegir_api(API_LIST)
        kurisu_config, config_mod= cargar_conf()
        hist= Chats_history.cargar_historial(HISTORIAL_PATH)
        client= genai.Client(api_key= chosen_api)
        chat= client.chats.create( 
            model= kurisu_config['model_name'],
            history= hist,
            config= config_mod
        )

        inp= input(Fore.CYAN + "(Christina) >> " + Fore.RESET) if not start_on_voice else 'voz'
        if inp.lower() in ["voice", "voz"]: 
            print(Fore.CYAN + "(Christina VOICE) >>" + Fore.RESET, end= ' ')
            inp= Voice_comms.start_voice()
            if inp.lower() == 'texto': 
                start_on_voice= False
                continue
            print(inp)
            start_on_voice= True
        elif inp.lower() == "byebye": 
            print(Fore.RESET)
            break
        elif inp.lower() in ["clear", "clear history", "clean", "limpiar"]:
            if os.path.exists(HISTORIAL_PATH):
                try:
                    os.remove(HISTORIAL_PATH)
                    print(Fore.GREEN + "Historial de chat borrado con éxito." + Fore.RESET)
                except Exception as e:
                    print(Fore.RED + f"No se pudo borrar el historial: {e}" + Fore.RESET)
            else:
                print(Fore.YELLOW + "No hay historial para borrar." + Fore.RESET)
            continue

        already_printed_part= ""
        for chunk in chat.send_message_stream(f"CONTEXTO:\n {get_context()}\n\n SOLICITUD:\n {inp}"): 
            if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
                continue
            for part in chunk.candidates[0].content.parts: 
                if part.thought: continue
                if part.text and part.text != already_printed_part:
                    print(Style.BRIGHT + f"{part.text}", end= '', flush= True)
                    already_printed_part= part.text
                    time.sleep(0.01)
        already_printed_part= ""
        print('\n'+Style.RESET_ALL)
        finished= Notification(
            app_id= 'Christina',
            title= 'Finished:',
            msg= inp,
            duration= 'short',
            icon= KURISU_ICON_PATH
        )
        finished.set_audio(sound= audio.Reminder, loop= False)
        finished.show()

        historial_act= chat.get_history()
        hist= historial_act
        Chats_history.guardar_historial(HISTORIAL_PATH, chat_list= hist)

        client.close()
    except genai.errors.APIError as e:
        if "429" in str(e) or "ResourceExhausted" in str(e):
            print(Fore.RED + Style.BRIGHT + "\n[Error 429: Límite de solicitudes o tokens excedido. El historial de chat podría estar muy pesado.]")
            print(Fore.YELLOW + "[Sugerencia: Escribe 'clear' para borrar el historial de chat acumulado.]\n" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"\n[Error de API: {e}]\n" + Style.RESET_ALL)
    except genai.errors.ServerError as e:
        disp_model= ( 
            "models/gemini-3.5-flash"
            if kurisu_config['model_name'] == "models/gemini-2.5-flash" 
            else "models/gemini-2.5-flash"
        )

        Utilities.set_attribute(
            'model_name', 
            disp_model, 
            conf_file= CONFIG_PATH
        )
        kurisu_config, config_mod= cargar_conf()