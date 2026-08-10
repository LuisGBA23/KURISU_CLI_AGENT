from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import sys
import platform
import time
from colorama import Fore, Style
import Utilities, Chats_history, Functions, Web_functions

load_dotenv()
API_LIST= os.getenv("GEMINI_KEYS").split(',')
if not API_LIST: 
    raise ValueError("missing env vars")
CONFIG_PATH= Utilities.get_path_to_parent_dict(__file__, 'configs', 'Kurisu_config.json')
SYS_INST_PATH= Utilities.get_path_to_parent_dict(__file__, 'configs', 'system_instruction.md')
HISTORIAL_PATH= Utilities.get_path_to_parent_dict(__file__, 'configs', 'historial.pkl')
REGISTRY= [
    Functions.command_exec, 
    Functions.work_with_files, 
    Functions.specific_edit_files, 
    Functions.do_a_commit,
    Web_functions.busqueda_internet,
    Web_functions.make_http_request,
    Web_functions.html_parser
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
    }

    return context

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

        inp= input(Fore.CYAN + "(Christina) >> " + Fore.RESET)
        if inp.lower() == "byebye": 
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
